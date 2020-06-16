# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

import json
from kral2.network import *
import socket
import time
from kral2.game.vec2 import Vec2

if TYPE_CHECKING:
    from typing import Dict, List, Optional
    from kral2.game.gameobject import GameObject


class RemoteClient:
    def __init__(self, sock: socket.socket, ip, port, client_id, name):
        self._s = sock
        self.client_id = client_id
        self.ip = ip
        self.port = port
        self.name = name
        self.lastping = time.time()
        self.pressed = {'w': False, 'a': False, 's': False, 'd': False, 'j': False, 'k': False}
        self.object: Optional[GameObject] = None

    def send(self, data):
        self._s.sendto(SIGNATURE + data, (self.ip, self.port))


class LocalServer:
    def __init__(self, ip, port, gen_object_for_client_func, try_to_build_func, try_to_destroy_func):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.setblocking(False)
        self._s.bind((ip, port))
        self._last_client_id = 12
        self._clients: Dict[int, RemoteClient] = {}
        self.objects: List[GameObject] = []
        self.gen_object_for_client = gen_object_for_client_func
        self.trytobuild = try_to_build_func
        self.trytodestroy = try_to_destroy_func
        self.lastsync = 0
        self.lastobjs = {}

    def cleanup(self):
        for cid in list(self._clients):
            if time.time() - self._clients[cid].lastping > PING_TIMEOUT:
                print('TIMEOUT', cid)
                try:
                    self.objects.remove(self._clients[cid].object)
                except ValueError:
                    print("Warning: timeout: client has not object")
                del self._clients[cid]

    def dumpall(self) -> bytes:
        result = []
        for obj in self.objects:
            result.append(obj.to_dict())
        return json.dumps(result).encode()

    def update(self):
        try:
            while True:
                msg, (ip, port) = self._s.recvfrom(1024)
                if not msg.startswith(SIGNATURE):
                    continue
                msg = msg[len(SIGNATURE):]
                if msg.startswith(NEW_CLIENT):
                    self._last_client_id = (self._last_client_id + 1) % 255
                    try:
                        name = msg[len(NEW_CLIENT):].decode()
                    except UnicodeDecodeError:
                        print('Invalid name')
                        name = '<invalid name>'
                    client = RemoteClient(self._s, ip, port, self._last_client_id, name)
                    client.send(self._last_client_id.to_bytes(1, 'little'))
                    self._clients[self._last_client_id] = client
                    obj = self.gen_object_for_client(client.client_id, client.name)
                    client.object = obj
                    client.send(OBJ_FOR_CLIENT + obj.id.to_bytes(3, 'little'))
                    client.send(OBJ_FOR_CLIENT + obj.id.to_bytes(3, 'little'))
                    client.send(OBJ_FOR_CLIENT + obj.id.to_bytes(3, 'little'))
                    client.send(SERVER_OBJECTS + self.dumpall())
                    print('NEW', client.client_id, client.name)
                else:
                    client = self._clients.get(msg[0])
                    if not client:
                        continue
                    if msg[1:2] == CLIENT_PRESS:
                        if len(msg) != 8:  # client_id + CLIENT_PRESS + w a s d j k
                            continue
                        client.lastping = time.time()
                        client.pressed = {
                            'w': bool(msg[2]),
                            'a': bool(msg[3]),
                            's': bool(msg[4]),
                            'd': bool(msg[5]),
                            'j': bool(msg[6]),
                            'k': bool(msg[7]),
                        }
                        # print('PRESS', client.client_id, client.pressed)

        except BlockingIOError:
            pass

        now = time.time()
        if now - self.lastsync > 60:
            for client in self._clients.values():
                client.send(SERVER_OBJECTS + self.dumpall())
            self.lastsync = now
        else:
            for oid in self.lastobjs:
                self.lastobjs[oid].processed = False
            for obj in self.objects:
                lo = self.lastobjs.get(obj.id)
                if not lo or lo.pos != obj.pos:  # FIXME: other attributes
                    for client in self._clients.values():
                        client.send(EDIT_OBJECT + json.dumps(obj.to_dict()).encode())
                        client.send(EDIT_OBJECT + json.dumps(obj.to_dict()).encode())
                self.lastobjs[obj.id] = obj.copy()
                self.lastobjs[obj.id].processed = True

            for oid in list(self.lastobjs):
                if not self.lastobjs[oid].processed:
                    for client in self._clients.values():
                        client.send(DELETE_OBJECT + oid.to_bytes(3, 'little'))
                    del self.lastobjs[oid]
        self.cleanup()
        self.update_for_input()

    def update_for_input(self):
        for client in self._clients.values():
            if client.object:
                movepos = Vec2(0, 0)
                if client.pressed['w']:
                    movepos += Vec2(0, -1)
                if client.pressed['a']:
                    movepos += Vec2(-1, 0)
                if client.pressed['s']:
                    movepos += Vec2(0, 1)
                if client.pressed['d']:
                    movepos += Vec2(1, 0)
                if client.pressed['j']:
                    self.trytobuild(client.object)
                if client.pressed['k']:
                    self.trytodestroy(client.object)
                client.object.move(movepos)

# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

import json
from kral2.network import *
import socket
import time

if TYPE_CHECKING:
    from typing import List


class LocalClient:
    def __init__(self, ip, port):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.connect((ip, port))
        self._s.send(SIGNATURE + NEW_CLIENT)
        res = self._s.recv(1024)
        self._s.setblocking(False)
        if len(res) != len(SIGNATURE) + 1 or not res.startswith(SIGNATURE):
            raise Exception('bad server')
        self.client_id = res[-1]

        self.pressed = {'w': False, 'a': False, 's': False, 'd': False, 'j': False, 'k': False}
        self.oldpressed = self.pressed.copy()
        self.lastping = time.time()
        self.objects = {}
        self.modified_objects = {}
        self.client_object_id = None

    def update(self):
        try:
            while True:
                msg = self._s.recv(2**20)
                if not msg.startswith(SIGNATURE):
                    continue
                msg = msg[len(SIGNATURE):]
                if msg.startswith(SERVER_OBJECTS):
                    self.objects = {}
                    for obj in json.loads(msg[1:].decode()):
                        self.objects[obj['id']] = obj
                    self.modified_objects = self.objects.copy()
                elif msg.startswith(OBJ_FOR_CLIENT):
                    msg = msg[len(OBJ_FOR_CLIENT):]
                    oid = msg[0] + msg[1] * 2**8 + msg[2] * 2**16
                    self.client_object_id = oid
                elif msg.startswith(EDIT_OBJECT):
                    obj = json.loads(msg[1:].decode())
                    self.objects[obj['id']] = obj
                    self.modified_objects[obj['id']] = obj.copy()
                elif msg.startswith(DELETE_OBJECT):
                    msg = msg[1:]
                    oid = msg[0] + msg[1] * 2**8 + msg[2] * 2**16
                    try:
                        del self.objects[oid]
                    except KeyError:
                        print('Warning: DELETE_OBJECT: object not found.')
        except BlockingIOError:
            pass
        if self.oldpressed != self.pressed or time.time() - self.lastping > PING_TIMEOUT / 2:
            pdata = b''
            for btn in self.pressed:
                pdata += b'\x01' if self.pressed[btn] else b'\x00'
            self.send(CLIENT_PRESS + pdata)
            self.send(CLIENT_PRESS + pdata)  # can we trust now?
            self.oldpressed = self.pressed.copy()
            self.lastping = time.time()

    def send(self, data):
        self._s.send(SIGNATURE + self.client_id.to_bytes(1, 'little') + data)

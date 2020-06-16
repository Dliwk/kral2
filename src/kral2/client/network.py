# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

import json
from kral2.network import *
import socket
import time
import threading

if TYPE_CHECKING:
    from typing import Optional


class LocalClient:
    def __init__(self, ip, port, name="Unknown Player"):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.connect((ip, port))
        self.name = name.encode()
        self._s.send(SIGNATURE + NEW_CLIENT + self.name)
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
        self.gbt = None

    def update(self):
        try:
            while True:
                msg = self._s.recv(2**20)
                if not msg.startswith(SIGNATURE):
                    continue
                msg = msg[len(SIGNATURE):]
                if msg.startswith(SERVER_OBJECTS):
                    if not (self.gbt and not self.gbt.finished):
                        def reload(data):
                            nonlocal self
                            self.objects = {}
                            for gobj in json.loads(data.decode()):
                                self.objects[gobj['id']] = gobj
                            self.modified_objects = self.objects.copy()

                        self.gbt = self.get_big(SERVER_OBJECTS, on_finish=reload)
                    self.gbt.new_shatter(msg)
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

    def get_big(self, prefix, on_finish):
        class GetBigThread(threading.Thread):
            def __init__(self, _prefix, _on_finish, _socket, _client_id):
                super().__init__(daemon=True)
                self._prefix = _prefix
                self._on_finish = _on_finish
                self._s = _socket
                self._data = {}
                self._count = 9999999999  # Hmm
                self._end_received = False
                self._client_id = _client_id
                self.finished = False

            def new_shatter(self, data):
                if data[0:1] == self._prefix and data[1:2] == OBJECTS_SHATTER:
                    count = data[2] + data[3] * 2**8 + data[4] * 2**16
                    if data[5:] == b'END':
                        self._end_received = True
                        self._count = count
                    else:
                        self._data[count] = data[5:]

            def run(self):
                time.sleep(1)
                while not self._end_received and len(self._data) < self._count:
                    if self._end_received:
                        count = self._count
                    else:
                        count = max(self._data) if self._data else 999999999
                    for i in range(count):
                        if i not in self._data:
                            self._s.send(
                                self._client_id.to_bytes(1, 'little') +
                                RETRY_SHATTER +
                                i.to_bytes(3, 'little'))
                    time.sleep(1)
                self._on_finish(b''.join(list(self._data.values())))
                self.finished = True
        gbt = GetBigThread(prefix, on_finish, self._s, self.client_id)
        gbt.start()
        return gbt

    def send(self, data):
        self._s.send(SIGNATURE + self.client_id.to_bytes(1, 'little') + data)

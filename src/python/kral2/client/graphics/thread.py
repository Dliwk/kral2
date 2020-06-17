# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

import sys
import multiprocessing
import pygame as pg
from kral2.client.graphics.sprite import spritefrom
from kral2.client.graphics.camera import Camera
from kral2.game.vec2 import Vec2

if TYPE_CHECKING:
    from typing import Sequence
    from kral2.client.network import LocalClient


class GraphicsThread(multiprocessing.Process):
    def __init__(self, localclient: LocalClient, winsize: Sequence[int] = (800, 600)):
        super().__init__()
        self._winsize = winsize
        self._client = localclient
        self._ui_sprites = {}
        self._game_sprites = {}
        self._ui_sprites_group = pg.sprite.Group()
        self._game_sprites_group = pg.sprite.Group()

    def run(self):
        pg.init()
        display = pg.display.set_mode(self._winsize)
        clock = pg.time.Clock()
        camera = Camera(Vec2(0, 0), self._winsize)

        _running = True
        while _running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    _running = False
            display.fill((0, 0, 0))

            self._client.pressed['w'] = pg.key.get_pressed()[pg.K_w]
            self._client.pressed['a'] = pg.key.get_pressed()[pg.K_a]
            self._client.pressed['s'] = pg.key.get_pressed()[pg.K_s]
            self._client.pressed['d'] = pg.key.get_pressed()[pg.K_d]
            self._client.pressed['j'] = pg.key.get_pressed()[pg.K_j]
            self._client.pressed['k'] = pg.key.get_pressed()[pg.K_k]
            self._client.update()

            for oid, obj in self._client.modified_objects.copy().items():
                if oid not in self._game_sprites:
                    self._game_sprites[oid] = spritefrom(obj)
                    self._game_sprites[oid].add(self._game_sprites_group)
                else:
                    sprite = spritefrom(obj)
                    self._game_sprites[oid].sync_with(sprite)
                del self._client.modified_objects[oid]

            for oid in self._game_sprites:
                self._game_sprites[oid].tracking = False

            for oid, obj in self._client.objects.items():
                self._game_sprites[oid].tracking = True

            for oid in self._game_sprites:
                if not self._game_sprites[oid].tracking:
                    self._game_sprites[oid].kill()

            client_object = self._client.objects.get(self._client.client_object_id)
            if client_object:
                camera.center = Vec2(client_object['pos']['x'], client_object['pos']['y'])
            camera.update(self._game_sprites.values())

            self._ui_sprites_group.draw(display)
            self._game_sprites_group.draw(display)
            clock.tick(60)
            pg.display.flip()

        sys.exit(0)

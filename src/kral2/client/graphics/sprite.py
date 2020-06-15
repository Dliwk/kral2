# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg
from kral2.game.vec2 import Vec2

if TYPE_CHECKING:
    from typing import Dict


class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, width, height, color):
        super().__init__()
        self.pos = pos
        self.width = width
        self.height = height

        self.image = pg.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def sync_with(self, sprite: Sprite):
        self.pos = sprite.pos
        self.width = sprite.width
        self.image = sprite.image
        self.rect = sprite.rect


def spritefrom(obj: Dict) -> Sprite:
    if obj['type'] == 'GameObject':
        return Sprite(
            pos=Vec2(obj['pos']['x'], obj['pos']['y']),
            width=obj['width'],
            height=obj['height'],
            color=obj['color'])

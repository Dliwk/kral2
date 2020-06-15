# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

from kral2.game.vec2 import Vec2

if TYPE_CHECKING:
    from typing import Sequence, Optional


class Camera:
    def __init__(self, position: Vec2, winsize):
        self.pos = position
        self._maxradius = 1000
        self._winsize = winsize

    @property
    def center(self):
        return self.pos + Vec2(self._winsize[0] / 2, self._winsize[1] / 2)

    @center.setter
    def center(self, value: Vec2):
        self.pos = value - Vec2(self._winsize[0] / 2, self._winsize[1] / 2)

    def update(self, sprites):
        for sprite in sprites:
            if (sprite.pos - self.pos).len() > self._maxradius:
                continue
            pos = sprite.pos - self.pos
            sprite.rect.x = pos.x
            sprite.rect.y = pos.y

    def move(self, position):
        self.pos += position

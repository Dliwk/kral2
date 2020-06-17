# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

from kral2.game.gameobject import GameObject
from kral2.game.textobj import TextObject
from kral2.game.vec2 import Vec2

if TYPE_CHECKING:
    from typing import Sequence, Optional


class PlayerObject(GameObject):
    def __init__(self, pos: Vec2, width, height, color, name):
        super().__init__(pos, width, height, color)
        self.name = TextObject(pos, width, height, color, name)
        self.targetobj = TargetObject(player=self)
        self.block = False

    def postinit(self):
        super().postinit()
        self.activity.add_object(self.targetobj)
        self.activity.add_object(self.name)

    def move(self, pos: Vec2):
        toffset = Vec2(0, 0)
        super().move(pos)
        if pos.x > 0:
            toffset += Vec2(self.width, 0)
        if pos.x < 0:
            toffset += Vec2(-self.width, 0)
        if pos.y > 0:
            toffset += Vec2(0, self.height)
        if pos.y < 0:
            toffset += Vec2(0, -self.height)
        if toffset != Vec2(0, 0):
            self.targetobj.offset = toffset
        self.name.pos = self.pos + Vec2(0, -self.height)

    def die(self):
        super().die()
        self.name.die()
        self.targetobj.die()


class TargetObject(GameObject):
    BUILDABLE_COLOR = (0, 255, 0)
    FORBIDDEN_COLOR = (255, 0, 0)

    def __init__(self, player: PlayerObject):
        self.player = player
        self.offset = Vec2(0, -self.player.height)
        super().__init__(player.pos + self.offset, self.player.width, self.player.height,
                         color=self.BUILDABLE_COLOR,
                         collide=False)
        self.block = False

    def die(self):
        super().die()

    def update(self):
        super().update()
        self.pos = self.player.pos + self.offset
        if self.activity.is_collide_any(self):
            self.color = self.FORBIDDEN_COLOR
        else:
            self.color = self.BUILDABLE_COLOR

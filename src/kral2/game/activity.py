# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

from kral2.game.gameobject import GameObject
from kral2.game.playerobj import PlayerObject, TargetObject
from kral2.game import Vec2
from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import List, Union


@dataclass
class Rect:
    x: Union[float, int]
    y: Union[float, int]
    width: Union[float, int]
    height: Union[float, int]


class Activity:
    def __init__(self):
        self.objects: List[GameObject] = []
        self.next_oid = 0

    @staticmethod
    def is_collide(obj1, obj2):
        rect1 = Rect(obj1.pos.x - obj1.width / 2, obj1.pos.y - obj1.height / 2, obj1.width, obj1.height)
        rect2 = Rect(obj2.pos.x - obj2.width / 2, obj2.pos.y - obj2.height / 2, obj2.width, obj2.height)
        return (rect1.x < rect2.x + rect1.width and
                rect1.x + rect2.width > rect2.x and
                rect1.y < rect2.y + rect1.height and rect1.height + rect1.y > rect2.y)

    def is_collide_any(self, obj):
        for go in self.objects:
            if obj is not go and self.is_collide(obj, go) and go.collide:
                return go
        return None

    def add_object(self, obj: GameObject):
        obj.id = self.next_oid
        obj.activity = self
        self.objects.append(obj)
        self.next_oid += 1
        obj.postinit()

    def spawn_player(self, client_id, name):
        obj = PlayerObject(Vec2(0, 0), 10, 10, (255, 255, 0), name)
        self.add_object(obj)
        return obj

    def try_to_build(self, player: PlayerObject):
        obj = GameObject(player.targetobj.pos, 10, 10, (255, 255, 255))
        if not self.is_collide_any(obj):
            self.add_object(obj)

    def try_to_destroy(self, player: PlayerObject):
        target = player.targetobj
        obj = self.is_collide_any(target)
        if obj and not isinstance(obj, PlayerObject) and not isinstance(obj, TargetObject):
            obj.die()

    def update(self):  # One tick
        diedobjs = []
        for obj in self.objects:
            if obj.died:
                diedobjs.append(obj)
            obj.update()
        for obj in diedobjs:
            self.objects.remove(obj)

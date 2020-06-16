# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

from kral2.game.activity import Activity
from kral2.game.gameobject import GameObject
from kral2.game.vec2 import Vec2

if TYPE_CHECKING:
    from typing import Sequence, Optional


class DefaultGame(Activity):
    def __init__(self):
        super().__init__()
        # for i in range(-100, 100, 50):
        #     self.add_object(GameObject(Vec2(i, 50), 10, 10, (255, 255, 255)))

# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

from kral2.game.gameobject import GameObject

if TYPE_CHECKING:
    pass


class TextObject(GameObject):
    def __init__(self, pos, width, height, color, text, activity=None):
        super().__init__(pos, width, height, color, activity=activity, collide=False)
        self.text = text
        self.block = False

    def to_dict(self):
        res = super().to_dict()
        res['type'] = 'TextObject'
        res['text'] = self.text
        return res

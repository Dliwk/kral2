# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg
from kral2.game.vec2 import Vec2

if TYPE_CHECKING:
    from typing import Dict, Union


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
        self.height = sprite.height
        self.image = sprite.image
        self.rect = sprite.rect


class TextSprite(pg.sprite.Sprite):
    def __init__(self, pos, width, height, color, text):
        super().__init__()
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text
        self.color = color

        self.image = pg.font.Font(None, 15).render(
            self.text, 1, self.color
        )
        self.rect = self.image.get_rect()

    def sync_with(self, sprite: TextSprite):
        self.pos = sprite.pos
        self.width = sprite.width
        self.height = sprite.height
        self.text = sprite.text
        self.image = sprite.image
        self.rect = sprite.rect


def spritefrom(obj: Dict) -> Union[Sprite, TextSprite]:
    if obj['type'] == 'GameObject':
        return Sprite(
            pos=Vec2(obj['pos']['x'], obj['pos']['y']),
            width=obj['width'],
            height=obj['height'],
            color=obj['color'])
    elif obj['type'] == 'TextObject':
        return TextSprite(
            pos=Vec2(obj['pos']['x'], obj['pos']['y']),
            width=obj['width'],
            height=obj['height'],
            color=obj['color'],
            text=obj['text'])

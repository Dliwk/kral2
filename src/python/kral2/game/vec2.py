# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Vec2(self.x, self.y)

    def __add__(self, other: Vec2):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2):
        return Vec2(self.x - other.x, self.y - other.y)

    def __eq__(self, other: Vec2):
        return self.x == other.x and self.y == other.y

    def len(self):
        return (self.x**2 + self.y**2)**0.5

    def to_dict(self):
        return {'x': self.x, 'y': self.y}

    def __repr__(self):
        return f'<Vec2({self.x}, {self.y}) object>'

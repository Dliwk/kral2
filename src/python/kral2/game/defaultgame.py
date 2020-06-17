# Copyright (c) 2020 Roman Trapeznikov
from __future__ import annotations

from typing import TYPE_CHECKING

from kral2.game.activity import Activity

if TYPE_CHECKING:
    pass


class DefaultGame(Activity):
    def __init__(self):
        super().__init__()

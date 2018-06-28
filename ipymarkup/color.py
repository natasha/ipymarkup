# coding: utf-8
from __future__ import unicode_literals

from .utils import Record


class Colors(Record):
    __attributes__ = ['colors']

    def __init__(self, colors):
        self.colors = colors
        self.index = 0
        self.mapping = {}

    def __getitem__(self, key):
        if key in self.mapping:
            return self.mapping[key]
        color = self.colors[self.index]
        self.index = (self.index + 1) % len(self.colors)
        self.mapping[key] = color
        return color


class Soft:
    BLUE = '#aec7e8'
    ORANGE = '#ffbb78'
    GREEN = '#98df8a'
    RED = '#ff9896'
    PURPLE = '#c5b0d5'

    COLORS = [
        BLUE,
        ORANGE,
        GREEN,
        RED,
        PURPLE
    ]


LINE = Colors(Soft.COLORS)


class Shade:
    YELLOW = '#ffffc2'
    DARK_YELLOW = '#fdf07c'
    DARKER_YELLOW = '#c3b95f'

    BLUE = '#ecf6ff'
    DARK_BLUE = '#c6e1f9'
    DARKER_BLUE = '#98bbda'

    ORANGE = '#fff1e4'
    DARK_ORANGE = '#ffd9b4'
    DARKER_ORANGE = '#ffbb78'

    GREEN = '#efffec'
    DARK_GREEN = '#afeca3'
    DARKER_GREEN = '#98df8a'

    RED = '#fff1f1'
    DARK_RED = '#ffd6d5'
    DARKER_RED = '#ff9896'

    COLORS = [
        YELLOW,
        BLUE,
        ORANGE,
        GREEN,
        RED
    ]
    DARK = [
        DARK_YELLOW,
        DARK_BLUE,
        DARK_ORANGE,
        DARK_GREEN,
        DARK_RED
    ]
    DARKER = [
        DARKER_YELLOW,
        DARKER_BLUE,
        DARKER_ORANGE,
        DARKER_GREEN,
        DARKER_RED
    ]


BACKGROUND = Colors(Shade.COLORS)

DARKER = dict(zip(
    Shade.COLORS,
    Shade.DARK
))

EVEN_DARKER = dict(zip(
    Shade.COLORS,
    Shade.DARKER
))


def register(type):
    LINE[type]
    BACKGROUND[type]

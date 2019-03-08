# coding: utf-8
from __future__ import unicode_literals

import re

from .utils import Record, assert_type


class Color(Record):
    __attributes__ = ['value', 'darker']

    def __init__(self, value, darker=None):
        if not re.match(r'^#[0-9a-f]{6}$', value):
            raise ValueError('Bad rgb: %r' % value)
        self.value = value
        if darker:
            assert_type(darker, Color)
        self.darker = darker


class Palette(Record):
    __attributes__ = ['colors']

    def __init__(self, colors):
        if not colors:
            raise ValueError('colors empty')
        for color in colors:
            assert_type(color, Color)
        self.colors = colors

        self.cache = {}
        self.default = self.colors[0]
        self.index = 0

    def get(self, type):
        if not type:
            return self.default
        if type not in self.cache:
            index = self.index % len(self.colors)
            color = self.colors[index]
            self.cache[type] = color
            self.index += 1
        return self.cache[type]

    def register(self, type, color=None):
        type = str(type)
        if not color and type in self.cache:
            return
        if not color:
            color = self.get(type)
        assert_type(color, Color)
        self.cache[type] = color


SOFT_BLUE = Color('#aec7e8')
SOFT_ORANGE = Color('#ffbb78')
SOFT_GREEN = Color('#98df8a')
SOFT_RED = Color('#ff9896')
SOFT_PURPLE = Color('#c5b0d5')
SOFT_PALETTE = Palette([
    SOFT_BLUE, SOFT_ORANGE,
    SOFT_GREEN, SOFT_RED, SOFT_PURPLE
])

YELLOW = Color('#ffffc2', Color('#fdf07c', Color('#c3b95f')))
BLUE = Color('#ecf6ff', Color('#c6e1f9', Color('#98bbda')))
ORANGE = Color('#fff1e4', Color('#ffd9b4', Color('#ffbb78')))
GREEN = Color('#efffec', Color('#afeca3', Color('#98df8a')))
RED = Color('#fff1f1', Color('#ffd6d5', Color('#ff9896')))
PALETTE = Palette([
    YELLOW, BLUE, ORANGE,
    GREEN, RED
])

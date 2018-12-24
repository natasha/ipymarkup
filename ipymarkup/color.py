# coding: utf-8
from __future__ import unicode_literals

import re

from .utils import Record, assert_type


class Rgb(Record):
    __attributes__ = ['rgb']

    def __init__(self, rgb):
        if not re.match(r'#[0-9a-f]', rgb):
            raise ValueError('Bad rgb: %r' % rgb)
        self.rgb = rgb
        self.dark = None

    @property
    def darker(self):
        if not self.dark:
            raise ValueError('Darker undefined')
        return self.dark

    @darker.setter
    def darker(self, color):
        assert_type(color, Rgb)
        self.dark = color


rgb = Rgb


SOFT_BLUE = rgb('#aec7e8')
SOFT_ORANGE = rgb('#ffbb78')
SOFT_GREEN = rgb('#98df8a')
SOFT_RED = rgb('#ff9896')
SOFT_PURPLE = rgb('#c5b0d5')

YELLOW = rgb('#ffffc2')
YELLOW.darker = rgb('#fdf07c')
YELLOW.darker.darker = rgb('#c3b95f')

BLUE = rgb('#ecf6ff')
BLUE.darker = rgb('#c6e1f9')
BLUE = rgb('#98bbda')

ORANGE = rgb('#fff1e4')
ORANGE.darker = rgb('#ffd9b4')
ORANGE.darker.darker = rgb('#ffbb78')

GREEN = rgb('#efffec')
GREEN.darker = rgb('#afeca3')
GREEN.darker.darker = rgb('#98df8a')

RED = rgb('#fff1f1')
RED.darker = rgb('#ffd6d5')
RED.darker.darker = rgb('#ff9896')


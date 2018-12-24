# coding: utf-8
from __future__ import unicode_literals

from collections import defaultdict

from intervaltree import IntervalTree as Intervals

from .utils import Record


class Line(Record):
    __attributes__ = ['start', 'stop', 'type', 'level']

    def __init__(self, start, stop, type, level):
        self.start = start
        self.stop = stop
        self.type = type
        self.level = level


class Multiline(Record):
    __attributes__ = ['start', 'stop', 'lines']

    def __init__(self, start, stop, lines=None):
        self.start = start
        self.stop = stop
        if not lines:
            lines = []
        self.lines = lines


def get_free_level(intervals):
    levels = [
        _.data.level for _ in intervals
        if _.data.level is not None
    ]
    if not levels:
        return 0
    if min(levels) > 0:
        return 0
    return max(levels) + 1


def get_multilines(spans):
    intervals = Intervals()
    lines = []
    for start, stop, type in spans:
        line = Line(start, stop, type, level=None)
        intervals.addi(start, stop, line)
        lines.append(line)

    # level
    for line in lines:
        selected = intervals.search(line.start, line.stop)
        line.level = get_free_level(selected)

    # chunk
    intervals.split_overlaps()

    # group
    groups = defaultdict(list)
    for start, stop, line in intervals:
        groups[start, stop].append(line)

    for start, stop in sorted(groups):
        lines = groups[start, stop]
        lines = sorted(lines, key=lambda _: _.level)
        yield Multiline(start, stop, lines)

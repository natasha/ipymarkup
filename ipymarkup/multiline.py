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

    def __lt__(self, other):
        if self.level != other.level:
            return self.level < other.level
        else:
            if self.type != other.type:
                if self.type is None:
                    return True
                if other.type is None:
                    return False
                return self.type < other.type
            else:
                return False  # eq


class Multiline(Record):
    __attributes__ = ['start', 'stop', 'lines']

    def __init__(self, start, stop, lines=None):
        self.start = start
        self.stop = stop
        if not lines:
            lines = []
        self.lines = lines


def get_free_level(intervals):
    if not intervals:
        return 0
    levels = [_.data.level for _ in intervals]
    if min(levels) > 0:
        return 0
    return max(levels) + 1


def get_multilines(spans):
    # level
    intervals = Intervals()
    for start, stop, type in sorted(spans):
        selected = intervals.search(start, stop)
        level = get_free_level(selected)
        intervals.addi(start, stop, Line(start, stop, type, level))

    # chunk
    intervals.split_overlaps()

    # group
    groups = defaultdict(list)
    for start, stop, line in intervals:
        groups[start, stop].append(line)

    for start, stop in sorted(groups):
        lines = groups[start, stop]
        lines = sorted(lines)
        yield Multiline(start, stop, lines)

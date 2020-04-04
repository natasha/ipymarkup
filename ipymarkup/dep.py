
from html import escape
from collections import defaultdict

from intervaltree import IntervalTree as Intervals

from .show import show_html
from .record import Record
from .palette import GREY


########
#
#   MARKUP
#
########


ROOT = 'root'


class Dep(Record):
    __attributes__ = ['source', 'target', 'type']

    def __init__(self, source, target, type):
        if source == target:
            raise ValueError('loop dep: %r' % source)
        self.source = source
        self.target = target
        self.type = type


def prepare_dep(dep):
    if isinstance(dep, Dep):
        return dep

    source, target, type = None, None, None
    if isinstance(dep, (tuple, list)):
        if len(dep) == 2:
            source, target = dep
        elif len(dep) == 3:
            source, target, type = dep
    else:
        source = getattr(dep, 'source', None)
        target = getattr(dep, 'target', None)
        type = getattr(dep, 'type', None)

    if isinstance(source, int) and isinstance(target, int):
        return Dep(source, target, type)

    raise TypeError(dep)


def prepare_deps(deps):
    for dep in deps:
        yield prepare_dep(dep)


class DepMarkup(Record):
    __attributes__ = ['words', 'deps']

    def __init__(self, words, deps):
        self.words = words
        self.deps = deps


#######
#
#  ARC
#
######


LEFT = 'left'
RIGHT = 'right'

BEGIN = 'begin'
END = 'end'
INSIDE = 'inside'


class Arc(Record):
    __attributes__ = ['start', 'stop', 'direction', 'type', 'level']

    def __init__(self, start, stop, direction, type, level):
        self.start = start
        self.stop = stop
        self.direction = direction  # assert start < stop
        self.type = type
        self.level = level

    def layout_order(self):
        return self.stop - self.start, self.start

    def level_order(self):
        return -self.level


class ArcSection(Record):
    __attributes__ = ['part', 'direction', 'type', 'level', 'parent']

    def __init__(self, part, direction, type, level, parent):
        self.part = part
        self.direction = direction
        self.type = type
        self.level = level
        self.parent = parent

    @property
    def shape(self):
        pair = self.part, self.direction
        if pair in [(BEGIN, RIGHT), (END, LEFT)]:
            return RIGHT
        elif pair in [(END, RIGHT), (BEGIN, LEFT)]:
            return LEFT


class DepMarkupSection(Record):
    __attributes__ = ['word', 'arcs']

    def __init__(self, word, arcs):
        self.word = word
        self.arcs = arcs


########
#
#   LEVELS
#
#####


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


ASCII = 'ascii'
HTML = 'html'


def section_markup(markup, mode=HTML):
    arcs = []
    for source, target, type in markup.deps:
        if type == ROOT:
            continue

        if source < target:
            start, stop = source, target
            direction = RIGHT
        else:
            start, stop = target, source
            direction = LEFT

        arc = Arc(start, stop, direction, type, level=None)
        arcs.append(arc)

    # order
    arcs = sorted(arcs, key=Arc.layout_order)

    # level
    intervals = Intervals()
    for arc in arcs:
        stop = arc.stop
        if mode == ASCII:
            stop += 1  # in ascii mode include stop
        intervals.addi(arc.start, stop, arc)

    for arc in arcs:
        selected = intervals.overlap(arc.start, arc.stop)
        arc.level = get_free_level(selected)

    # group
    sections = defaultdict(list)
    for arc in arcs:
        start, stop, direction, type, level = arc
        parent = id(arc)
        for index in range(start, stop + 1):
            if index == start:
                part = BEGIN if direction == RIGHT else END
            elif index == stop:
                part = END if direction == RIGHT else BEGIN
            else:
                part = INSIDE

            section = ArcSection(part, direction, type, level, parent)
            sections[index].append(section)

    for index, word in enumerate(markup.words):
        arcs = sections[index]
        arcs = sorted(arcs, key=Arc.level_order)
        yield DepMarkupSection(word, arcs)


########
#
#   SPACE
#
#######


def space_section_arcs(previous):
    for arc in previous.arcs:
        if arc.part == INSIDE or arc.shape == RIGHT:
            yield ArcSection(
                INSIDE, arc.direction, arc.type,
                arc.level, arc.parent
            )


def add_space_sections(sections):
    size = len(sections)
    for index in range(size):
        section = sections[index]
        if index > 0:
            previous = sections[index - 1]
            arcs = list(space_section_arcs(previous))
            yield DepMarkupSection(word=None, arcs=arcs)
        yield section


########
#
#  HTML
#
#####


def format_dep_markup(words, deps,
                      arc_radius=5, arc_skew=5, arc_gap=10):
    deps = list(prepare_deps(deps))
    markup = DepMarkup(words, deps)
    sections = list(section_markup(markup))
    sections = list(add_space_sections(sections))

    yield '<div class="tex2jax_ignore">'
    for section in sections:
        yield '<span style="display: inline-block">'

        levels = []
        lefts, rights = 0, 0
        for arc in section.arcs:
            levels.append(arc.level)
            if arc.shape == LEFT:
                lefts += 1
            elif arc.shape == RIGHT:
                rights += 1

        height = 0
        if levels:
            height = arc_gap * (max(levels) + 2)  # extra gap for type text

        yield (
            '<span style="display: block; position: relative; '
            'min-width: %dpx; height: %dpx">' % (arc_radius, height)
        )

        gap = 100 / (lefts + rights + 1)
        left, right = 0, 0
        for arc in section.arcs:

            ######
            #   BORDER
            ######

            color = GREY
            style = [
                'display: block', 'position: absolute', 'bottom: 0',
                'border-top: 1px solid %s' % color.line.value,
                'height: %dpx' % (arc_gap * (arc.level + 1))
            ]
            if arc.part == INSIDE:
                style.append('width: 100%')
            elif arc.shape == RIGHT:
                #   ___
                #  /
                style.extend([
                    'right: 0', 'border-top-left-radius: %dpx' % arc_radius,
                    'border-left: 1px solid %s' % color.line.value,
                    'transform: skew(%ddeg)' % -arc_skew,
                    'width: %d%%' % ((rights - right) * gap),
                ])
                right += 1
            elif arc.shape in LEFT:
                #  __
                #    \
                style.extend([
                    'left: 0', 'border-top-right-radius: %dpx' % arc_radius,
                    'border-right: 1px solid %s' % color.line.value,
                    'transform: skew(%ddeg)' % arc_skew,
                    'width: %d%%' % ((lefts - left) * gap)
                ])
                left += 1
            yield '<span style="%s">' % '; '.join(style)

            if arc.part == END:

                #######
                #  ARROW
                #######

                # css triangle trick https://css-tricks.com/snippets/css/css-triangle/
                width, height = 3, 6
                style = [
                    'display: block', 'position: absolute',
                    'bottom: -1px',  # cover border a bit
                    'width: 0', 'height: 0',
                    'border-left: %dpx solid transparent' % width,
                    'border-right: %dpx solid transparent' % width,
                    'border-top: %dpx solid %s' % (height, color.line.value)
                ]
                if arc.direction == LEFT:
                    style.append('left: %dpx' % -width)
                elif arc.direction == RIGHT:
                    style.append('right: %dpx' % -width)
                yield '<span style="%s"></span>' % ('; '.join(style))

                #######
                #   LABEL
                ########

                if arc.type:
                    style = [
                        'display: block', 'position: absolute',
                        'top: %dpx' % -arc_gap,
                        'line-height: 1',
                        'font-size: %dpx' % (arc_gap * 0.9),  # to fit between lines
                        'color: %s' % color.text.value
                    ]
                    if arc.direction == LEFT:
                        style.append('transform: skew(%ddeg)' % arc_skew)  # recover
                    elif arc.direction == RIGHT:
                        style.append('transform: skew(%ddeg)' % -arc_skew)
                    yield '<span style="%s">' % '; '.join(style)
                    yield escape(arc.type)
                    yield '</span>'

            yield '</span>'  # end border
        yield '</span>'  # end section

        #######
        #  WORD
        #####

        yield '<span style="display: block">'
        if section.word:
            yield escape(section.word)
        else:  # space section
            yield '\xa0'
        yield '</span>'

        yield '</span>'

    yield '</div>'


#######
#
#   ASCII
#
####


def format_dep_ascii_markup(words, deps):
    deps = list(prepare_deps(deps))
    markup = DepMarkup(words, deps)
    sections = list(section_markup(markup, mode=ASCII))

    max_level = max(
        arc.level
        for section in sections
        for arc in section.arcs
    )
    width = (max_level + 1) * 2

    blocks, words, types = [], [], []
    for section in sections:
        row = [' '] * width
        type = None
        for arc in section.arcs:
            index = 2 * arc.level
            if arc.part == INSIDE:
                row[index] = ' '
                row[index + 1] = '│'
            else:
                if arc.part == BEGIN:
                    block = '─'
                elif arc.part == END:
                    block = '►'
                    type = arc.type
                row[index] = block

                if arc.shape == LEFT:
                    block = '└'
                elif arc.shape == RIGHT:
                    block = '┌'
                row[index + 1] = block
        blocks.append(list(reversed(row)))
        words.append(section.word)
        types.append(type)

    # Extend
    # ┌►xxxx└─┌─
    # ┌►┌─┌─xxxx

    height = len(sections)
    for y in range(height):
        for x in range(1, width):
            block = blocks[y][x]
            previous = blocks[y][x - 1]
            if block == ' ' and previous in '►─':
                blocks[y][x] = previous
                blocks[y][x - 1] = '─'

    size = max(len(_) for _ in words)
    for row, word, type in zip(blocks, words, types):
        word = word.ljust(size)
        type = type or ''
        yield ' '.join([''.join(row), word, type])


######
#
#  SHOW
#
######


def show_dep_markup(words, deps, **kwargs):
    deps = prepare_deps(deps)
    lines = format_dep_markup(words, deps, **kwargs)
    show_html(lines)


def show_dep_ascii_markup(words, deps):
    deps = prepare_deps(deps)
    for line in format_dep_ascii_markup(words, deps):
        print(line)

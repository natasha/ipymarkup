
import re
from collections import defaultdict
from textwrap import TextWrapper
from html import escape

from intervaltree import IntervalTree as Intervals

from .show import show_html
from .record import Record
from .palette import PALETTE


######
#
#   SPAN
#
#########


class Span(Record):
    __attributes__ = ['start', 'stop', 'type']

    def __init__(self, start, stop, type=None):
        if start >= stop:
            raise ValueError('invert span: (%r, %r)' % (start, stop))
        self.start = start
        self.stop = stop
        self.type = type


def order_spans(spans):
    return sorted(spans, key=lambda _: _.start)


def prepare_span(span):
    if isinstance(span, Span):
        return span

    start, stop, type = None, None, None
    if isinstance(span, (tuple, list)):
        if len(span) == 2:
            start, stop = span
        elif len(span) == 3:
            start, stop, type = span
    else:
        start = getattr(span, 'start', None)
        stop = getattr(span, 'stop', None)
        type = getattr(span, 'type', None)

    if isinstance(start, int) and isinstance(stop, int):
        return Span(start, stop, type)

    raise TypeError(span)


def prepare_spans(spans):
    for span in spans:
        yield prepare_span(span)


#########
#
#  MULTILINE
#
#######


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
        selected = intervals.overlap(line.start, line.stop)
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


###########
#
#   WRAP
#
########


def span_text_sections(text, spans):
    previous = 0
    for span in spans:
        start, stop, _ = span
        yield text[previous:start], None
        yield text[start:stop], span
        previous = stop
    yield text[previous:], None


def Wrapper(width):
    return TextWrapper(
        width,
        expand_tabs=False,
        replace_whitespace=False,
        drop_whitespace=False
    ).wrap


def wrap(text, width):
    wrapper = Wrapper(width)
    matches = re.finditer(r'([^\n\r]+)', text)
    for match in matches:
        start = match.start()
        line = match.group(1)
        for sub in wrapper(line):
            stop = start + len(sub)
            yield start, stop, sub
            start = stop


def distribute_multilines(wraps, multilines):
    index = 0
    for start, stop, line in wraps:
        slices = []
        while index < len(multilines):
            multi = multilines[index]
            if multi.start >= stop:
                break
            slice = Multiline(
                max(multi.start, start) - start,
                min(multi.stop, stop) - start,
                multi.lines
            )
            slices.append(slice)
            if multi.stop <= stop:
                index += 1
            else:
                break
        yield start, line, slices


def wrap_multilines(text, multilines, width):
    wraps = wrap(text, width)
    return distribute_multilines(wraps, multilines)


########
#
#   NER
#
######


def format_span_box_markup(text, spans, palette=PALETTE):
    spans = order_spans(prepare_spans(spans))

    yield (
        '<div class="tex2jax_ignore" '
        'style="white-space: pre-wrap">'  # render spaces
    )
    for text, span in span_text_sections(text, spans):
        text = escape(text)
        if not span:
            yield text
            continue

        color = palette.get(span.type)
        yield (
            '<span style="'
            'padding: 2px; '
            'border-radius: 4px; '
            'border: 1px solid {border}; '
            'background: {background}'
            '">'.format(
                background=color.background.value,
                border=color.border.value
            )
        )
        yield text
        if span.type:
            yield (
                '<span style="'
                'vertical-align: middle; '
                'margin-left: 2px; '
                'font-size: 0.7em; '
                'color: {color};'
                '">'.format(
                    color=color.text.value
                )
            )
            yield span.type
            yield '</span>'
        yield '</span>'
    yield '</div>'


def format_span_line_markup(text, spans, palette=PALETTE,
                            width=80, line_gap=8, line_width=3,
                            label_size=11, background='white'):
    spans = order_spans(prepare_spans(spans))
    multilines = list(get_multilines(spans))

    level_width = line_gap + line_width
    yield (
        '<div class="tex2jax_ignore" style="'
        'white-space: pre-wrap'
        '">'
    )
    for offset, line, multilines in wrap_multilines(text, multilines, width):
        yield '<div>'  # line block
        for text, multi in span_text_sections(line, multilines):
            text = escape(text)
            if not multi:
                yield (
                    '<span style="display: inline-block; '
                    'vertical-align: top">'
                )
                yield text
                yield '</span>'
                continue

            level = max(_.level for _ in multi.lines)
            margin = (level + 1) * level_width
            yield (
                '<span style="display: inline-block; '
                'vertical-align: top; position: relative; '
                'margin-bottom: {margin}px">'.format(
                    margin=margin
                )
            )

            for line in multi.lines:
                padding = line_gap + line.level * level_width
                color = palette.get(line.type)
                yield (
                    '<span style="'
                    'border-bottom: {line_width}px solid {color}; '
                    'padding-bottom: {padding}px'
                    '">'.format(
                        line_width=line_width,
                        padding=padding,
                        color=color.line.value
                    )
                )
            yield text
            for _ in multi.lines:
                yield '</span>'

            for line in multi.lines:
                if not line.type or offset + multi.start != line.start:
                    continue

                bottom = -line.level * level_width - line_gap
                yield (
                    '<span style="'
                    'font-size: {label_size}px; line-height: 1; '
                    'white-space: nowrap; '
                    'text-shadow: 1px 1px 0px {background}; '
                    'position: absolute; left: 0; '
                    'bottom: {bottom}px">'.format(
                        label_size=label_size,
                        background=background,
                        bottom=bottom
                    )
                )
                yield line.type
                yield '</span>'

            yield '</span>'  # close relative
        yield '</div>'  # close line
    yield '</div>'


def format_span_ascii_markup(text, spans, width=70):
    spans = order_spans(prepare_spans(spans))
    multilines = list(get_multilines(spans))

    for offset, line, multilines in wrap_multilines(text, multilines, width):
        yield line.replace('\t', ' ')

        if multilines:
            height = max(
                line.level
                for multi in multilines
                for line in multi.lines
            ) + 1
            width = len(line)
            matrix = [
                [' ' for _ in range(width)]
                for row in range(height)
            ]
            for multi in multilines:
                for line in multi.lines:
                    for x in range(multi.start, multi.stop):
                        matrix[line.level][x] = '─'
            for multi in multilines:
                for line in multi.lines:
                    if line.type and offset + multi.start == line.start:
                        size = line.stop - line.start
                        space = width - multi.start
                        type = line.type[:min(size, space)]
                        for x, char in enumerate(type):
                            x = multi.start + x
                            matrix[line.level][x] = char
            for row in matrix:
                yield ''.join(row)


########
#
#   SHOW
#
#######


def show_span_box_markup(text, spans, **kwargs):
    lines = format_span_box_markup(text, spans, **kwargs)
    show_html(lines)


def show_span_line_markup(text, spans, **kwargs):
    lines = format_span_line_markup(text, spans, **kwargs)
    show_html(lines)


def show_span_ascii_markup(text, spans, **kwargs):
    for line in format_span_ascii_markup(text, spans, **kwargs):
        print(line)

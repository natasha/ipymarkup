# coding: utf-8
from __future__ import unicode_literals

import re
from textwrap import TextWrapper
from cgi import escape

from .compat import str, range, basestring
from .utils import Record, assert_type
from .multiline import Multiline, get_multilines
from .color import (
    YELLOW,
    SOFT_BLUE
)


__all__ = [
    'Span',
    'BoxMarkup',
    'LineMarkup',
    'AsciiMarkup',

    'markup',
    'show_markup',
    'show_box_markup',
    'show_line_markup',
    'show_ascii_markup'
]


class Span(Record):
    __attributes__ = ['start', 'stop', 'type']

    def __init__(self, start, stop, type=None):
        assert_type(start, int)
        assert_type(stop, int)
        if start >= stop:
            raise ValueError('expected start < stop')
        self.start = start
        self.stop = stop
        if type is not None:
            type = str(type)
        self.type = type


class Html:
    def _repr_html_(self):
        return ''.join(self.as_html)


class Ascii:
    def _repr_pretty_(self, printer, cycle):
        for line in self.as_ascii:
            printer.text(line)
            printer.break_()


class Markup(Record):
    __attributes__ = ['text', 'spans']

    def __init__(self, text, spans):
        assert_type(text, basestring)
        self.text = text
        self.spans = list(spans)
        for span in self.spans:
            assert_type(span, Span)
        self.multilines = list(get_multilines(self.spans))


def chunk(text, spans):
    previous = 0
    for span in spans:
        start, stop, _ = span
        yield text[previous:start], None
        yield text[start:stop], span
        previous = stop
    yield text[previous:], None


class BoxMarkup(Html, Markup):
    def __init__(self, text, spans):
        Markup.__init__(self, text, spans)

    @property
    def as_html(self):
        yield (
            '<div class="tex2jax_ignore" '
            'style="white-space: pre-wrap">'
        )
        for text, span in chunk(self.text, self.spans):
            text = escape(text)
            if not span:
                yield text
                continue

            yield (
                '<span style="'
                'padding: 2px; '
                'border-radius: 4px; '
                'border: 1px solid {border}; '
                'background: {background}'
                '">'.format(
                    background=YELLOW.rgb,
                    border=YELLOW.darker.rgb
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
                        color=YELLOW.darker.darker.rgb
                    )
                )
                yield span.type
                yield '</span>'
            yield '</span>'
        yield '</div>'


def Wrapper(width):
    return TextWrapper(
        width,
        expand_tabs=False,
        replace_whitespace=False,
        drop_whitespace=False
    ).wrap


def fold(text, width):
    wrapper = Wrapper(width)
    matches = re.finditer(r'([^\n\r]+)', text)
    for match in matches:
        start = match.start()
        line = match.group(1)
        for fold in wrapper(line):
            stop = start + len(fold)
            yield start, stop, fold
            start = stop


def distribute(folds, multilines):
    index = 0
    for start, stop, line in folds:
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


def wrap(text, multilines, width):
    folds = fold(text, width)
    return distribute(folds, multilines)


class LineMarkup(Html, Markup):
    def __init__(self, text, spans,
                 width=80, line_gap=5, line_width=2,
                 label_size=8, background='white'):
        Markup.__init__(self, text, spans)
        assert_type(width, int)
        self.width = width
        assert_type(line_gap, int)
        self.line_gap = line_gap
        assert_type(line_width, int)
        self.line_width = line_width
        assert_type(label_size, int)
        self.label_size = label_size
        assert_type(background, basestring)
        self.background = background
        self.level_width = line_gap + line_width

    @property
    def as_html(self):
        yield (
            '<div class="tex2jax_ignore" style="'
            'white-space: pre-wrap'
            '">'
        )
        for offset, line, multilines in wrap(self.text, self.multilines, self.width):
            yield '<div>'  # line block
            for text, multi in chunk(line, multilines):
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
                margin = (level + 1) * self.level_width
                yield (
                    '<span style="display: inline-block; '
                    'vertical-align: top; position: relative; '
                    'margin-bottom: {margin}px">'.format(
                        margin=margin
                    )
                )

                for line in multi.lines:
                    padding = self.line_gap + line.level * self.level_width
                    yield (
                        '<span style="'
                        'border-bottom: {line_width}px solid {color}; '
                        'padding-bottom: {padding}px'
                        '">'.format(
                            line_width=self.line_width,
                            padding=padding,
                            color=SOFT_BLUE.rgb
                        )
                    )
                yield text
                for _ in multi.lines:
                    yield '</span>'

                for line in multi.lines:
                    if not line.type or offset + multi.start != line.start:
                        continue

                    bottom = -(line.level + 1) * self.level_width + self.line_width
                    bottom -= 1  # looks better
                    yield (
                        '<span style="background: {background}; '
                        'font-size: {label_size}px; line-height: 1; '
                        'position: absolute; left: 0; '
                        'bottom: {bottom}px">'.format(
                            label_size=self.label_size,
                            background=self.background,
                            bottom=bottom
                        )
                    )
                    yield line.type
                    yield '</span>'

                yield '</span>'  # close relative
            yield '</div>'  # close line
        yield '</div>'


class AsciiMarkup(Ascii, Markup):
    def __init__(self, text, spans, width=70):
        Markup.__init__(self, text, spans)
        self.width = width

    @property
    def as_ascii(self):
        for offset, line, multilines in wrap(self.text, self.multilines, self.width):
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
                            matrix[line.level][x] = '-'
                for multi in multilines:
                    for line in multi.lines:
                        if line.type and offset + line.start == multi.start:
                            size = line.stop - line.start
                            space = width - multi.start
                            type = line.type[:min(size, space)]
                            for x, char in enumerate(type):
                                x = multi.start + x
                                matrix[line.level][x] = char
                for row in matrix:
                    yield ''.join(row)


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


def markup(text, spans, Markup=BoxMarkup, **kwargs):
    spans = [prepare_span(_) for _ in spans]
    return Markup(text, spans, **kwargs)


def show_markup(text, spans, Markup=BoxMarkup, **kwargs):
    from IPython.display import display

    display(markup(text, spans, Markup, **kwargs))


show_box_markup = show_markup


def show_line_markup(text, spans, Markup=LineMarkup, **kwargs):
    show_markup(text, spans, Markup, **kwargs)


def show_ascii_markup(text, spans, Markup=AsciiMarkup, **kwargs):
    show_markup(text, spans, Markup, **kwargs)

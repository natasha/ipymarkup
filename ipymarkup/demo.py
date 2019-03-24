# coding: utf-8
from __future__ import unicode_literals

from .markup import HtmlMarkup
from .palette import PALETTE
from . import (
    Span,
    BoxMarkup,
    LineMarkup,
    AsciiMarkup
)


def is_space(char):
    import re
    return re.match(r'\s', char)


def generate_spans(text):
    mins = {}
    maxes = {}
    for index, char in enumerate(text):
        if is_space(char):
            continue
        if char not in mins:
            mins[char] = index
        maxes[char] = index
    for char in mins:
        if char in maxes:
            start = mins[char]
            stop = maxes[char] + 1
            yield Span(start, stop, type=char)


def generate_cases():
    text = 'a a a b b c c c'
    spans = list(generate_spans(text))
    yield text, spans

    text = 'a a a b b c e d d d f f g g h'
    spans = list(generate_spans(text))
    yield text, spans

    text = 'a d a b a a a b c c c f d'
    spans = list(generate_spans(text))
    yield text, spans

    text = 'a b b c c d e f g h h i i a'
    spans = list(generate_spans(text))
    yield text, spans


def init_palette(palette, types='abcdefghijklmno'):
    for type in types:
        palette.get(type)
    palette.get(None)


init_palette(PALETTE)


MARKUPS = [
    LineMarkup,
    BoxMarkup,
    AsciiMarkup,
]


def generate_cell(Markup, text, spans):
    markup = Markup(text, spans)
    if issubclass(Markup, HtmlMarkup):
        for line in markup.as_html:
            yield line
    elif issubclass(Markup, AsciiMarkup):
        yield '<pre>'
        yield '\n'.join(markup.as_ascii)
        yield '</pre>'


def generate_row(case):
    text, spans = case
    for Markup in MARKUPS:
        yield ''.join(generate_cell(Markup, text, spans))


def generate_header():
    for markup in MARKUPS:
        yield markup.__name__


def generate_table():
    yield generate_header()
    for case in generate_cases():
        yield generate_row(case)


def format_table(rows):
    yield '<table>'
    for row in rows:
        yield '<tr style="background: none">'
        for cell in row:
            yield '<td style="width: 20%">'
            yield cell
            yield '</td>'
        yield '</tr>'
    yield '</table>'


def show_html(lines):
    from IPython.display import display, HTML

    html = '\n'.join(lines)
    display(HTML(html))


def show_table():
    rows = generate_table()
    html = format_table(rows)
    show_html(html)

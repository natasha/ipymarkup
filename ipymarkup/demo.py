
import re

from .show import show_html
from .span import (
    Span,
    format_span_box_markup,
    format_span_line_markup,
    format_span_ascii_markup,
)
from .dep import (
    Dep,
    format_dep_markup,
    format_dep_ascii_markup
)
from .palette import PALETTE


is_space = re.compile(r'^\s$').match


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


def generate_span_cases():
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


def word_index(words, char):
    for index, word in enumerate(words):
        if char in word:
            return index


def generate_dep_cases():
    words = 'aaaaa bbbbb ccccc ddddd'.split()
    deps = []
    for source in range(4):
        for target in range(4):
            if source != target:
                dep = Dep(source, target, '%d%d' % (source, target))
                deps.append(dep)
    yield words, deps

    words = 'aaa bbb ccc ddd eee fff ggg'.split()
    deps = []
    for type in 'ab ad dc cb ag ge gf ea'.split():
        source, target = type
        source = word_index(words, source)
        target = word_index(words, target)
        dep = Dep(source, target, type)
        deps.append(dep)
    yield words, deps


def init_palette(palette, types='abcdefghijklmno'):
    for type in types:
        palette.get(type)
    palette.get(None)


init_palette(PALETTE)


SPAN_FORMATS = [
    format_span_box_markup,
    format_span_line_markup,
    format_span_ascii_markup
]
DEP_FORMATS = [
    format_dep_markup,
    format_dep_ascii_markup
]


def ascii_html(lines):
    yield '<pre>'
    yield '\n'.join(lines)
    yield '</pre>'


def generate_span_cell(format, text, spans):
    lines = format(text, spans)
    if format == format_span_ascii_markup:
        lines = ascii_html(lines)
    for line in lines:
        yield line


def generate_dep_cell(format, words, deps):
    lines = format(words, deps)
    if format == format_dep_ascii_markup:
        lines = ascii_html(lines)
    for line in lines:
        yield line


def generate_span_row(case):
    text, spans = case
    for format in SPAN_FORMATS:
        yield ''.join(generate_span_cell(format, text, spans))


def generate_dep_row(case):
    words, deps = case
    for format in DEP_FORMATS:
        yield ''.join(generate_dep_cell(format, words, deps))


def format_header(formats):
    for format in formats:
        header = format.__name__.replace('format', 'show')
        yield '<div style="margin-top: 2em">%s</div>' % header


def generate_table():
    yield format_header(SPAN_FORMATS)
    for case in generate_span_cases():
        yield generate_span_row(case)

    yield format_header(DEP_FORMATS)
    for case in generate_dep_cases():
        yield generate_dep_row(case)


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


def show_table():
    rows = generate_table()
    html = format_table(rows)
    show_html(html)

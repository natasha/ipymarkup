
from .ner import format_ner_box_markup, show_ner_box_markup  # noqa
from .ner import format_ner_line_markup, show_ner_line_markup  # noqa
from .ner import format_ner_ascii_markup, show_ner_ascii_markup  # noqa

from .dep import format_dep_markup, show_dep_markup  # noqa
from .dep import format_dep_ascii_markup, show_dep_ascii_markup  # noqa


# legacy
show_box_markup = show_ner_box_markup
show_line_markup = show_ner_line_markup
show_ascii_markup = show_ner_ascii_markup

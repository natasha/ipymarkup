
from .span import format_span_box_markup, show_span_box_markup  # noqa
from .span import format_span_line_markup, show_span_line_markup  # noqa
from .span import format_span_ascii_markup, show_span_ascii_markup  # noqa

from .dep import format_dep_markup, show_dep_markup  # noqa
from .dep import format_dep_ascii_markup, show_dep_ascii_markup  # noqa


# legacy
show_box_markup = show_span_box_markup
show_line_markup = show_span_line_markup
show_ascii_markup = show_span_ascii_markup

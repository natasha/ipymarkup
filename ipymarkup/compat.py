try:
    # Python 2
    str = unicode
    range = xrange
except NameError:
    # Python 3
    str = str
    range = range

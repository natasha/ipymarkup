try:
    # Python 2
    basestring = basestring
    str = unicode
    range = xrange
except NameError:
    # Python 3
    str = str
    basestring = str
    range = range

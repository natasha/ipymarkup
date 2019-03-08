
import re
import sys
from os.path import exists


def find(path):
    if not exists(path):
        raise RuntimeError('path not found: %r' % path)

    with open(path) as file:
        for line in file:
            match = re.search(r'\d+\.\d+\.\d+', line)
            if match:
                return match.group()

    raise RuntimeError('version not found')


def inc(version):
    try:
        parts = version.split('.')
        parts = map(int, parts)
        major, minor, fix = parts
    except ValueError:
        raise RuntimeError('bad version: %r' % version)

    return '%d.%d.%d' % (major, minor + 1, fix)


def patch(path, before, after):
    if not exists(path):
        raise RuntimeError('path not found: %r' % path)

    with open(path) as file:
        text = file.read()
        text = text.replace(before, after)
        with open(path, 'w') as file:
            file.write(text)


def main(args):
    if len(args) != 2:
        raise RuntimeError('version.py [get|inc] path')

    command, path = args
    if command == 'get':
        print(find(path))
    elif command == 'inc':
        before = find(path)
        after = inc(before)
        patch(path, before, after)
        print('%s: %s -> %s' % (path, before, after))


if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(args)
    except RuntimeError as error:
        sys.exit(error)

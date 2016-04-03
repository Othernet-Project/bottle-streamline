import re


WORD_RE = re.compile('([A-Z]+[a-z0-9]*)')


def decamelize(s):
    """
    Convert CamelCase string to lowercase. Boundary between words is converted
    to underscore.
    """
    return '_'.join(WORD_RE.findall(s)).lower()

import functools
from dateutil import parser

@functools.lru_cache(maxsize=None)
def date_parse(date):
    return parser.parse(date)

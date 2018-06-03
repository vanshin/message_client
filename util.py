#coding=utf8

import json

from functools import partial

def is_valid(s, func):
    try:
        func(s)
        return True
    except:
        return False

is_valid_json = partial(is_valid, func=json.loads)

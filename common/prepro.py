# coding=utf-8

"""This module contains functions to clean and tokenize text.

>>> s = u'''世界，你好！
... Hello, World!'''
>>> t = remove_symbols(s)
>>> t == u'世界 你好  Hello  World '
True
>>> u = tokenize_unicode_chars(t)
>>> u == '世 界   你 好     Hello    World  '
True
>>> v = normalize_spaces(u)
>>> v == u'世 界 你 好 Hello World '
True
>>> preprocess(s)
'世 界 你 好 hello world '
"""

import re


def remove_symbols(s):
    return re.sub(r'[^\w]', ' ', s, flags=re.UNICODE)


def tokenize_unicode_chars(s):
    return re.sub(r'([^A-Za-z])', '\\1 ', s, flags=re.UNICODE)


def normalize_spaces(s):
    return re.sub(r'\s+', ' ', s, flags=re.UNICODE).strip()


def preprocess(s):
    return normalize_spaces(tokenize_unicode_chars(remove_symbols(s))).lower()

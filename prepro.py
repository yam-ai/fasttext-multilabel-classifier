# coding=utf-8
# Copyright 2019 YAM AI Machinery Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
>>> v == u'世 界 你 好 Hello World'
True
>>> preprocess(s)
'世 界 你 好 hello world'
"""

import re


def remove_symbols(s):
    return re.sub(r'[^\w]', ' ', s, flags=re.UNICODE)


def tokenize_unicode_chars(s):
    return re.sub(r'([^A-Za-z])', '\\1 ', s, flags=re.UNICODE)


def normalize_spaces(s):
    return ' '.join(s.split())


def preprocess(s):
    return normalize_spaces(tokenize_unicode_chars(remove_symbols(s))).lower()

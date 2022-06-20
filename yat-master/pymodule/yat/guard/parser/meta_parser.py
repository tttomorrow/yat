#!/usr/bin/env python
# encoding=utf-8
"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
"""
this is the test case meta data parser.py, all meta text are write at the head of a test file with comment
or write at the test point near with comment, and the syntax is like javadoc:

    @owner: author name [owner1, owner2, ...]
    @date: the create-date test case [YYYY-MM-DD HH:mm:ss]
    @describe: the short describe of the test case
    @requirement: the requirement id/name [ id1, id2, ...]
    @developer: the developer's id [developer1, developer2, ...]
    @testpoint: the describe of the test point
    @dts: DTS No. and the fix owner [DTS_NUMBER1, DTS_NUMBER2, ...]

"""
from io import StringIO

from .comment_parser import CommentParser
from .errors import MetaParseError
from .meta import CaseMeta, DTS
from .meta_lex import Token
from .meta_lex import MetaLex


class MetaParser:
    """
    parse the meta text to CaseMeta instance
    """
    __blank = {
        Token.TYPE_TAB,
        Token.TYPE_BLANK
    }

    def __init__(self, script, line_mark=('#',), multiline_mark=None):
        comment_parser = CommentParser(script, line_mark, multiline_mark)
        comment = comment_parser.parse()
        self.lex_iter = MetaLex(StringIO(comment)).lex()
        self.meta = CaseMeta(script.name)

    def parse(self):
        """
        Parse the given meta text to CaseMeta
        """
        for line in self.lex_iter:
            self.parse_entry(iter(line))

        return self.meta

    def parse_entry(self, line):
        try:
            token = self.skip_blank(line)

            while True:
                if token.tp == Token.TYPE_AT:
                    self.parse_at(line)
                token = self.skip_blank(line)
        except StopIteration:
            pass

    def parse_at(self, line):
        token = next(line)
        if token.tp == Token.TYPE_WORD and next(line).tp == Token.TYPE_COLON:
            key = token.value
            meta_parser = self.__meta_map.get(key)
            if meta_parser:
                if not meta_parser['multiple'] and key in self.meta:
                    raise MetaParseError('@{} is duplicate'.format(key))

                value = meta_parser['parser.py'](self, line)

                if meta_parser['multiple']:
                    if key not in self.meta:
                        self.meta[key] = []
                    if isinstance(value, (list, tuple)):
                        self.meta[key].extend(value)
                    else:
                        self.meta[key].append(value)
                else:
                    self.meta[key] = value

    def parse_word(self, line):
        token = self.skip_blank(line)
        if token.tp == Token.TYPE_WORD:
            return token.value

    __tp_map = {
        Token.TYPE_COLON: ':',
        Token.TYPE_BLANK: ' ',
        Token.TYPE_TAB: '\t',
        Token.TYPE_AT: '@',
        Token.TYPE_COMMA: ','
    }

    def parse_lists(self, line):
        def _parse_lists(iterator, ls):
            try:
                token = self.skip_blank(iterator)
                if token.tp == Token.TYPE_WORD:
                    ls.append(token.value)
                    token = self.skip_blank(iterator)
                    if token.tp == Token.TYPE_COMMA:
                        _parse_lists(iterator, ls)
            except StopIteration:
                pass

        res = []
        _parse_lists(line, res)
        return res

    def parse_line(self, line):
        buf = []
        try:
            while True:
                token = next(line)
                if token.tp == Token.TYPE_WORD:
                    buf.append(token.value)
                else:
                    buf.append(self.__tp_map[token.tp])
        except StopIteration:
            pass

        return ''.join(buf)

    def skip_blank(self, line):
        v = next(line)
        while v.tp in self.__blank:
            v = next(line)

        return v

    __meta_map = {
        'owner': {
            'parser.py': parse_lists,
            'multiple': False
        },
        'date': {
            'parser.py': parse_word,
            'multiple': False
        },
        'describe': {
            'parser.py': parse_line,
            'multiple': False
        },
        'requirement': {
            'parser.py': parse_lists,
            'multiple': False
        },
        'developer': {
            'parser.py': parse_lists,
            'multiple': False
        },
        'testpoint': {
            'parser.py': parse_line,
            'multiple': True
        },
        'dts': {
            'parser.py': parse_lists,
            'multiple': True
        }
    }






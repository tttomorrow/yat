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

from .errors import LexError


class Token:
    TOKEN_LBRACE = '{'
    TOKEN_RBRACE = '}'
    TOKEN_QUOTE = "'"
    TOKEN_LINE_COMMENT = '#'
    TOKEN_SEMICOLON = ';'

    MOLD_SYMBOL = 1
    MOLD_WORD = 2
    MOLD_QUOTE_VALUE = 3

    def __init__(self, mold, value):
        self.mold = mold
        self.value = value

    def __repr__(self):
        return 'Token {{ mold: {}, value: {} }}'.format(self.mold, self.value)


class Lex:
    BLANKS = (' ', '\t', '\r', '\n')
    WORD_SPLIT = (
        ' ',
        '\t',
        '\r',
        '\n',
        Token.TOKEN_LINE_COMMENT,
        Token.TOKEN_QUOTE,
        Token.TOKEN_RBRACE,
        Token.TOKEN_LBRACE,
        Token.TOKEN_SEMICOLON,
        ''
    )

    ESCAPE_CHAR = {
        '\\': '\\',
        "'": "'"
    }

    def __init__(self, stream):
        self.stream = stream

    def lex(self):

        tokens = []
        ch = self.skip_blank()

        while len(ch) > 0:
            need_next = True
            if ch == Token.TOKEN_QUOTE:
                tokens.append(self.lex_quoted_value())
            elif ch == Token.TOKEN_LBRACE:
                tokens.append(Token(Token.MOLD_SYMBOL, Token.TOKEN_LBRACE))
            elif ch == Token.TOKEN_RBRACE:
                tokens.append(Token(Token.MOLD_SYMBOL, Token.TOKEN_RBRACE))
            elif ch == Token.TOKEN_LINE_COMMENT:
                self.lex_line_comment()
            elif ch == Token.TOKEN_SEMICOLON:
                tokens.append(Token(Token.MOLD_SYMBOL, Token.TOKEN_SEMICOLON))
            else:
                ch, word = self.lex_word(ch)
                tokens.append(word)
                if ch not in self.BLANKS:
                    need_next = False

            if need_next:
                ch = self.skip_blank()

        return tokens

    def lex_quoted_value(self):
        buf = []
        ch = self.read_next()
        while ch != Token.TOKEN_QUOTE:
            if len(ch) <= 0:
                raise LexError('uncompleted quote value found')

            if ch == '\\':
                ch = self.read_next()
                if ch in self.ESCAPE_CHAR:
                    ch = self.ESCAPE_CHAR[ch]
                else:
                    raise LexError('unknown escape character found \\%s' % ch)

            buf.append(ch)
            ch = self.read_next()

        return Token(Token.MOLD_QUOTE_VALUE, ''.join(buf))

    def lex_word(self, first):
        buf = [first]
        ch = self.read_next()
        while ch not in self.WORD_SPLIT:
            buf.append(ch)
            ch = self.read_next()

        return ch, Token(Token.MOLD_WORD, ''.join(buf))

    def lex_line_comment(self):
        ch = self.read_next()
        while len(ch) > 0 and ch != '\n':
            ch = self.read_next()

    def skip_blank(self):
        ch = self.read_next()
        while ch in self.BLANKS:
            ch = self.read_next()

        return ch

    def read_next(self):
        return self.stream.read(1)

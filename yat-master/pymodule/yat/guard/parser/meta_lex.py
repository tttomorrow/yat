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

class Token:
    TYPE_WORD = 1
    TYPE_AT = 2
    TYPE_TAB = 3
    TYPE_COLON = 4
    TYPE_COMMA = 5
    TYPE_BLANK = 6
    TYPE_CR = 7
    TYPE_LF = 8

    __type_to_str = {
        TYPE_AT: '@',
        TYPE_TAB: '\\t',
        TYPE_COLON: ':',
        TYPE_COMMA: ',',
        TYPE_BLANK: ' ',
        TYPE_CR: '\\r',
        TYPE_LF: '\\n'
    }

    def __init__(self, tp, value=None):
        self.tp = tp
        self.value = value

    def __repr__(self):
        if self.value is None:
            value = self.__type_to_str.get(self.tp)
        else:
            value = self.value
        return 'Token(type=%d, value="%s")' % (self.tp, value)


class MetaLex:
    __lex_map = {
        ' ': Token(Token.TYPE_BLANK),
        '\t': Token(Token.TYPE_TAB),
        '@': Token(Token.TYPE_AT),
        ':': Token(Token.TYPE_COLON),
        ',': Token(Token.TYPE_COMMA),
        '\r': Token(Token.TYPE_CR),
        '\n': Token(Token.TYPE_LF)
    }

    def __init__(self, stream):
        self.stream = stream

    def read(self, n=1):
        return self.stream.read(n)

    def lex(self):
        line = []
        while True:
            ch = self.read()

            if len(ch) == 0:
                if len(line) > 0:
                    yield line
                    line = []
                else:
                    return
            else:
                if ch == '\r':
                    continue
                elif ch == '\n':
                    if len(line) > 0:
                        yield line
                        line = []
                    else:
                        continue
                elif ch in self.__lex_map:
                    line.append(self.__lex_map[ch])
                else:
                    word, symbol = self.lex_word(ch)
                    line.append(word)
                    if symbol:
                        if symbol.tp == Token.TYPE_LF:
                            yield line
                            line = []
                        elif symbol.tp == Token.TYPE_CR:
                            pass
                        else:
                            line.append(symbol)

    def lex_word(self, first):
        buf = [first]

        ch = self.read()
        while ch != '' and ch not in self.__lex_map:
            buf.append(ch)
            ch = self.read()

        return Token(Token.TYPE_WORD, ''.join(buf)), self.__lex_map.get(ch)

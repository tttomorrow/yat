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

from .errors import ParseError
from .lex import Lex
from .lex import Token


class BlockNode:
    def __init__(self, name):
        self.name = name
        self.sub_blocks = []


class ActionNode:
    def __init__(self, name, params=None):
        if params is None:
            params = []
        self.name = name
        self.params = params


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        tokens = Lex(self.stream).lex()
        return self.parse_block(iter(tokens))

    def parse_block(self, iterator, name=None):
        if name is None:
            token = self.next_token(iterator)
            if token is None:
                raise ParseError('parse block: expect word, but EOF found')
            elif token.mold == Token.MOLD_WORD:
                return self.parse_block_with_name(iterator, token.value)
            else:
                raise ParseError('parse block: expect a word, but found %s' % token)
        else:
            return self.parse_block_with_name(iterator, name)

    def parse_block_with_name(self, iterator, name):
        block = BlockNode(name)
        token = self.next_token(iterator)
        if token is None:
            raise ParseError('parse block: expect {, but EOF found')
        elif token.mold == Token.MOLD_SYMBOL and token.value == Token.TOKEN_LBRACE:
            blocks = self.parse_block_body(iterator)
        else:
            raise ParseError('parse block: expect a left brace, but found %s' % token)

        block.sub_blocks = blocks

        return block

    def parse_block_body(self, iterator):
        token = self.next_token(iterator)
        if token is None:
            raise ParseError('parse block body: uncompleted block body')

        blocks = []

        while token.value != Token.TOKEN_RBRACE:
            if token.mold == Token.MOLD_WORD:
                if token.value in ('run', 'suite'):
                    blocks.append(self.parse_action(token.value, iterator))
                else:
                    blocks.append(self.parse_block(iterator, token.value))
            else:
                raise ParseError('parse block body: expect work, but found %s' % token)

            token = self.next_token(iterator)

        return blocks

    def parse_action(self, name, iterator):
        token = self.next_token(iterator)
        if token is None:
            raise ParseError('parse action: expect ;, but found EOF')

        params = []
        while token.value != Token.TOKEN_SEMICOLON:
            params.append(token.value)
            token = self.next_token(iterator)
            if token is None:
                raise ParseError('parse action: expect ;, but found EOF')

        return ActionNode(name, params)

    def next_token(self, iterator):
        try:
            return next(iterator)
        except StopIteration:
            return None

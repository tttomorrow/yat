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
from .errors import ParserError
from .reader import PlainReader


class PlainNode:
    def __init__(self, id, name, level, **attrs):
        self.id = id
        self.name = name
        self.level = level
        self.attrs = attrs
        self.child = []

    @property
    def left(self):
        return self.child[0]

    @property
    def right(self):
        return self.child[1]

    def add_child(self, child):
        if not isinstance(child, (PlainNode,)):
            raise RuntimeError("not a valid child node")
        self.child.append(child)

    def __getattr__(self, item):
        return self.attrs[item]


class PlainTree:
    def __init__(self, tree):
        self.tree = tree


class PlainParser:
    def __init__(self, content):
        self.reader = PlainReader(content)
        self._header = None

    def parse(self):
        self._parse_header()
        tree = self._parse_body()
        self._parse_predicate()

        return PlainTree(tree)

    def _parse_header(self):
        self.reader.skip_line()
        self._header = [item.strip(' ') for item in self.reader.next_line().strip('|').split('|')]
        if self._header[0] != 'Id':
            raise ParserError('Expect Id header at index 0')
        if self._header[1] != 'Description':
            raise ParserError('Expect Description header at index 1')
        self.reader.skip_line()

    def _parse_body(self):
        root = PlainNode(-1, 'root', -1)
        self._parse_body_tree(root)
        self.reader.skip_line()
        return root

    def _parse_body_tree(self, node):
        pre_node = None
        while self.reader.has_next():
            line = self.reader.top_line()
            if line.startswith('----'):
                break
            row = line.strip('|').split('|')
            node_id = int(row[0].strip(' '))
            node_name = row[1].strip(' ')
            node_level = self._get_level(row[1])

            new_node = PlainNode(node_id, node_name, node_level)
            if new_node.level == node.level + 1:
                self.reader.next_line()
                node.add_child(new_node)
                pre_node = new_node
            elif new_node.level == node.level + 2:
                self._parse_body_tree(pre_node)
            elif new_node.level <= node.level:
                break
            else:
                raise ParserError("expect sub-node")

        return node

    def _parse_predicate(self):
        pass

    @staticmethod
    def _get_level(row_item):
        counter = 0
        for it in row_item:
            if it == ' ':
                counter += 1
            else:
                break

        return int((counter - 1) / 2)

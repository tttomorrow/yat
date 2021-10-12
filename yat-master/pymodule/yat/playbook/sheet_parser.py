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

import re

import xlrd

from .errors import PlaybookError

REQUIRE_INDEX = -1
OPTION_INDEX = -2


class NoOrderHeaderContext:
    def __init__(self, names, index):
        self.names = names
        self.index = index

    def _get_index(self, name):
        v = self.index[name]
        if v == REQUIRE_INDEX:
            PlaybookError("Require index with name %s is not exists" % name)
        elif v == OPTION_INDEX:
            return None
        return v

    def __getattr__(self, item):
        return self._get_index(item)

    def __getitem__(self, item):
        return self._get_index(item)


class NoOrderHeaderParser:
    def __init__(self, ctx, header):
        self.ctx = ctx
        self.header = header
        self.name2inner = self._make_name2inner()
        self.inner2name = self._make_inner2name()
        self.require_count = self._make_require_count()

    def parse(self):
        names = []
        for cell in self.header:
            if len(cell.value) > 0:
                names.append(cell.value)
            else:
                break

        count = len(names)
        if count < self.require_count:
            raise PlaybookError("Playbook sheet require columns count >= %d" % self.require_count)

        name_index_map = self._make_inner_ctx()

        for index, name in enumerate(names):
            inner_name = self.name2inner.get(name)
            if inner_name:
                name_index_map[inner_name] = index

        for k, v in name_index_map.items():
            if v == REQUIRE_INDEX:
                raise PlaybookError("Require column with name %s" % self.inner2name[k].encode('utf-8'))

        return NoOrderHeaderContext(names, name_index_map)

    def _make_ctx(self, k, v):
        res = {}
        for c in self.ctx:
            res[c[k]] = c[v]
        return res

    def _make_name2inner(self):
        return self._make_ctx(0, 1)

    def _make_inner2name(self):
        return self._make_ctx(1, 0)

    def _make_inner_ctx(self):
        return self._make_ctx(1, 2)

    def _make_require_count(self):
        count = 0
        for c in self.ctx:
            if c[2] == REQUIRE_INDEX:
                count += 1
        return count


class TestCase:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.case_name = kwargs['case_name']
        self.comment = kwargs.get('comment')
        self.setup = kwargs.get('setup')
        self.cleanup = kwargs.get('cleanup')
        self.case = kwargs.get('case')
        self.case_expect = kwargs.get('case_expect')
        self.auto = kwargs.get('auto')
        self.type = kwargs.get('type')
        self.sheet = kwargs.get("sheet")
        self.row = kwargs.get("row")
        self.expect_index = kwargs.get("expect_index")
        self.result_index = kwargs.get("result_index")
        self.output_index = kwargs.get("output_index")

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "TestCase { name: %s, auto: %s, type: %s, sheet: %s, row: %d, expect_index: %d }" \
               % (self.name, self.auto, self.type, self.sheet, self.row, self.expect_index)


class PlaybookConfigure:
    _config_ctx = [
        ('sheet', 'sheet', REQUIRE_INDEX),
        ('execute', 'run', REQUIRE_INDEX),
    ]

    _macro_ctx = [
        ('macro', 'macro', REQUIRE_INDEX),
        ('value', 'value', REQUIRE_INDEX)
    ]

    def __init__(self, book, start_sheet):
        self.book = book
        self.sheet_enabled = []
        self.all_sheet = []
        self.start_sheet = start_sheet
        self.macros = {}

    def parse(self):
        self._parse_schedule()
        self._parse_macros()

    def _parse_schedule(self):
        names = self.book.sheet_names()
        sheet = None
        if 'configure' in names:
            sheet = self.book.sheet_by_name('configure')
        if sheet is None:
            self.sheet_enabled = names[self.start_sheet:]
            self.all_sheet = self.sheet_enabled
        else:
            self._parse_schedule_sheet(sheet)

    def _parse_macros(self):
        names = self.book.sheet_names()
        sheet = None
        if 'macros' in names:
            sheet = self.book.sheet_by_name('macros')

        if sheet is not None:
            self._parse_macros_sheet(sheet)

    def _parse_macros_sheet(self, sheet):
        ctx = NoOrderHeaderParser(self._macro_ctx, sheet.row_slice(0, 0)).parse()
        macro_index = ctx.index['macro']
        value_index = ctx.index['value']
        count = len(ctx.names)

        for row_idx in range(1, sheet.nrows):
            row = sheet.row_slice(row_idx, 0, count)
            macro_name = row[macro_index].value
            macro_value = row[value_index].value
            self.macros[macro_name] = macro_value

    def _parse_schedule_sheet(self, sheet):
        ctx = NoOrderHeaderParser(self._config_ctx, sheet.row_slice(0, 0)).parse()
        sheet_index = ctx.index['sheet']
        run_index = ctx.index['run']
        count = len(ctx.names)

        for row_idx in range(1, sheet.nrows):
            row = sheet.row_slice(row_idx, 0, count)
            sheet_name = row[sheet_index].value
            run = row[run_index].value

            self.all_sheet.append(sheet_name)
            if run == 'Y':
                self.sheet_enabled.append(sheet_name)


class PlaybookParser:
    def __init__(self, **kwargs):
        playbook = kwargs['playbook']
        self.book = xlrd.open_workbook(playbook, encoding_override='UTF-8')
        self.start_sheet = kwargs.get('start_sheet', 1)
        self._playbook_ctx = None
        self.configure = PlaybookConfigure(self.book, self.start_sheet)
        self._opts = kwargs

    def sheets(self):
        self.configure.parse()
        for sheet_name in self.configure.sheet_enabled:
            sheet = self.book.sheet_by_name(sheet_name)
            yield PlaybookSheetParser(sheet, **self._opts)


class PlaybookSheetParser:
    _playbook_ctx = {
        'poc': [
            ('Test Case Name', 'case_name_index', REQUIRE_INDEX),
            ('Test Case Setup', 'setup_index', OPTION_INDEX),
            ('Test Case Cleanup', 'cleanup_index', OPTION_INDEX),
            ('Test Case Steps', 'case_index', REQUIRE_INDEX),
            ('Test Case Expected', 'case_expect_index', REQUIRE_INDEX),
            ('Test Case Output', 'case_output_index', OPTION_INDEX),
            ('Test Case Result', 'case_result_index', OPTION_INDEX),
            ('Test Case Automated', 'case_auto_index', OPTION_INDEX),
            ('Test Case Execute Type', 'case_type_index', OPTION_INDEX)
        ],
        'tmss': [
            ('Testcase_Number', 'case_name_index', REQUIRE_INDEX),
            ('Testcase_Pretreatment Condition', 'setup_index', OPTION_INDEX),
            ('Testcase Cleanup', 'cleanup_index', OPTION_INDEX),
            ('Testcase_Test Steps', 'case_index', REQUIRE_INDEX),
            ('Testcase_Expected Result', 'case_expect_index', REQUIRE_INDEX),
            ('Testcase_Output', 'case_output_index', OPTION_INDEX),
            ('Testcase_Result', 'case_result_index', OPTION_INDEX),
            ('Testcase_Automated', 'case_auto_index', OPTION_INDEX),
            ('Testcase Execute Type', 'case_type_index', OPTION_INDEX)
        ]
    }

    @staticmethod
    def _escape_comment(comment):
        return comment.replace("\\", "\\\\").replace("}", "\\}")

    def __init__(self, sheet, **kwargs):
        self.sheet = sheet
        self.sheet_name = self.sheet.name
        self.is_parse_comment = kwargs.get('parse_comment', False)
        self.playbook_schema = kwargs.get('playbook_schema', 'tmss')

    def cases(self):
        header = self._parse_header(self.sheet.row_slice(0, 0))

        for row_idx in range(1, self.sheet.nrows):
            yield self._parse_one_case(
                self.sheet.name,
                header,
                self.sheet.row_slice(row_idx, 0, len(header.names)),
                row_idx
            )

    def _parse_header(self, header):
        return NoOrderHeaderParser(self._playbook_ctx[self.playbook_schema], header).parse()

    @staticmethod
    def _get_value(row, index):
        if index is None:
            return None
        else:
            return row[index].value

    def _parse_one_case(self, sheet_name, header, row, row_idx):
        setup = self._get_value(row, header.setup_index)
        cleanup = self._get_value(row, header.cleanup_index)
        case = self._get_value(row, header.case_index)
        case_expect = self._get_value(row, header.case_expect_index)
        name = self._get_value(row, header.case_name_index)
        auto = self._get_value(row, header.case_auto_index)
        case_type = self._get_value(row, header.case_type_index)

        if auto is None or auto.upper() in ('Y', 'TRUE', ''):
            auto = True
        elif auto.upper() in ('N', 'FALSE'):
            auto = False
        else:
            raise PlaybookError("test case auto execute column must be Y/N or TRUE/FALSE")

        if case_type is None or case_type == '':
            case_type = 'unit.sql'

        case_type = case_type.lower()
        if case_type not in ('unit.sql', 'z.sql', 'sh', ):
            raise PlaybookError("test case type only allow unit.sql/z.sql/sh")

        if re.match(r'^[a-zA-Z0-9_-]+$', name) is None:
            raise PlaybookError("test case name %s must match regex [a-zA-Z0-9_-]+" % name)

        if self.is_parse_comment:
            comment = self._parse_comment(header, row)
        else:
            comment = None

        return TestCase(
            name='%s/%s' % (sheet_name, name),
            case_name=name,
            setup=setup,
            cleanup=cleanup,
            case=case,
            case_expect=case_expect,
            comment=comment,
            auto=auto,
            type=case_type,
            sheet=sheet_name,
            expect_index=header.case_expect_index,
            row=row_idx,
            result_index=header.case_result_index,
            output_index=header.case_output_index
        )

    def _parse_comment(self, header, row):
        skip_index = {
            header.setup_index,
            header.cleanup_index,
            header.case_index,
            header.case_expect_index,
            header.case_name_index
        }

        buf = []

        for i, v in enumerate(row):
            if i not in skip_index:
                buf.append("%s: %s" % (header.names[i], self._escape_comment(v.value)))

        return "\n".join(buf)

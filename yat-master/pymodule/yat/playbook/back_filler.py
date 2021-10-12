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

import json
import os

from .sheet_parser import PlaybookParser


class PlaybookBackFiller:
    def __init__(self, **kwargs):
        self.playbook = kwargs['playbook']
        self.suite_dir = kwargs['test_suite']
        self.test_case_dir = kwargs.get('test_case_dir', 'testcase')
        self.conf_dir = kwargs.get('conf_dir', 'conf')
        self.expect_dir = kwargs.get('expect_dir', 'expect')
        self.result_dir = kwargs.get('result_dir', 'result')
        self.schedule_dir = kwargs.get('schedule_dir', 'schedule')
        self.force = kwargs.get('force', False)
        self.verbose = kwargs.get('verbose', False)
        self.parser = PlaybookParser(**kwargs)
        self.openpyxl = __import__('openpyxl')

    @staticmethod
    def read_file(path):
        with open(path) as infile:
            return infile.read()

    def get_output_playbook(self, ext2):
        name, ext = os.path.splitext(self.playbook)
        if self.force:
            back_file = self.playbook
        else:
            back_file = "%s.%s%s" % (name, ext2, ext)

        return back_file

    def read_bare_result(self, case):
        case_path = os.path.join(self.suite_dir, self.result_dir, case.name + ".bare")
        if os.path.exists(case_path):
            return self.read_file(case_path)

    def read_result(self, case):
        case_path = os.path.join(self.suite_dir, self.result_dir, case.name)
        if os.path.exists(case_path):
            return self.read_file(case_path)

    def back_fill_content(self, data_source, ext2):
        book = self.openpyxl.load_workbook(self.playbook)

        for sheet in self.parser.sheets():
            for case in sheet.cases():
                sheet = book[case.sheet]

                for index, data in data_source(case):
                    column = getattr(case, index)
                    if column is None:
                        if self.verbose:
                            print('back fill [%s]-[%s] ... failed' % (case.sheet, case.name))
                    else:
                        column += 1
                        if data is not None:
                            sheet.cell(case.row + 1, column).value = data
                            if self.verbose:
                                print('back fill [%s]-[%s]-[%d] ... ok' % (case.sheet, case.name, column))
                        else:
                            if self.verbose:
                                print('back fill [%s]-[%s]-[%d] ... failed' % (case.sheet, case.name, column))

        book.save(self.get_output_playbook(ext2))


class PlaybookExpectBackFiller(PlaybookBackFiller):
    def __init__(self, **kwargs):
        super(PlaybookExpectBackFiller, self).__init__(**kwargs)

    def back_fill(self):
        def data_source(case):
            if case.auto:
                if case.type == 'unit.sql':
                    yield 'expect_index', self.read_bare_result(case)
                else:
                    yield 'expect_index', self.read_result(case)

        self.back_fill_content(data_source, 'back-fill')


class PlaybookResultBackFiller(PlaybookBackFiller):
    def __init__(self, **kwargs):
        super(PlaybookResultBackFiller, self).__init__(**kwargs)

    def back_fill(self):
        result = self.parse_result()

        def data_source(case):
            if case.auto:
                if case.type == 'unit.sql':
                    yield 'output_index', self.read_bare_result(case)
                    yield 'result_index', result[case.name]
                else:
                    yield 'output_index', self.read_result(case)
                    yield 'result_index', result[case.name]

        self.back_fill_content(data_source, 'result')

    def parse_result(self):
        result_file = os.path.join(self.suite_dir, 'log', 'yat.json')
        with open(result_file) as fresult:
            result = json.load(fresult)

            res = {}
            for subSuite in result['subSuites']:
                for results in subSuite['results']:
                    for case in results['cases']:
                        res[case['case']] = case['result']

            return res

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

import os
import stat
from .errors import PlaybookError
from .sheet_parser import PlaybookParser


class Schedule:
    def __init__(self):
        self.schedule = []

    def add_test_case(self, case, **kwargs):
        self.schedule.append((case, kwargs,))

    def save(self, path):
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(path, flags, mode), 'w') as output:
            for case in self.schedule:
                props = []
                for k, v in case[1].items():
                    props.append('%s=%s' % (k, v))
                if len(props) > 0:
                    prop_str = '(%s)' % ','.join(props)
                else:
                    prop_str = ''
                output.write('group: \'%s\'%s\n' % (case[0].encode('utf-8'), prop_str))


class Macros:
    def __init__(self, macros):
        self.macros = macros

    def save(self, path):
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(path, flags, mode), 'w') as output:
            for k, v in self.macros.items():
                k = str(k)
                v = str(v)
                output.write('%s: \'%s\'\n' % (k, v))


class CaseGenerator:
    def __init__(self, case, suite_dir, scheduler, case_dir='testcase', expect_dir='expect'):
        self.case = case
        self.suite_dir = suite_dir
        self.scheduler = scheduler
        self.case_dir = case_dir
        self.expect_dir = expect_dir

    def generate(self):
        raise RuntimeError("must implement CaseGenerator generate method")

    @staticmethod
    def make_parent(path):
        parent, _ = os.path.split(path)
        if not os.path.exists(parent):
            os.makedirs(parent)

    def case_is_empty(self):
        return len(self.case.case) <= 0


class UnitSqlCaseGenerator(CaseGenerator):
    def __init__(self, case, suite_dir, scheduler):
        super(UnitSqlCaseGenerator, self).__init__(case, suite_dir, scheduler)

    def generate(self):
        if self.case_is_empty():
            return
        case_path = os.path.join(self.suite_dir, self.case_dir, self.case.name + ".unit.sql")
        self.make_parent(case_path)

        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(case_path, flags, mode), 'w') as stream:
            self._gen_comment(stream)
            self._gen_setup(stream)
            self._gen_test_case(stream)
            self._gen_cleanup(stream)

        self.scheduler.add_test_case(self.case.name)

    def _gen_comment(self, stream):
        # generate comment
        if stream is None:
            return
        self._gen_block_common(stream, '#comment', self.case.comment)

    def _gen_setup(self, stream):
        if stream is None:
            return
        self._gen_block_common(stream, '#setup', self.case.setup)

    def _gen_cleanup(self, stream):
        if stream is None:
            return
        self._gen_block_common(stream, '#cleanup', self.case.cleanup)

    def _gen_test_case(self, stream):
        self._gen_block_common(stream, '#test', self.case.case)
        if self.case.case_expect is not None:
            self._gen_block_common(stream, '#expect', self.case.case_expect)

    def _gen_block_common(self, stream, block_name, content):
        if content is None:
            return
        content_lines = ["    %s" % line.encode(encoding='utf-8') for line in content.splitlines()]
        stream.write("%s\n{\n%s\n}\n" % (block_name, "\n".join(content_lines)))


class NormalCaseGenerator(CaseGenerator):
    def __init__(self, case, suite_dir, scheduler, case_type):
        super(NormalCaseGenerator, self).__init__(case, suite_dir, scheduler)
        self.case_type = case_type

    def generate(self):
        if self.case_is_empty():
            return
        self._gen_setup()
        self._gen_test_case()
        self._gen_cleanup()

    def _gen_setup(self):
        self._gen_one_case(self.case.setup, "_setup")
        self.scheduler.add_test_case(self.case.name + "_setup", valid='false')

    def _gen_test_case(self):
        self._gen_one_case(self.case.case, "")
        self.scheduler.add_test_case(self.case.name)
        expect_path = os.path.join(self.suite_dir, self.expect_dir, self.case.name)
        self.make_parent(expect_path)
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(expect_path, flags, mode), 'w') as expect_out:
            expect_out.write(self.case.case_expect.encode('utf-8'))

    def _gen_cleanup(self):
        self._gen_one_case(self.case.cleanup, "_cleanup")
        self.scheduler.add_test_case(self.case.name + "_cleanup", valid='false')

    def _gen_one_case(self, content, suffix):
        case_path = os.path.join(self.suite_dir, self.case_dir, self.case.name + suffix + self.case_type)
        self.make_parent(case_path)
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(case_path, flags, mode), 'w') as output:
            output.write(content.encode('utf-8'))


class SuiteGenerator:
    def __init__(self, **kwargs):
        self.playbook = kwargs['playbook']
        self.suite_dir = kwargs['test_suite']
        self.test_case_dir = kwargs.get('test_case_dir', 'testcase')
        self.conf_dir = kwargs.get('conf_dir', 'conf')
        self.schedule_dir = kwargs.get('schedule_dir', 'schedule')
        self.parser = PlaybookParser(**kwargs)
        self.schedule = Schedule()

    def generate(self):
        for sheet in self.parser.sheets():
            for case in sheet.cases():
                if not case.auto:
                    continue
                if case.type == 'unit.sql':
                    UnitSqlCaseGenerator(case, self.suite_dir, self.schedule).generate()
                elif case.type == 'z.sql':
                    NormalCaseGenerator(case, self.suite_dir, self.schedule, '.z.sql').generate()
                elif case.type == 'sh':
                    NormalCaseGenerator(case, self.suite_dir, self.schedule, '.sh').generate()
                else:
                    raise PlaybookError('found not support test case type %s' % case.type)

        self.schedule.save(os.path.join(self.suite_dir, self.schedule_dir, 'schedule.schd'))
        macros = self.parser.configure.macros
        if len(macros) > 0:
            Macros(macros).save(os.path.join(self.suite_dir, self.conf_dir, 'macro.yml'))

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
import os
from yat.common.shell import run_shell
from yat.common.utils import rmtree, chmod
from yat.const import YAT_HOME_APP, YAT_HOME_SCRIPT, YAT_HOME_PYTHON
from yat.errors import YatError
from .diff import collect_diff_file
from .permission import suite_permission
from .workdir import WorkDir
from .yat_output import make_yat_output


class YatCommand:
    """
    running real yat
    :param opts: options pass from command line
    """
    _make_ctx = {
        'test_dir': '-d',
        'schedule': '-s',
        'mode': '-m',
        'left': '-l',
        'right': '-r',
        'target': '-t',
        'no_echo': '--no-echo',
        'panic': '--panic',
        'suite_serial': '--serial',
        'version': '--version',
        'configure': '-f',
        'nodes': '-n',
        'macro': '-i',
        'macro_file': '-e',
        'lib_path': '--lib-path',
        'daemon': '--daemon',
        'color': '--color',
        'bare': '--bare',
        'width': '--width',
        'cases': '--cases',
        'action': '--action',
        'timeout': '--timeout',
        'expect': '--expect'
    }

    def __init__(self, **opts):
        self.opts = opts
        self.prefix_cmd = ""
        self.jvm_opts = opts.get('jvm_opts', [])
        self.work_dir = None

    def run(self):
        """
        do prepare, run yat and clean up works
        """
        self.work_dir = WorkDir(os.path.abspath(self.opts['test_dir']))
        test_dir = self.work_dir.get_work_dir()

        if self.opts['lib_path']:
            self.opts['lib_path'] = os.path.abspath(self.opts['lib_path'])

        if not is_test_suite(test_dir):
            raise YatError("given test suite path: %s seems not a legal test suite directory" % test_dir)

        if self.opts['output']:
            self.opts['output'] = os.path.abspath(self.opts['output'])
            make_yat_output(test_dir, self.opts['output'], force=self.opts['force'])
            self.opts['test_dir'] = self.opts['output']
            self.work_dir = WorkDir(os.path.abspath(self.opts['test_dir']))

        return self._run_yat_with_init()

    def _run_yat_with_init(self):
        test_dir = self.work_dir.get_work_dir()
        try:
            if self.opts['mode'] != 'diff' and not self.opts['no_clean']:
                self._suite_clean()

            self._suite_env()
            self._suite_init()
            suite_permission(test_dir, True)
            return self._run_yat()
        finally:
            suite_permission(test_dir)
            collect_diff_file(test_dir)

    def _run_yat(self):
        """
        do real work of run yat
        """
        test_dir = self.opts['test_dir']
        if self.opts.get('debug'):
            cmd = ['java', '-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005']
        else:
            cmd = ['java']
        if self.opts.get('prefix_shell'):
            self.set_prefix_cmd(self.opts.get('prefix_shell'))
        cmd.extend(self.jvm_opts)
        cmd.extend(['-jar', self._get_app_jar()])
        cmd.extend(self._make_yat_command(**self.opts))

        if len(self.prefix_cmd) > 0:
            prefix = self.prefix_cmd
        else:
            prefix = self.work_dir.get_yat_env()

        real_cmd = ". %s; cd %s; %s" % (prefix, test_dir, ' '.join((str(v) for v in cmd)))
        ret, _ = run_shell(real_cmd, pipe=False)
        return ret

    def version(self):
        _, out = run_shell(['java', '-jar', self._get_app_jar(), '--version'], shell=False)
        return out.strip('\r\n\t ')

    def set_prefix_cmd(self, cmd):
        self.prefix_cmd = cmd
        return self

    def _suite_init(self):
        self.mkdirs(self.work_dir.output.get_log_dir())
        self.mkdirs(self.work_dir.output.get_result_dir())
        self.mkdirs(self.work_dir.output.get_temp_dir())

    def _suite_clean(self):
        self.clean_tree(self.work_dir.output.get_log_dir())
        self.clean_tree(self.work_dir.output.get_result_dir())
        self.clean_tree(self.work_dir.output.get_temp_dir())

    def _suite_env(self):
        python_path = self.work_dir.get_python_dir()

        if 'PYTHONPATH' in os.environ:
            os.environ['PYTHONPATH'] = '%s:%s:%s' % (python_path, YAT_HOME_PYTHON, os.environ['PYTHONPATH'])
        else:
            os.environ['PYTHONPATH'] = '%s:%s' % (python_path, YAT_HOME_PYTHON)

        # for shell script plugin
        script_path = self.work_dir.get_script_dir()
        os.environ['PATH'] = '%s:%s:%s' % (script_path, YAT_HOME_SCRIPT, os.environ['PATH'])

        # ld library
        lib_path = self.work_dir.get_lib_dir()
        if 'LD_LIBRARY_PATH' in os.environ:
            os.environ['LD_LIBRARY_PATH'] = '{}:{}'.format(lib_path, os.environ['LD_LIBRARY_PATH'])
        else:
            os.environ['LD_LIBRARY_PATH'] = lib_path

    @staticmethod
    def _get_app_jar():
        for name in os.listdir(YAT_HOME_APP):
            if re.match(r'yat-[0-9]+\.[0-9]+\.[0-9]+', name):
                return os.path.join(YAT_HOME_APP, name)
        return None

    def _make_yat_command(self, **opts):
        """
        make the real command to run yat
        """
        cmd = []
        for name, opt in self._make_ctx.items():
            value = opts.get(name)
            if value is not None:
                if isinstance(value, bool):
                    if value:
                        cmd.append(opt)
                elif isinstance(value, (list, tuple)):
                    for v in value:
                        cmd.append(opt)
                        cmd.append(v)
                else:
                    cmd.append(opt)
                    cmd.append(value)
        return cmd

    @classmethod
    def clean_tree(cls, clean_dir):
        """
        cleanup result directory
        :param clean_dir: the result directory
        """
        if os.path.exists(clean_dir):
            chmod(clean_dir, 0o700, True)
            rmtree(clean_dir)

    @classmethod
    def mkdirs(cls, target_dir):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)


def is_test_suite(suite_dir):
    """
    is the directory legal
    :param suite_dir:
    :return:
    """
    work_dir = WorkDir(suite_dir)
    test_case_dir = work_dir.get_test_case_dir()
    test_conf_dir = work_dir.get_conf_dir()
    test_schedule_dir = work_dir.get_schedule_dir()

    return os.path.exists(test_case_dir) and os.path.exists(test_conf_dir) and os.path.exists(test_schedule_dir)

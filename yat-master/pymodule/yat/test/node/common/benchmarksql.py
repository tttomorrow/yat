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
import shutil
import stat
from subprocess import Popen, STDOUT
from yat.test.node.plugins import plugin


def _is_success(log, judge):
    with open(log, 'r') as check:
        for line in check:
            judge(line)


def _sub_process(cmds, log_path, wait=True, timeout=None):
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    with os.fdopen(os.open(log_path, flags, mode), 'w') as out:
        for cmd in cmds:
            proc = Popen(cmd, stderr=STDOUT, stdout=out)
        proc.poll()
    if wait:
        proc.wait(timeout)

    return proc


class BenchmarkSql:
    default_conf = {
        'db': 'oracle',
        'driver': 'com.huawei.gauss.jdbc.ZenithDriver',
        'conn': 'jdbc:zenith:@127.0.0.1:1611',
        'user': 'benchmarksql',
        'password': '',
        'warehouses': 1,
        'loadWorkers': 5,
        'terminals': 10,

        'runTxnsPerTerminal': 0,
        'runMins': 5,
        'limitTxnsPerMin': 0,
        'terminalWarehouseFixed': 'true',

        'newOrderWeight': 45,
        'paymentWeight': 43,
        'orderStatusWeight': 4,
        'deliveryWeight': 4,
        'stockLevelWeight': 4,

        'resultDirectory': 'my_result_%tY-%tm-%td_%tH%tM%tS',
        'osCollectorScript': './misc/os_collector_linux.py',
        'osCollectorInterval': 1
    }
    _run_dir_name = "run"
    _conf_path = "props.gs"
    _build_cmd_path = "runDatabaseBuild.sh"
    _run_cmd_path = "runBenchmark.sh"
    _destroy_cmd_path = "runDatabaseDestroy.sh"
    _log_build_path = "benchmarksql.build.{}.log"
    _log_run_path = "benchmarksql.run.{}.log"
    _log_destroy_path = "benchmarksql.destroy.{}.log"

    def __init__(self, root_path, output_path, id=0, **conf):
        self.root_path = root_path
        self.output_path = output_path
        self.run_path = os.path.join(self.output_path, self._run_dir_name)
        self._make_output_path()
        self._make_executable()
        self._write_conf(conf)
        self.log_build_path = self._real_path(self._log_build_path.format(id))
        self.log_run_path = self._real_path(self._log_run_path.format(id))
        self.log_destroy_path = self._real_path(self._log_destroy_path.format(id))

    def _make_output_path(self):
        if not os.path.exists(self.output_path):
            shutil.copytree(self.root_path, self.output_path)
            for root, dirs, files in os.walk(self.output_path):
                for directory in dirs:
                    real_path = os.path.join(root, directory)
                    os.chmod(real_path, 0o700)
                for sub_file in files:
                    real_path = os.path.join(root, sub_file)
                    os.chmod(real_path, 0o600)

    def _real_path(self, path):
        return os.path.join(self.run_path, path)

    def _make_executable(self):
        for root, _, files in os.walk(self.run_path):
            for f in files:
                if f.endswith(".sh"):
                    os.chmod(os.path.join(root, f), 0o700)

    def _write_conf(self, conf):
        real_conf = {}
        for key, value in self.default_conf.items():
            real_conf[key] = value
        for key, value in conf.items():
            real_conf[key] = value

        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        with os.fdopen(os.open(self._real_path(self._conf_path), flags, mode), 'w') as conf_file:
            for key, value in real_conf.items():
                conf_file.write("{}={}\n".format(key, value))

    def is_build_success(self):
        def _judge(line):
            if 'errorCode' in line:
                raise AssertionError("BenchmarkSql Build Failed")

        _is_success(self.log_build_path, _judge)

    def is_run_success(self):
        def _judge(line):
            if 'Error' in line:
                raise AssertionError("BenchmarkSql Run Failed")

        _is_success(self.log_run_path, _judge)

    def build(self, timeout=None):
        """
        run benchmarksql database build action
        :param timeout: timeout to wait subprocess(benchmarksql process)
        :exception: RaiseException if action is failed
        """
        cmd_arry = [["cd" , self.run_path] , ["./"+self._build_cmd_path , self._conf_path]] 
        _sub_process(cmd_arry , self.log_build_path , timeout=timeout)
        self.is_build_success()

    def run(self, timeout=None):
        """
       run benchmarksql business
       :param timeout: timeout to wait subprocess(benchmarksql process)
       :exception: RaiseException if action is failed
       """
        cmd_arry = [["cd" , self.run_path] , ["./"+self._run_cmd_path , self._conf_path]]
        _sub_process(cmd_arry , self.log_run_path , timeout=timeout)
        self.is_run_success()

    def run_background(self, timeout=None):
        cmd_arry = [["cd" , self.run_path] , ["./"+self._run_cmd_path , self._conf_path]]
        return BenchmarkSqlProcess(
            _sub_process(cmd_arry , self.log_run_path , timeout=timeout , wait=False), self)

    def destroy(self, timeout=None):
        """
       run benchmarksql database destroy action
       :param timeout: timeout to wait subprocess(benchmarksql process)
        """
        cmd_arry = [["cd" , self.run_path] , ["./"+self._destroy_cmd_path , self._conf_path]]
        _sub_process(cmd_arry , self.log_destroy_path , timeout=timeout)


class BenchmarkSqlProcess:
    def __init__(self, proc, bench):
        self.proc = proc
        self.bench = bench

    def poll(self):
        return self.proc.poll()

    def wait(self, timeout=None):
        """
        wait the sub process finished or timeout
        :param timeout:
        :exception:
            1. RaiseException when run action is failed
            2. TimeoutException when timeout for wait
        """
        self.proc.wait(timeout)
        self.bench.is_run_success()

    def kill(self):
        self.proc.kill()


@plugin('*')
def tpcc(self, root_path, output_path, id=0, **conf):
    return BenchmarkSql(root_path, output_path, id, **conf)

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

from yat.shell import Shell
from yat.test.node.result import ShellResult
from ..plugins import plugin

_shell = Shell()


class ZSql:
    def _build_zsql_cmd(self, sql=None, sql_file=None) -> str:
        cmd = ['zsql', '{0}/{1}@{2}:{3}'.format(
            self.user,
            self.password,
            self.host,
            self.port
        ), '-a']

        if sql is not None:
            cmd.extend(['-c', "'{}'".format(sql)])
        elif sql_file is not None:
            cmd.extend(['-f', "'{}'".format(sql_file)])
        else:
            raise RuntimeError("sql or sql_file should given")

        return ' '.join(cmd)

    def __init__(self, user, password, host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def execute(self, sql, *args, **kwargs) -> (int, str):
        return _shell.sh(self._build_zsql_cmd(sql=sql.format(*args, **kwargs)), shell=False)

    def execute_file(self, path) -> (int, str):
        return _shell.sh(self._build_zsql_cmd(sql_file=path), shell=False)


@plugin('zenith')
def zsql(self, sql, *args, **kwargs) -> ShellResult:
    code, out = ZSql(
        self.db_user, self.db_password, self.db_host, self.db_port).execute(sql=sql, *args, **kwargs)
    return ShellResult(out, code)


@plugin('zenith')
def fzsql(self, sql_file, *args, **kwargs) -> ShellResult:
    code, out = ZSql(
        self.db_user, self.db_password, self.db_host, self.db_port).execute_file(sql_file)
    return ShellResult(out, code)


def _key_val_cmd(cmd, **kwargs):
    opts = [cmd]
    for k, v in kwargs.items():
        if k.lower() == 'file':
            opts.append('{}="{}"'.format(k, str(v)))
        else:
            opts.append('{}={}'.format(k, str(v)))

    return ' '.join(opts)


@plugin('zenith')
def exp(self, **kwargs):
    return self.zsql(_key_val_cmd('EXP', **kwargs))


@plugin('zenith')
def imp(self, **kwargs):
    return self.zsql(_key_val_cmd("IMP", **kwargs))

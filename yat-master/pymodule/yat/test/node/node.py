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

from functools import partial

from yat import configure
from yat import db
from yat.common.utils import deprecated
from yat.shell import SSH
from yat.shell import Shell
from yat.test.data_generator import DataGenerator
from .plugins import get_plugins
from .result import ShellResult
from .result import SqlResult


class LazyResource:
    """
    lazy object wrapper

    class TheClass:
        def __init__(self):
            # do connection

        def close(self):
            # close connection

        def action(self):
            # do something

    obj = Lazy(lambda: TheClass())
    # the TheClass.__init__ is not call now
    obj.action()  # the TheClass.__init__ is called and action is called

    """

    def __init__(self, maker):
        self._maker = maker
        self._proxy = None

    def __getattr__(self, item):
        if self._proxy is None:
            self._proxy = self._maker()
        return getattr(self._proxy, item)

    def reset(self):
        """
        if the lazy object is used, closing it first, then make it invalid(None)
        """
        if self._proxy is not None:
            self._proxy.close()
            self._proxy = None

    def close(self):
        """
        closing the proxy only if the proxy is initialized
        :return:
        """
        if self._proxy is not None:
            self._proxy.close()


class Node:
    """
    Node operate interface, which contains:

    * shell command power by ssh
    * sql command
    * ssh scp
    * local shell
    * plugins methods
    """

    _kwargs_name_map = {
        'db_user': '{}_DB_USER',
        'db_password': '{}_DB_PASSWD',
        'db_host': '{}_DB_HOST',
        'db_port': '{}_DB_PORT',
        'db_type': '{}_DB_TYPE',
        'db_name': '{}_DB_NAME',
        'ssh_host': '{}_SSH_HOST',
        'ssh_port': '{}_SSH_PORT',
        'ssh_user': '{}_SSH_USER',
        'ssh_password': '{}_SSH_PASSWD',
    }

    def __init__(self, node=None, **kwargs):
        if node is None:
            self.name = 'default'
        else:
            self.name = node
        self._env_name = self.name.upper()
        self._init_conn_info(kwargs)
        self._load_plugin()
        self.ssh = LazyResource(lambda: SSH(self.ssh_user, self.ssh_password, self.ssh_host, self.ssh_port, **kwargs))
        self.db = LazyResource(
            lambda: db.get_db(self.db_user, self.db_password, self.db_host, self.db_port, self.db_type,
                              dbname=self.db_name, **kwargs))
        self.shell = LazyResource(lambda: Shell())

        self.lazy_map = {
            'ssh': self.ssh,
            'db': self.db,
            'shell': self.shell
        }
        self.db.autocommit = kwargs.get('autocommit', True)

    @property
    @deprecated
    def node(self):
        return self.name

    def _load_plugin(self):

        if self.db_type:
            self.plugins = get_plugins(self.db_type)
        else:
            self.plugins = {}

        self.plugins = {**get_plugins('*'), **self.plugins}

    def _get_attr(self, kwargs, name):
        if name in kwargs:
            return kwargs[name]
        elif name in self._kwargs_name_map:
            env_name = self._kwargs_name_map[name]
            return configure.get(env_name.format(self._env_name))
        raise KeyError('given key {} not exists'.format(name))

    def _init_conn_info(self, kwargs):
        self.db_user = self._get_attr(kwargs, 'db_user')
        self.db_password = self._get_attr(kwargs, 'db_password')
        self.db_host = self._get_attr(kwargs, 'db_host')
        self.db_port = self._get_attr(kwargs, 'db_port')
        self.db_type = self._get_attr(kwargs, 'db_type')
        self.db_name = self._get_attr(kwargs, 'db_name')

        self.ssh_host = self._get_attr(kwargs, 'ssh_host')
        self.ssh_port = self._get_attr(kwargs, 'ssh_port')
        self.ssh_user = self._get_attr(kwargs, 'ssh_user')
        self.ssh_password = self._get_attr(kwargs, 'ssh_password')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def reset(self, **kwargs):
        """
        reset all or the specific connections
        """
        if len(kwargs) == 0:
            for _, v in self.lazy_map.items():
                v.reset()
            return

        for k, v in kwargs.items():
            if k in self.lazy_map:
                if v:
                    self.lazy_map[k].reset()
            else:
                raise RuntimeError("unknown args " + k + " for re_init method")

    def sql(self, sql, *args) -> SqlResult:
        """
        execute a sql text with bind arguments

        :param sql: sql text to be execute
        :param args: the bind arguments for sql
        :return: SqlResult
        """
        try:
            res = self.db.execute_query(sql, *args)
            return SqlResult(result=res)
        except self.db.db_error as e:
            return SqlResult(error=str(e))

    def sh(self, cmd) -> ShellResult:
        """
        execute cmd with ssh2 protocol

        :param cmd: cmd text to be execute
        :return: ShellResult
        """
        code, msg = self.ssh.sh(cmd)
        return ShellResult(msg, code)

    def scp_get(self, _from, to):
        """
        copy file from remote with ssh2 protocol

        :param _from: remote file path
        :param to: local file path
        :return: true if success, else false
        """
        self.ssh.scp_get(_from, to)

    def scp_put(self, _from, to):
        """
        copy file to remote host with ssh2 protocol

        :param _from: local file path
        :param to: remote file path
        :return: true if success, else false
        """
        self.ssh.scp_put(_from, to)

    def close(self):
        """
        free connection and memory resource
        Warning: user must call this for resource free
        """
        self.db.close()
        self.ssh.close()

    def __getattr__(self, item):
        if item in self.plugins:
            return partial(self.plugins[item], self)
        else:
            raise AttributeError("'{}' object has no attribute {}".format(self.__class__.__name__, item))

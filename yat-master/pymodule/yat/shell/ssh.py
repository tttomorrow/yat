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

import io
from threading import Thread, Lock

import paramiko
import scp
from paramiko.client import MissingHostKeyPolicy


class _Buffer:
    """
    Thread-safe Buffer using StringIO
    """
    def __init__(self):
        self._io = io.StringIO()
        self._lock = Lock()

    def write(self, data):
        try:
            self._lock.acquire()
            self._io.write(data)
        finally:
            self._lock.release()

    def getvalue(self):
        return self._io.getvalue()


class _AllOkPolicy(MissingHostKeyPolicy):
    """
    accept all missing host key policy for paramiko
    """
    def missing_host_key(self, client, hostname, key):
        pass


class SSH:
    """
    Ssh client to execute remote shell command and scp files or directories
    """

    @staticmethod
    def _read_to(stream, buffer):
        """
        Read stream to buffer in other thread
        """

        def _read_handle():
            line = stream.readline()
            while line:
                buffer.write(line)
                line = stream.readline()

        thread = Thread(target=_read_handle)
        thread.start()
        return thread

    def __init__(self, user, password, host, port, **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = kwargs.get('timeout', None)
        self._do_connect()

    def _do_connect(self):
        """
        do the ssh2 session connect with username and password
        """
        self._session = paramiko.SSHClient()
        self._session.set_missing_host_key_policy(_AllOkPolicy)
        self._session.connect(self.host, self.port, self.user, self.password, timeout=self.timeout)

    def sh(self, cmd, *params, **kwargs) -> (int, str):
        """
        execute shell command in remote host with ssh2 protocol
        :param cmd: command in text
        :param params: arguments for command format
        :param kwargs: named-arguments for command format
        :return: (exit_code, output(include stderr and stdout))
        """
        channel = self._session.get_transport().open_session()
        if len(params) == 0 and len(kwargs) == 0:
            real_cmd = cmd
        else:
            real_cmd = cmd.format(*params, kwargs)
        channel.exec_command(real_cmd.format(*params, **kwargs))
        stdout = channel.makefile('r', 40960)
        stderr = channel.makefile_stderr('r', 40960)

        buffer = _Buffer()
        stdout_reader = self._read_to(stdout, buffer)
        stderr_reader = self._read_to(stderr, buffer)

        stdout_reader.join()
        stderr_reader.join()

        return_code = channel.recv_exit_status()

        return return_code, buffer.getvalue()

    def scp_get(self, _from, to, force=False):
        """
        get remote directory or files to local
        :param _from: the remote path to fetch
        :param to: the local path
        :param force: force override local exists files
        :exception IOError if io error occur
        """
        scp.get(self._session.get_transport(), _from, to, recursive=True)

    def scp_put(self, _from, to, force=False):
        """
        put local file or directory to remote host
        :param _from: local file or directory
        :param to: remote file or directory
        :param force: force override exists files or not
        """
        scp.put(self._session.get_transport(), _from, to, recursive=True)

    def close(self):
        """
        close the ssh2 session connection, when call to a closed ssh instance error will be raise
        """
        self._session.close()

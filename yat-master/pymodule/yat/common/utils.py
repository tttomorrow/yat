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

import functools
import os
import stat
import warnings

import pwd


def scan_path(path, handler, include=False):
    """
    scan a directory with DFS
    :param path: path to scan
    :param handler: handler to deal with each node in path tree
    :param include: deal with the path itself or not
    """
    if os.path.isdir(path):
        sub_files = os.listdir(path)

        for file in sub_files:
            real_file = os.path.join(path, file)
            if os.path.isdir(real_file):
                scan_path(real_file, handler)
                handler(real_file, True, file)
            else:
                handler(real_file, False, file)

        path_is_dir = True
    else:
        path_is_dir = False

    if include:
        handler(path, path_is_dir, os.path.basename(path))


def chmod(path, mode, recursion=False, path_filter=None, onerror=None):
    """
    chmod with recursion and path filter
    :param path: the file or dir to chmod
    :param mode: the mode to set to file or dir
    :param recursion: recursion to all sub file or dir of dir
    :param path_filter: a func (path) -> bool to filter the path to be set or not set
           if None do not filter
    :param onerror: a func (path, exception) -> None, when error occur call this func,
           if None just throw the error
    """
    try:
        if path_filter is None:
            os.chmod(path, mode)
        elif path_filter(path):
            os.chmod(path, mode)
    except Exception as e:
        if onerror:
            onerror(path, e)
        else:
            raise e
    if recursion and os.path.isdir(path):
        for sub_file in os.listdir(path):
            chmod(os.path.join(path, sub_file), mode, recursion, path_filter)


def rmtree(path, include_self=True, follow_link=False):
    def _rm(_path):
        for sub in os.listdir(_path):
            _real_path = os.path.join(_path, sub)
            if os.path.isdir(_real_path):
                if os.path.islink(_real_path):
                    if follow_link:
                        _rm(_real_path)
                    else:
                        os.unlink(_real_path)
                else:
                    _rm(_real_path)
                    os.rmdir(_real_path)
            else:
                os.unlink(_real_path)

    if os.path.isdir(path):
        if os.path.islink(path):
            if follow_link:
                _rm(path)
        else:
            _rm(path)

        if include_self:
            if os.path.islink(path):
                os.unlink(path)
            else:
                os.rmdir(path)
    else:
        os.unlink(path)


def get_ugid(user):
    _, _, uid, gid, *_ = pwd.getpwnam(user)
    return uid, gid


root_uid, root_gid = get_ugid('root')

_perm_enum = {
    '': 0,
    'r': 4,
    'w': 2,
    'x': 1,
    'rx': 5,
    'wx': 3,
    'rw': 6,
    'rwx': 7
}


def _str2permission(perm):
    res = _perm_enum.get(perm)
    if res is None:
        raise RuntimeError(f"not a valid permission string {perm}")

    return res


def get_permission(file_path):
    path_stat = os.stat(file_path)
    return stat.S_IMODE(path_stat.st_mode)


def user_has_permission(user, path, permission):
    if isinstance(user, (int,)):
        uid = user
        gid = pwd.getpwuid(uid)[3]
    else:
        _, _, uid, gid, *_ = pwd.getpwnam(user)

    if isinstance(permission, (int,)):
        if permission < 0 or permission > 7:
            raise RuntimeError(f"not allow permission argument {permission}")
    else:
        permission = _str2permission(permission)

    path_stat = os.stat(path)
    mode = stat.S_IMODE(path_stat)
    path_uid = path_stat.st_uid
    path_gid = path_stat.st_gid

    if uid == path_uid:
        return ((mode & 0o700) >> 8) & permission == permission
    elif gid == path_gid:
        return (mode & 0o070) >> 4 & permission == permission
    else:
        return (mode & 0o007) & permission == permission


def curr_user_hash_permission(path, permission):
    return user_has_permission(os.getuid(), path, permission)


def deprecated(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)
        return func(*args, **kwargs)

    return _wrapper

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
import re
import stat
from yat.common.shell import shell_output
from yat.errors import YatError


def env_checking():
    """
    checking the git instance and version
    :return:
    """
    errors = []

    ret, out = shell_output('git --version')

    if ret != 0:
        errors.append("git is not install in this system")
        return errors

    matcher = re.match(r'.*([0-9]+)\.([0-9]+)\.([0-9]+).*', out)
    if matcher is None:
        raise YatError('unknown error occur when running command git --version:\n%s' % out)
    else:
        major = int(matcher.group(1))
        version = int(matcher.group(2))

        if major < 1 or version < 7:
            errors.append('git version 1.7+ is required')

    return errors


def clone(url, repo=None, branch=None):
    """
    clone git repo from given url to specific repo directory with given branch
    :param url:
    :param repo:
    :param branch:
    :return:
    """
    if branch:
        clone_cmd = 'git clone -b {} {}'.format(branch, url)
    else:
        clone_cmd = 'git clone {}'.format(url)

    if repo:
        clone_cmd += ' {}'.format(repo)

    ret, out = shell_output(clone_cmd)
    if ret != 0:
        raise YatError('git clone with error: \n%s' % out)


def init(repo):
    ret, out = shell_output('mkdir -p {0}; cd {0}; git init'.format(repo))
    if ret != 0:
        raise YatError('git init with error: \n{}'.format(out))


def add_remote(repo, name, url):
    """
    add new remote with given name
    :param repo:
    :param name:
    :param url:
    :return:
    """
    remotes = get_remotes(repo)
    if name in remotes:
        raise YatError('remote with name {} is exists'.format(name))
    else:
        ret, out = shell_output('cd {}; git remote add {} {}'.format(repo, name, url))
        if ret != 0:
            raise YatError('git add remote failed: \n%s' % out)


def fetch(repo, remote=None):
    """
    fetch remote with given remote name
    :param repo:
    :param remote:
    :return:
    """
    if remote:
        fetch_cmd = 'cd {}; git fetch {}'.format(repo, remote)
    else:
        fetch_cmd = 'cd {}; git fetch --all'.format(repo)
    ret, out = shell_output(fetch_cmd)
    if ret != 0:
        raise RuntimeError('git fetch with error: \n%s' % out)


def reset(repo, commit=None, hard=False):
    """
    reset current work tree or index to given commit
    :param repo:
    :param commit:
    :param hard:
    :return:
    """
    if commit is None:
        commit = ''

    if hard:
        reset_cmd = 'cd {}; git reset --hard {}'.format(repo, commit)
    else:
        reset_cmd = 'cd {}; git reset {}'.format(repo, commit)

    ret, out = shell_output(reset_cmd)
    if ret != 0:
        raise YatError('git reset with error: \n%s' % out)


def pull(repo):
    """
    pull current branch to latest of remote
    :param repo:
    :return:
    """
    ret, out = shell_output('cd {}; git pull'.format(repo))
    if ret != 0:
        raise YatError('git pull with error: \n%s' % out)


def checkout(repo, commit):
    """
    checkout tag, commit, branch
    :param repo:
    :param commit:
    :return:
    """
    ret, out = shell_output('cd {}; git checkout {}'.format(repo, commit))
    if ret != 0:
        raise YatError('git checkout with error: \n{}'.format(out))


def parse_dir(url):
    """
    parse dirname from url
    :param url:
    :return:
    """
    matcher = re.match(r'.*/(?:[a-zA-Z0-9._-]+/)*([a-zA-Z0-9._-]+)', url)
    if matcher is None:
        raise YatError('given url is invalid: %s' % url)
    else:
        dir_name = matcher.group(1)
        if dir_name.endswith('.git'):
            dir_name = dir_name[:-4]

        return dir_name


def get_remotes(repo):
    """
    get remote set
    :param repo:
    :return:
    """
    ret, out = shell_output('cd {}; git remote -v'.format(repo))
    if ret != 0:
        raise YatError('git remote with error: \n%s' % out)
    else:
        urls = {}
        for line in out.splitlines():
            matcher = re.match(r'(.+)[ \t]+([a-zA-Z0-9:/@._-]+)[ \t]+.*', line)
            if matcher:
                urls[matcher.group(1)] = matcher.group(2)
        return urls


def set_sparse_list(repo, sparse_list):
    """

    :param repo:
    :param sparse_list:
    :return:
    """
    ret, out = shell_output('cd {}; git config core.sparsecheckout true'.format(repo))
    if ret != 0:
        raise YatError('git config with error: \n{}'.format(out))

    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    with os.fdopen(os.open(os.path.join(repo, '.git', 'info', 'sparse-checkout'), flags, mode), 'w') as sparse:
        sparse.writelines(line + '\n' for line in sparse_list)


def remote_valid(url, repo):
    """
    valid the given url is in the exists repo's remote
    :param url:
    :param repo:
    :return:
    """
    urls = get_remotes(repo)

    if url not in urls.values():
        raise YatError('given remote not equal the exists repo remote:\n{}\nnot in:\n{}'.format(
            url,
            '\n'.join(('{}\t{}'.format(k, v) for k, v in enumerate(urls)))
        ))


def clean(repo):
    """
    git clean -df
    :param repo:
    :return:
    """
    ret, out = shell_output('cd {}; git clean -df'.format(repo))
    if ret != 0:
        raise YatError('git clean with error: \n%s' % out)


def clone_or_fetch(url, repo=None, branch=None, sparse_list=None):
    """
    clone a new repo or fetch all in exists repo
    :param url:
    :param repo:
    :param branch:
    :param sparse_list:
    :return:
    """
    if repo:
        git_dir = repo
    else:
        git_dir = parse_dir(url)

    if os.path.exists(git_dir):
        remote_valid(url, git_dir)
        if len(sparse_list) > 0:
            set_sparse_list(git_dir, sparse_list)

        clean(git_dir)
        reset(git_dir, commit='HEAD', hard=True)
        checkout(git_dir, branch)
        pull(git_dir)
    else:
        if len(sparse_list) > 0:
            init(git_dir)
            set_sparse_list(git_dir, sparse_list)
            add_remote(git_dir, 'origin', url)
            fetch(git_dir)
            checkout(git_dir, branch)
        else:
            clone(url, repo=git_dir, branch=branch)



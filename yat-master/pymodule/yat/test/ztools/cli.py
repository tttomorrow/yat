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

import click

from yat.test.ztools.errors import ArgumentsError, ZenithToolsError
from . import database as zdatabase
from . import install as zinstall
from . import instance as zinstance
from . import params as zparams
from .util import set_env


def get_action(opts, actions):
    """
    get the action from opts with action list
    :param opts:
    :param actions:
    :return:
    """
    action = None
    for it in actions:
        if opts[it]:
            if action:
                raise ArgumentsError('can not set --{0} when --{1} is set'.format(it, action))
            action = it
    return action


@click.group()
def cli():
    """
    ztools is utils for zenith
    """
    pass


@cli.command(name='install')
@click.option('-g', '--package', help='Setting the package file')
@click.option('-a', '--app', help='Setting the app home directory')
@click.option('-d', '--data', help='Set the data path to create instance')
@click.option('-p', '--port', type=int, help='Setting the port to listen', default=1611)
@click.option('-c', '--config', multiple=True, help='config to set to instance')
@click.option('-i', '--init-script', help='Creating database script to using')
@click.option('-t', '--init-template', help='Creating database template script to using')
@click.option('--create-db', is_flag=True, help='Create database or not')
@click.option('--origin', is_flag=True, help='')
def install(**opts):
    """
    Install binary of zenith from given package
    """
    origin = opts['origin']
    if origin:
        zinstall.origin_install(**opts)
    else:
        zinstall.install(opts['package'], opts['app'])

        data = opts['data']
        create_db = opts['create_db']
        config = opts['config'] if opts['config'] else []

        if data:
            zinstance.create_instance(data, opts['port'], config)

        if create_db:
            zdatabase.create_db(data)


INS_ACTION_KILL = 'kill'
INS_ACTION_CREATE = 'create'
INS_ACTION_DELETE = 'delete'
INS_ACTION_START = 'start'
INS_ACTION_STATUS = 'status'
INS_ACTIONS = (
    INS_ACTION_CREATE,
    INS_ACTION_KILL,
    INS_ACTION_DELETE,
    INS_ACTION_START,
    INS_ACTION_STATUS
)


@cli.command(name='instance')
@click.option('--kill', is_flag=True, help='Kill instance with given data path')
@click.option('--create', is_flag=True, help='Create a instance into given data path')
@click.option('--delete', is_flag=True, help='Delete an instance with given data path')
@click.option('--start', is_flag=True, help='Start a instance with given data path')
@click.option('--status', is_flag=True, help='Show the instance status')
@click.option('--db-charset', help='Set the database charset', default='utf8')
@click.option('-d', '--data', help='Setting the data directory', default='data', required=True)
@click.option('-p', '--port', type=int, help='Setting the port to listen(available when --create)', default=1611)
@click.option('-c', '--config', multiple=True, help='Config to set to instance(available when --create)')
@click.option('--create-db', is_flag=True, help='Create a database or not when instance created(available when --create)')
@click.option('-i', '--init-script', help='Creating database script to use(available when --create-db)')
@click.option('-t', '--init-template', help='Creating database template script to use(available when --create-db)')
@click.option('-m', '--mode', help='Setting the instance start mode(available when --start)', default='open')
def instance(**opts):
    """
    Zenith instance manager
    """
    set_env()
    action = get_action(opts, INS_ACTIONS)
    if action is None:
        raise ArgumentsError('instance action is not select within (--kill,--create,--delete,--start, --status)')

    data = opts['data']
    db_charset = opts['db_charset']

    if action == INS_ACTION_START:
        mode = opts['mode']
        if not zinstance.start_instance(data, mode):
            raise ZenithToolsError('start zenith instance failed, place see the logs')
        print('Instance Start Successfully')
    elif action == INS_ACTION_CREATE:
        port = opts['port']
        config = opts['config'] if opts['config'] else []
        create_db = opts['create_db']
        init_script = opts['init_script']
        init_template = opts['init_template']

        if not create_db and (init_template or init_script):
            raise ArgumentsError('-i/--init-script/-t/-init-template is not available when not setting --create-db')

        zinstance.create_instance(data, port, config)

        if create_db:
            if not zinstance.start_instance(data, 'nomount'):
                print(zinstance.get_run_log(data))
                raise ZenithToolsError('start zenith instance failed, place see the logs')
            zdatabase.create_db(
                data,
                init_script=init_script,
                init_template=init_template,
                db_charset=db_charset
            )
        print('Instance Create Successfully')
    elif action == INS_ACTION_DELETE:
        zinstance.delete_instance(data)
        print('Instance Delete Successfully')
    elif action == INS_ACTION_KILL:
        zinstance.kill_instance(data)
        print('Instance Kill Successfully')
    elif action == INS_ACTION_STATUS:
        status = zinstance.status_instance(data)
        print('Instance Status: %s' % status)
    else:
        raise ZenithToolsError('unknown error occur when parse instance action')


DB_ACTION_CREATE = 'create'
DB_ACTION_DELETE = 'delete'
DB_ACTIONS = (
    DB_ACTION_CREATE,
    DB_ACTION_DELETE
)


@cli.command(name='database')
@click.option('--create', is_flag=True, help='Create a database with given data path')
@click.option('--delete', is_flag=True, help='Delete database with given data path')
@click.option('--db-charset', help='Set the database charset', default='utf8')
@click.option('-d', '--data', help='Setting the data directory', default='data', required=True)
@click.option('--no-clean-archive', is_flag=True, help='Don not clean the archive log files when delete database(available when --delete)')
@click.option('-i', '--init-script', help='Creating database script to use(available when --create-db)')
@click.option('-t', '--init-template', help='Creating database template script to use(available when --create-db)')
def database(**opts):
    """
    Zenith database manager
    """
    set_env()
    action = get_action(opts, DB_ACTIONS)
    if action is None:
        raise ArgumentsError('database action is not select within (--create,--delete)')

    data = opts['data']
    if action == DB_ACTION_DELETE:
        zdatabase.delete_db(data, not opts['no_clean_archive'])
        print('Database Delete Successfully')
    elif action == DB_ACTION_CREATE:
        zdatabase.create_db(
            data,
            init_script=opts['init_script'],
            init_template=opts['init_template'],
            db_charset=opts['db_charset']
        )
        print('Database Create Successfully')
    else:
        raise ZenithToolsError('unknown error occur when parse database action')


PARAM_ACTION_WRITE = 'write'
PARAM_ACTION_READ = 'read'
PARAM_ACTIONS = (
    PARAM_ACTION_READ,
    PARAM_ACTION_WRITE
)


@cli.command(name='params')
@click.option('--write', help='Write zenith setting params into file')
@click.option('--read', help='Read zenith setting from setting file')
@click.option('-i', '--init-file', help='Init configure file to read')
@click.option('-w', '--write-file', help='File to write new configure')
@click.option('-c', '--config', multiple=True, help='Configure to set')
def params(**opts):
    """
    Zenith params manager
    """
    set_env()
    action = get_action(opts, PARAM_ACTIONS)
    if action is None:
        raise ArgumentsError('params action is not select within (--read,--write)')
    init_file = opts['init_file']

    if init_file:
        finit = open(init_file)
        param = zparams.ZParam(finit.read())
    else:
        param = zparams.ZParam()
    config = opts['config'] if opts['config'] else []

    if action == PARAM_ACTION_WRITE:
        write_file = opts['write_file']
        if write_file is None:
            raise ArgumentsError('-w/--write-file must be set when set --write action')

        for cnf in config:
            idx = cnf.index('=')
            key = cnf[:idx].strip()
            value = cnf[idx + 1:].strip()
            param.set(key, value)

        param.save(write_file)
        print('Configure Write Successfully')
    elif action == PARAM_ACTION_READ:
        for cnf in config:
            print(param.get(cnf))
    finit.close()
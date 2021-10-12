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

import yaml
from yaml import loader

from yat.guard.errors import TestGuardError
from .context import ctx

# store actions to load
_actions = []


def _load_action(fun):
    _actions.append(fun)
    return fun


def load(config_path):
    """
    load all configure to context from a yaml file
    :param config_path: the configure file path
    """
    with open(config_path) as fconfig:
        context = yaml.safe_load(fconfig)
        if context is None:
            return

        for action in _actions:
            action(context)


@_load_action
def _load_meta_checker(context):
    checker = context.get('meta_checker')

    if checker:
        for key, value in checker.items():
            if key in ctx.meta_checker:
                if 'required' in value:
                    ctx.meta_checker[key]['required'] = value['required']
                if 'checker' in value:
                    ch = value['checker']
                    if isinstance(ch, (list, tuple)):
                        ctx.meta_checker[key]['checker'] = [re.compile(it) for it in ch]
                    else:
                        ctx.meta_checker[key]['checker'] = re.compile(ch)

            else:
                raise TestGuardError('found unknown setting keys: meta_checker.{}'.format(key))


@_load_action
def _load_valid_case(context):
    valid_case = context.get('valid_case')

    if valid_case:
        for key, value in valid_case.items():
            ctx.valid_case[key] = value


@_load_action
def _load_valid_charset(context):
    valid_charset = context.get('valid_charset')
    if valid_charset:
        ctx.valid_charset = []
        ctx.valid_charset.append(valid_charset)


@_load_action
def _load_case_name_checker(context):
    case_checker = context.get('case_name_checker')
    if case_checker:
        for key, value in case_checker.items():
            if key not in ctx.case_name_checker:
                raise TestGuardError('found unknown setting keys: case_name_checker.{}'.format(key))

            if key in {'name_regex', 'weak_name_regex', 'feature_regex', 'serial_regex'}:
                ctx.case_name_checker[key] = re.compile(value)
            elif key == 'feature_size':
                if isinstance(value, (tuple, list)) and len(value) == 2:
                    ctx.case_name_checker[key] = value
                else:
                    raise TestGuardError('found invalid value {} of setting key: case_name_checker.{}'.format(value, key))
            elif isinstance(value, (str, tuple, list, int)):
                ctx.case_name_checker[key] = value
            else:
                raise TestGuardError('found invalid value {} of setting keys: case_name_checker.{}'.format(value, key))


@_load_action
def _load_case_size_checker(context):
    case_size_checker = context.get('case_size_checker')
    if case_size_checker:
        for key, value in case_size_checker.items():
            if key not in ctx.case_size_checker:
                raise TestGuardError('found unknown setting keys: case_size_checker.{}'.format(key))
            ctx.case_size_checker[key] = value


@_load_action
def _load_checker_lists(context):
    checkers = context.get('checkers')
    if isinstance(checkers, (type, list)):
        ctx.checkers = checkers
    elif isinstance(checkers, (str,)):
        ctx.checkers = [checkers]
    else:
        raise TestGuardError('found invalid type {} of setting key: checkers'.format(checkers))

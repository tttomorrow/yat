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

import random


def random_perm(*params, count=10, use_weight=True):
    """
    random select from given params

    the pattern of params is :

    1. (
            (A, A, A, ..., A),
            (A, A, A, ..., A),
            ...,
            (A, A, A, ..., A)
        )

    2. (
            (
                (A, weight),
                (A, weight),
                ...
                (A, weight)
            ),
            (
                (A, weight),
                (A, weight),
                ...
                (A, weight)
            ),
            ...,
            (
                (A, weight),
                (A, weight),
                ...
                (A, weight)
            )
        )

    :param params: a list of list
    :param count: random generate count
    :param use_weight: use weight random-select or not
    :return: a list of perm data
    """
    select_param = []
    for param in params:
        if not use_weight:
            population, use_weight = param, None
        elif isinstance(param[0], (tuple, list)):
            population, use_weight = zip(*param)
        else:
            population, use_weight = param, None

        select_param.append(random.choices(population, weights=use_weight, k=count))

    return tuple(zip(*select_param))


def _combination(params, index, res, current_list: list):
    if len(current_list) == len(params):
        res.append([it for it in current_list])
    else:
        for item in params[index]:
            current_list.append(item)
            _combination(params, index + 1, res, current_list)
            current_list.pop()


def all_perm(*params):
    """
    get the perm of given params

    the pattern of params :see random_perm
    :param params: a list of list
    """
    current_list = []
    res = []
    _combination(params, 0, res, current_list)
    return res


def param_case():
    """
    decorator to make new test case class using params
    """
    def _wrapper(cls):
        name = cls.__name__
        test_funcs = {}

        for attr in dir(cls):
            it = getattr(cls, attr)
            if not hasattr(it, '__parameters__') or not callable(it):
                continue

            delattr(cls, attr)
            parameters = getattr(it, '__parameters__')

            pre_doc = '' if it.__doc__ is None else it.__doc__

            for i, param in enumerate(parameters):
                def _gen_method(_parameter, origin_method):
                    def _test_func(self):
                        return origin_method(self, _parameter)

                    return _test_func

                test_func = _gen_method(param, it)
                test_func.__doc__ = '{} with param {}'.format(pre_doc, param)
                test_funcs['{}_{}'.format(attr, i)] = test_func

        new_class = type(name, (cls,), test_funcs)

        return new_class

    return _wrapper


def param_item(*parameters):
    """
    decorator to set param for test methods

    Usage:

    @param_case()
    class TestXXX(TestCase):
        @param_item(1, 3, 4)
        def test_xxx(self, params):
            ...

    that will generate code like this:

    class TestXXX(TestCase):
        def test_xxx_0(self):
            test_xxx(this, 1)

        def test_xxx_1(self):
            test_xxx(this, 3)

        def test_xxx_2(self):
            test_xxx(this, 4)
    """
    def _wrapper(fun):
        setattr(fun, '__parameters__', parameters)
        return fun

    return _wrapper


def random_param(*params, count=10, use_weight=True):
    """
    decorator to set random select param of perm of param

    Usage:

    @param_case()
    class TestXXX(TestCase):
        @random_param((1, 2, 3), ('A', 'B'), count=2)
        def test_xxx(self, params):
            ...

    that will generate code like this:

    class TestXXX(TestCase):
        def test_xxx_0(self):
            test_xxx(this, (2, 'A'))

        def test_xxx_1(self):
            test_xxx(this, (3, 'B'))
    """
    return param_item(*random_perm(*params, count=count, use_weight=use_weight))


def perm_param(*params):
    """
    decorator to set random select all perm param

    Usage:

    @param_case()
    class TestXXX(TestCase):
        @random_param((1, 2, 3), ('A', 'B'))
        def test_xxx(self, params):
            ...

    that will generate code like this:

    class TestXXX(TestCase):
        def test_xxx_0(self):
            test_xxx(this, (1, 'A'))

        def test_xxx_1(self):
            test_xxx(this, (1, 'B'))

        def test_xxx_2(self):
            test_xxx(this, (2, 'A'))

        def test_xxx_3(self):
            test_xxx(this, (2, 'B'))

        def test_xxx_4(self):
            test_xxx(this, (3, 'A'))

        def test_xxx_5(self):
            test_xxx(this, (3, 'B'))
    """
    return param_item(*all_perm(*params))

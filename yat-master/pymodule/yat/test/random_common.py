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
"""

Util functions for random action for py unittest test case

"""

import random
import time


def seed(seed=None):
    """
    set the seed to generate
    :param seed: the seed value, if None use time.clock()
    """
    random.seed(seed if seed else time.clock())


def select(threshold):
    """
    a selector with specific threshold
    :param threshold: [0,1], threshold
    :return: true or false
    """
    if threshold < 0 or threshold > 1:
        raise RuntimeError("select require threshold [0,1]")
    return random.random() < threshold


def array_select(self, arr):
    return arr[random.randint(0, len(arr) - 1)]

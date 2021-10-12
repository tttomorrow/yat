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

import logging
from unittest import TestCase


class TestLogging(TestCase):
    def test_logging(self):
        handler = logging.FileHandler('d:\\abc.log')
        handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)6s %(threadName)s - [%(filename)s] %(message)s"))

        log = logging.getLogger('abc')
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)

        print(log.handlers)

        log.info("abc")
        log.info("hello, world")
        log.debug('xml')
        log.error('error name')
        for i in range(100):
            log.warning("{}'ths name found".format(str(i)))

        handler.close()
        log.handlers.clear()

        handler = logging.FileHandler('d:\\abc1.log')
        handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s %(levelname)6s %(threadName)s - [%(filename)s] %(message)s"))
        log.addHandler(handler)

        log.info("abc")
        log.info("hello, world")
        log.debug('xml')
        log.error('error name')
        for i in range(100):
            log.warning("{}'ths name found".format(str(i)))

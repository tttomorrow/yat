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
import tornado.escape
import tornado.web
from ..executor.unittest import UnittestExecutor


class UnittestHandler(tornado.web.RequestHandler):
    """
    handler to execute unittest python file
    """
    def post(self):
        """
        [request]

        post
        {
            case: case/name
            out: /path/to/output
            log: /path/to/log
        }


        [response]

        {
            result: success|failed

        }
        """
        file_info = tornado.escape.json_decode(self.request.body)
        result = UnittestExecutor().execute(file_info['case'], file_info['out'], file_info['log'])

        self.finish({'result': 'success' if result.wasSuccessful() else 'failed'})


class RunnableHandler(tornado.web.RequestHandler):
    def post(self):
        pass

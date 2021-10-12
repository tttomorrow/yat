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

import tornado.web
import tornado.escape
from yat.pyexecutor.vars import var


class VarsHandler(tornado.web.RequestHandler):
    """
    the vars manager
    """
    def post(self):
        """
        POST /vars

        {
            key1: val1,
            key2: val2,
            key3: val3,
            ...
        }
        """
        the_vars = tornado.escape.json_decode(self.request.body)
        print(the_vars)
        for k, v in the_vars.items():
            var[k] = v

        for k, v in var.items():
            print("%-25s = %s" % (k, v))

    def delete(self):
        """
        DELETE /vars

        // delete all
        {
            vars: ['*']
        }

        // delete specific
        {
            vars: ['key1', 'key2', 'key3', ...]
        }
        """
        the_vars = tornado.escape.json_decode(self.request.body)
        keys = the_vars['vars']

        if len(keys) == 1 and keys[0] == '*':
            var.clear()
        else:
            for k in keys:
                del var[k]

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

import sys

from common_sql.plain_parser import PlainParser
from ..plugins import plugin
from ..result import YatResult


class ExplainResult(YatResult):
    def __init__(self, result):
        super(ExplainResult, self).__init__(result)


@plugin('zenith')
def explain(self, sql, *args):
    res = self.db.execute_query('explain ' + sql, *args)
    PlainParser([v[0] for v in res]).parse()


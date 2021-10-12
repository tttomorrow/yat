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

import json
import re
import stat
from yat.guard.report.basic import Reporter
from yat.guard.report.report_manager import reporter


@reporter
class JSONReporter(Reporter):
    _url_pattern = re.compile(r'^file:json:([^:]+\.json)$')

    def __init__(self, url, **opts):
        json_filename = self._parse_json_path(url)
        self.json_filename = json_filename
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        self._stream = os.fdopen(os.open(json_filename, flags, mode), 'w')
        self._stream.write('[\n')
        self._cache = None

    def report(self, error):
        node = error.to_dict()

        if self._cache is None:
            self._cache = node
        else:
            self._stream.write("  {},\n".format(json.dumps(self._cache)))
            self._cache = node

    def finish(self):
        if self._cache is not None:
            self._stream.write("  {}\n".format(json.dumps(self._cache)))
            self._stream.write(']\n')
        self._stream.close()

    def _parse_json_path(self, url):
        return self._url_pattern.match(url).group(1)

    @classmethod
    def match(cls, url):
        return None is not cls._url_pattern.match(url)

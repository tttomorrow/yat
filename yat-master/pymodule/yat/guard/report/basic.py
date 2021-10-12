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
import stat
from .report_manager import reporter


class Reporter:
    def report(self, error):
        raise RuntimeError("must override handle method")

    def finish(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()


class ConsoleReporter(Reporter):
    def report(self, error):
        print(error)


@reporter
class TextFileReporter(Reporter):
    _url_pattern = re.compile(r'^file:text:([^:]+\.(?:txt|log))$')

    def __init__(self, url, **opts):
        self.filename = self._parse_text_path(url)
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        self.writer = os.fdopen(os.open(self.filename, flags, mode), 'w')

    def report(self, error):
        self.writer.write(str(error) + "\n")

    def finish(self):
        self.writer.close()

    def _parse_text_path(self, url):
        return self._url_pattern.match(url).group(1)

    @classmethod
    def match(cls, url):
        return None is not cls._url_pattern.match(url)


class CombineReporter(Reporter):
    def __init__(self, *reports):
        self.reports = reports

    def report(self, error):
        for report in self.reports:
            report.report(error)

    def finish(self):
        for report in self.reports:
            report.finish()


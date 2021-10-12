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

import os
import re
import stat
from jinja2 import Template

from yat.guard.report.basic import Reporter
from yat.guard.report.report_manager import reporter


@reporter
class HTMLReporter(Reporter):
    _url_pattern = re.compile(r'^file:html:([^:]+\.html)$')

    def __init__(self, url, **opts):
        html_filename = self._parse_html_path(url)
        self.html_filename = html_filename
        self.cache = []
        self.template = opts.get('template', os.path.join(os.path.dirname(__file__), 'template.html'))

    def report(self, error):
        self.cache.append(error.to_dict())

    def finish(self):
        with open(self.template) as ftemplate:
            template = Template(ftemplate.read())
            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
            mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
            with os.fdopen(os.open(self.html_filename, flags, mode), 'w', buffering=1000000) as out:
                out.write(template.render(errors=self.cache))

    def _parse_html_path(self, url):
        return self._url_pattern.match(url).group(1)

    @classmethod
    def match(cls, url):
        return None is not cls._url_pattern.match(url)

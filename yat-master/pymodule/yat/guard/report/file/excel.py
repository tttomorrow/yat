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

from yat.guard.report.basic import Reporter
from yat.guard.report.report_manager import reporter


@reporter
class ExcelReporter(Reporter):
    _url_pattern = re.compile(r'^file:excel:([^:]+\.xlsx?)$')

    def __init__(self, url, **opts):
        openpyxl = __import__('openpyxl')
        self.styles = openpyxl.styles

        self.line_style = None
        self.head_style = None
        self.init_style()

        self.excel_filename = self._parse_excel_path(url)
        self.book = openpyxl.Workbook()
        self.book.remove_sheet(self.book['Sheet'])
        self.sheet = self.book.create_sheet('Check Result')
        self.sheet.cell(1, 1, value='Level')
        self.sheet.cell(1, 2, 'Code')
        self.sheet.cell(1, 3, 'Name')
        self.sheet.cell(1, 4, 'Type')
        self.sheet.cell(1, 5, 'Error')
        self.sheet.cell(1, 6, 'File')
        self.set_style('A1:F1', self.head_style)

        self.sheet.column_dimensions['A'].width = 10
        self.sheet.column_dimensions['B'].width = 15
        self.sheet.column_dimensions['C'].width = 20
        self.sheet.column_dimensions['D'].width = 30
        self.sheet.column_dimensions['E'].width = 50
        self.sheet.column_dimensions['F'].width = 70

        self.line = 2

    def init_style(self):
        common_side = self.styles.Side(color='444444', border_style='thin')
        hs = self.head_style = self.styles.NamedStyle('head_style')
        hs.font = self.styles.Font(bold=True, size=11, name='Courier New')
        hs.border = self.styles.Border(left=common_side, right=common_side, top=common_side, bottom=common_side)
        hs.fill = self.styles.PatternFill('solid', fgColor='F0F0F0', bgColor='10A010')

        ls = self.line_style = self.styles.NamedStyle('line_style')
        ls.font = self.styles.Font(bold=False, size=10, name='Courier New')
        ls.border = hs.border

    def set_style(self, cell, style):
        for line in self.sheet[cell]:
            for cell in line:
                cell.style = style

    def report(self, error):
        self.sheet.cell(self.line, 1, str(error.level))
        self.sheet.cell(self.line, 2, str(error.code))
        self.sheet.cell(self.line, 3, error.name)
        self.sheet.cell(self.line, 4, error.type)
        self.sheet.cell(self.line, 5, error.msg)
        self.sheet.cell(self.line, 6, error.script)
        self.set_style('A{0}:F{0}'.format(self.line), self.line_style)
        self.line += 1

    def finish(self):
        self.book.save(self.excel_filename)

    def _parse_excel_path(self, url):
        matcher = self._url_pattern.match(url)
        return matcher.group(1)

    @classmethod
    def match(cls, url):
        return None is not cls._url_pattern.match(url)

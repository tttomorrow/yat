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

from yat.guard.export import storage


@storage
class CIDAExcelStorage:
    _url_pattern = re.compile(r'^file:excel:cida:([^:]+\.xlsx?)$')

    def __init__(self, url, **opts):
        openpyxl = __import__('openpyxl')
        self.styles = openpyxl.styles

        self.excel_path = self._url_pattern.match(url).group(1)
        self.head_style = None
        self.line_style = None
        self.init_style()

        self.book = openpyxl.Workbook()
        self.book.remove_sheet(self.book['Sheet'])
        self.sheet = self.book.create_sheet('Test Cases')
        self.sheet.cell(1, 1,  'Depth')
        self.sheet.cell(1, 2,  'Feature_Name')
        self.sheet.cell(1, 3,  'Feature_Number')
        self.sheet.cell(1, 4,  'TestCase_Name')
        self.sheet.cell(1, 5,  'TestCase_Number')
        self.sheet.cell(1, 6,  'TestCase_Pretreatment Condition')
        self.sheet.cell(1, 7,  'TestCase_Test Steps')
        self.sheet.cell(1, 8,  'TestCase_Expected Result')
        self.sheet.cell(1, 9,  'TestCase_Level')
        self.sheet.cell(1, 10, 'TestCase_Test Case Type')
        self.sheet.cell(1, 11, 'TestCase_Automated')
        self.sheet.cell(1, 12, 'TestCase_Design Description')
        self.sheet.cell(1, 13, 'TestCase_Remark')
        self.sheet.cell(1, 14, 'RMResource_Name')
        self.sheet.cell(1, 15, 'TestCase_Author')
        self.sheet.cell(1, 16, 'Association_RMResource_Number')
        self.sheet.cell(1, 17, 'Association_RMResource_Name')
        self.set_style('A1:Q1', self.head_style)

        self.sheet.column_dimensions['A'].width = 10
        self.sheet.column_dimensions['C'].width = 20
        self.sheet.column_dimensions['D'].width = 20
        self.sheet.column_dimensions['E'].width = 20
        self.sheet.column_dimensions['F'].width = 40
        self.sheet.column_dimensions['G'].width = 45

        self.line = 2

    def set_style(self, cell, style):
        for line in self.sheet[cell]:
            for cell in line:
                cell.style = style

    def init_style(self):
        common_side = self.styles.Side(color='444444', border_style='thin')
        hs = self.head_style = self.styles.NamedStyle('head_style')
        hs.font = self.styles.Font(bold=True, size=11, name='Courier New')
        hs.border = self.styles.Border(left=common_side, right=common_side, top=common_side, bottom=common_side)
        hs.fill = self.styles.PatternFill('solid', fgColor='F0F0F0', bgColor='10A010')

        ls = self.line_style = self.styles.NamedStyle('line_style')
        ls.font = self.styles.Font(bold=False, size=10, name='Courier New')
        ls.border = hs.border

    def store(self, meta):
        case_name = self._get_case_name(meta.script)
        case_content = self._get_case_content(meta.script)
        requirement_txt = self._get_requirement_txt(meta.requirement)
        author_txt = self._get_author_txt(meta.owner)

        self.sheet.cell(self.line, 1,  '...')
        self.sheet.cell(self.line, 2,  '')
        self.sheet.cell(self.line, 3,  '')
        self.sheet.cell(self.line, 4, case_name)
        self.sheet.cell(self.line, 5,  case_name)
        self.sheet.cell(self.line, 6,  '')
        self.sheet.cell(self.line, 7, case_content)
        self.sheet.cell(self.line, 8,  '')
        self.sheet.cell(self.line, 9, 'Level 3')
        self.sheet.cell(self.line, 10,  '')
        self.sheet.cell(self.line, 11, 'True')
        self.sheet.cell(self.line, 12, '')
        self.sheet.cell(self.line, 13, '')
        self.sheet.cell(self.line, 14, '')
        self.sheet.cell(self.line, 15, author_txt)
        self.sheet.cell(self.line, 16, requirement_txt)
        self.sheet.cell(self.line, 17, requirement_txt)
        self.set_style('A{0}:Q{0}'.format(self.line), self.line_style)
        self.line += 1

    def finish(self):
        self.book.save(self.excel_path)

    @classmethod
    def match(cls, url):
        return None is not cls._url_pattern.match(url)

    @staticmethod
    def _get_case_name(script):
        return os.path.splitext(os.path.splitext(os.path.basename(script))[0])[0]

    @staticmethod
    def _get_case_content(script):
        with open(script, 'rb') as content:
            content = content.read()
            if len(content) > 32000:
                return content[:32000]
            else:
                return content

    @staticmethod
    def _get_requirement_txt(requirement):
        return ';'.join(requirement)

    @staticmethod
    def _get_author_txt(author):
        return ';'.join(author)

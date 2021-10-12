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
test_case_name：tc_{stage}_{module}_{features}[_{serial}]

stage：sdv | sit | svt
module：sql | storage | cm | om | tools
features：Users can defined 3 level features, which must be combined by '_',
          and for each sub-feature name only contains by lower letters and numbers,
          and which must not begin with number, and the max-length is 8
serial：optional，which is the feature serial, and only contains by numbers, the max-length is 4


"""
from yat.guard.setting import ctx
from .common import _split_case_name
from .manager import checker
from ..errors import CheckError


@checker
class CaseNameChecker:
    """
    test case name checker
    """
    name = 'weak_case_name_checker'

    def __init__(self):
        self.name_regex = ctx.case_name_checker['weak_name_regex']

    def check(self, script):
        """
        check script test case name valid
        :param script: the full script path name
        :return: list of error
        """
        errors = []
        case_name, _ = _split_case_name(script)
        if not self.name_regex.match(case_name):
            errors.append(CheckError.error(
                CheckError.CHECK_ERROR,
                self.name,
                'case name valid',
                'the case name {} is invalid'.format(case_name),
                script
            ))

        return errors



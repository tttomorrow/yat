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
import re

from yat.guard.setting import ctx
from .common import _split_case_name
from .manager import checker
from ..errors import CheckError


@checker
class CaseNameChecker:
    """
    test case name checker
    """
    name = 'case_name_checker'

    digits_regex = re.compile('[0-9]+')

    def __init__(self):
        self.name_regex = ctx.case_name_checker['name_regex']
        self.feature_regex = ctx.case_name_checker['feature_regex']
        self.feature_max_count = ctx.case_name_checker['feature_max_count']
        self.feature_size = ctx.case_name_checker['feature_size']
        self.prefix = ctx.case_name_checker['prefix']
        self.serial_regex = ctx.case_name_checker['serial_regex']
        self.serial_max_size = ctx.case_name_checker['serial_max_size']

    def check(self, script):
        """
        check script test case name valid
        :param script: the full script path name
        :return: list of error
        """
        errors = []
        case_name, _ = _split_case_name(script)
        if self.name_regex.match(case_name):
            return errors

        names = case_name.split('_')
        names_len = len(names)

        if names_len < 2:
            errors.append(CheckError.error(
                CheckError.CHECK_ERROR,
                self.name,
                'case feature name miss',
                'the case name {} require at last one feature name'.format(case_name),
                script
            ))
            return errors

        prefix, *features = names
        if prefix != 'tc':
            errors.append(CheckError.error(
                CheckError.CHECK_ERROR,
                self.name,
                'case name prefix invalid',
                'the case name {} should start with prefix {}'.format(case_name, self.prefix),
                script
            ))

        if len(features) == 1:
            if self.digits_regex.match(features[0]):
                errors.append(CheckError.error(
                    CheckError.CHECK_ERROR,
                    self.name,
                    'case feature name miss',
                    'the case name {} require at last one feature name'.format(case_name),
                    script
                ))

                if not self.serial_regex.match(features[0]):
                    errors.append(CheckError.error(
                        CheckError.CHECK_ERROR,
                        self.name,
                        'case feature name miss',
                        'the case name {} require at last one feature name'.format(case_name),
                        script
                    ))
            else:
                errors.extend(self._check_feature(case_name, script, features))
        else:
            if self.serial_regex.match(features[-1]):
                feature_count = len(features) - 1
                errors.extend(self._check_feature(case_name, script, features[:-1]))
            else:
                feature_count = len(features)
                errors.extend(self._check_feature(case_name, script, features))

            if feature_count > self.feature_max_count:
                errors.append(CheckError.error(
                    CheckError.CHECK_ERROR,
                    self.name,
                    'case name feature count too big',
                    'the case name {}\'s feature name count is bigger than the max value {}'.format(
                        case_name,
                        self.feature_max_count),
                    script
                ))
        return errors

    def _check_feature(self, case_name, script, features):
        errors = []

        for feature in features:
            if not self.feature_regex.match(feature):
                errors.append(CheckError.error(
                    CheckError.CHECK_ERROR,
                    self.name,
                    'case feature name invalid',
                    'the case name {}\'s feature name {} is invalid'.format(case_name, feature),
                    script
                ))

        return errors


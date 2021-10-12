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
import os

from yat.errors import YatError
from yat.suite.workdir import WorkDir

_result_map = {
    'failed': 'F',
    'ok': 'S',
    'ignore': 'I'
}


def _make_upload_format(res, **kwargs):
    upload_data = {
        'common': {
            'trigger': 'Yat',
            'target_name': kwargs['name'],
            'target_ver': kwargs['version'],
            'target_csv_ver': kwargs['csv_version']
        },
        'results': []
    }

    if 'tag' in kwargs:
        upload_data['common']['tag'] = kwargs['tag']

    results = upload_data['results']

    suite_name = res['suite']
    for sub_suites in res['subSuites']:
        sub_suite_name = sub_suites['name']
        if len(sub_suite_name) > 0:
            prefix = "{}/{}".format(suite_name, sub_suite_name)
        else:
            prefix = suite_name

        for group in sub_suites['results']:
            for case in group['cases']:
                results.append({
                    'name': '{}/{}'.format(prefix, case['case']),
                    'start': case['startTime'],
                    'spend': int(case['usingTime']),
                    'result': _result_map[case['result']]
                })
    return upload_data


def load_result(suite_dir, **kwargs):
    work_dir = WorkDir(suite_dir)
    json_res = work_dir.output.get_yat_json_log()
    if not os.path.exists(json_res):
        raise YatError("Is the suite running before you do this?")

    with open(json_res) as stream:
        return _make_upload_format(json.load(stream), **kwargs)

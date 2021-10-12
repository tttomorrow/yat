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

import yaml
import requests


from yat.errors import YatError
from yat.suite.workdir import WorkDir
from .load_result import load_result


def do_upload(suite_dir, **kwargs):
    work_dir = WorkDir(suite_dir)
    upload_conf = work_dir.get_conf_upload()
    if not os.path.exists(upload_conf):
        raise YatError("upload configure file not found")

    with open(upload_conf) as stream:
        conf = yaml.safe_load(stream)

    url = conf.get('url')
    token = conf.get('api_token')

    headers = {
        'Content-Type': 'application/json',
        'X-Api-Token': token
    }
    data = load_result(suite_dir, **kwargs)

    url = '{}/case/result'.format(url)
    res = requests.post(url, headers=headers, json=data)

    if res.status_code != 200:
        raise YatError("upload test result failed: HTTP CODE = {}, MSG = {}".format(res.status_code, res.text))
    else:
        print("upload test case success: {}".format(res.text))

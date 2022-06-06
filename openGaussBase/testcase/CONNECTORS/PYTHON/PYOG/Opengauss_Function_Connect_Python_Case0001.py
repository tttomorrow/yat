"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

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
Case Type   : python驱动pyog
Case Name   : pip安装驱动
Description :
    1、进入site-packages目录
    2、使用pip安装
Expect      :
    1、成功
    2、成功
History     :
"""
import os
import re
import unittest

from yat.test import Node

from testcase.utils.Logger import Logger


class ConnPython1(unittest.TestCase):
    def setUp(self):
        self.pri_root = Node('PrimaryRoot')
        self.LOG = Logger()
        text = '----Opengauss_Function_Connect_Python_Case0001 start----'
        self.LOG.info(text)

    def test_install(self):
        text = '----step1: 获取site-packages目录 expect: 成功----'
        self.LOG.info(text)
        get_path_cmd = "updatedb; " \
                       "locate site-packages|grep python3|head -1"
        pak_path = os.popen(get_path_cmd).readlines()[0].strip()
        self.LOG.info(pak_path)
        self.assertIsNotNone(pak_path, text)

        text = '----step2: 使用pip安装 expect: 成功----'
        self.LOG.info(text)
        pip_cmd = f"cd {pak_path}; " \
            f"pip3 uninstall py-opengauss -y; " \
            f"pip3 install py-opengauss " \
            f"--trusted-host mirrors.tools.huawei.com " \
            f"-i http://mirrors.tools.huawei.com/pypi/simple"
        self.LOG.info(pip_cmd)
        pip_res = os.popen(pip_cmd).readlines()
        self.LOG.info(pip_res)
        succ_expect = 'Successfully installed py-opengauss'
        regex_res = re.search(succ_expect, ''.join(pip_res), re.S)
        self.assertIsNotNone(regex_res, text)

    def tearDown(self):
        text = '----Opengauss_Function_Connect_Python_Case0001 end----'
        self.LOG.info(text)

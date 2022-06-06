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
Case Type   : go驱动
Case Name   : 安装驱动
Description :
    1.配置go环境变量
    2.安装驱动
Expect      :
    1.执行成功
    2.执行成功
History     :
"""
import os
import unittest

from yat.test import Node

from testcase.utils.ComGo import ComGo
from testcase.utils.Logger import Logger


class ConnGO1(unittest.TestCase):
    def setUp(self):
        self.pri_root = Node('PrimaryRoot')
        self.log = Logger()
        self.go = ComGo()
        self.cur_os = self.pri_root.sh('cat /etc/system-release').result()
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = f'----前置检查：已安装golang1.11.1以上版本----'
        self.log.info(text)
        res = self.go.check_install_go(self.pri_root, '1.11.1')
        self.assertTrue(res, f'执行失败: {text}')

    def test_1(self):
        text = '----step1: 配置go环境变量 expect: 成功----'
        self.log.info(text)
        if 'CentOS' in self.cur_os:
            cmd = 'source /etc/profile;'
        else:
            cmd = ''
        cmd += 'go env -w GO111MODULE=on \n' \
               'go env -w GOPROXY=http://mirrors.tools.huawei.com/goproxy/\n' \
               'go env -w GONOSUMDB=*'
        self.log.info(cmd)
        res = self.pri_root.sh(cmd).result()
        self.log.info(res)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

        text = '----step2: 安装驱动 expect: 成功----'
        self.log.info(text)
        if 'CentOS' in self.cur_os:
            cmd = 'source /etc/profile;'
        else:
            cmd = ''
        cmd += 'go get gitee.com/opengauss/openGauss-connector-go-pq'
        self.log.info(cmd)
        res = self.pri_root.sh(cmd).result()
        self.log.info(res)
        if len(res) > 0:
            self.assertIn('go: downloading', res, f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)

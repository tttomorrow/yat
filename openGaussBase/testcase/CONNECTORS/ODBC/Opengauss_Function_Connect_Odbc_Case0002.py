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
Case Type   : c++驱动odbc
Case Name   : 安装ODBC连接数据库所需驱动
Description :
    1、切换python库为python2，检查动态链接库
    2、使用yum安装odbc/odbc-dev
    3、安装openGauss社区ODBC驱动包
Expect      :
    1、成功
    2、成功
    3、成功
History     :
"""
import os
import re
import unittest
import sys

from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class ConnODBC2(unittest.TestCase):
    def setUp(self):
        self.LOG = Logger()
        text = f'---{os.path.basename(sys.argv[4])} start---'
        self.LOG.info(text)
        self.common = Common()
        self.constant = Constant()
        self.pri_root = Node(node='PrimaryRoot')
        self.local_path = '/usr/local/odbclib'
        self.odbc_pkg = os.path.join(macro.DB_SCRIPT_PATH,
                                     "..", macro.ODBC_NAME)

    def test_install(self):
        text = '---step1: 切换python库为python2 expect: 成功---'
        self.LOG.info(text)
        check_yum_res = self.common.check_yum_python(self.pri_root)
        self.LOG.info(check_yum_res)
        self.assertTrue(check_yum_res, '执行失败' + text)

        text = '---step2: 使用yum安装odbc/odbc-dev expect: 成功---'
        self.LOG.info(text)

        yum_cmd = f"yum remove -y unixODBC; " \
                  f"yum remove -y unixODBC-devel;" \
                  f"yum install -y unixODBC;" \
                  f"yum install -y unixODBC-devel"
        self.LOG.info(yum_cmd)
        yum_res = self.pri_root.sh(yum_cmd).result()
        self.LOG.info(yum_res)
        succ_expect = 'Installed:\n  unixODBC'
        regex_res = re.findall(succ_expect, yum_res, re.S)
        self.LOG.info(regex_res)
        self.assertIsNotNone(regex_res, '执行失败' + text)
        self.assertEqual(2, len(regex_res), '执行失败' + text)

        check_odbc_cmd = f"rpm -qa |egrep ODBC"
        check_res = self.pri_root.sh(check_odbc_cmd).result()
        self.LOG.info(check_res)
        self.assertIn('unixODBC', check_res, '执行失败' + text)
        self.assertIn('unixODBC-devel', check_res, '执行失败' + text)

        text = '---step3: 安装openGauss社区ODBC驱动包 expect: 成功---'
        self.LOG.info(text)
        check_odbc = f"ls {self.odbc_pkg}"
        check_res = self.pri_root.sh(check_odbc).result()
        self.LOG.info(check_res)
        if 'No such file or directory' in check_res:
            self.pri_root.scp_put(self.odbc_pkg, self.odbc_pkg)
        tar_cmd = f"mkdir -p {self.local_path}; " \
                  f"tar -zxvf {self.odbc_pkg} -C {self.local_path} "
        self.LOG.info(tar_cmd)
        tar_res = self.pri_root.sh(tar_cmd).result()
        check_tar = f"ls {os.path.join(self.local_path, 'lib')}"
        check_res = self.pri_root.sh(check_tar).result()
        self.LOG.info(check_res)
        self.assertNotIn("No such file or directory", check_res, text)

    def tearDown(self):
        text = '---Opengauss_Function_Connect_ODBC_Case0002 end---'
        self.LOG.info(text)

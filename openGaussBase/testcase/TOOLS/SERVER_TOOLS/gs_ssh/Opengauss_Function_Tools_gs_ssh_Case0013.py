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
Case Type   : 服务端工具
Case Name   : 在openGauss各主机上执行的linux shell命令名:cal,date命令
Description :
    1.cal命令：显示公历（阳历）日历如只有一个参数，则表示年份(1-9999)，
    如有两个参数，则表示月份和年份
    1.1显示指定年月日期
    1.2显示2013年每个月日历
    1.3将星期一做为第一列,显示前中后三月
    2.date命令：显示或设定系统的日期与时间
    2.1显示当前日期
    2.2显示当前时间
    2.3显示GMT
Expect      :
    1.1.显示正确
    1.2.显示正确
    2.3.显示正确
    2.1.显示正确
    2.2.显示正确
    2.3.显示正确
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Log = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Log.info('----Opengauss_Function_Tools_gs_ssh_Case0013开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        Log.info('------------------显示指定年月日期------------------')
        cal_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "cal 9 1998"'
        Log.info(cal_cmd)
        cal_msg = self.dbuser_node.sh(cal_cmd).result()
        Log.info(cal_msg)
        self.assertIn('September 1998', cal_msg)

        Log.info('------------------显示2013年每个月日历------------------')
        cal_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "cal -y 2013"'
        Log.info(cal_cmd)
        cal_msg = self.dbuser_node.sh(cal_cmd).result()
        Log.info(cal_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, cal_msg)
        self.assertIn('2013', cal_msg)

        Log.info('-----将星期一做为第一列,显示前中后三月-----')
        cal_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "cal -m3"'
        Log.info(cal_cmd)
        cal_msg = self.dbuser_node.sh(cal_cmd).result()
        Log.info(cal_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, cal_msg)

        Log.info('------------------显示当前日期------------------')
        date_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "date +%Y%m%d"'
        Log.info(date_cmd)
        date_msg = self.dbuser_node.sh(date_cmd).result()
        Log.info(date_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, date_msg)

        Log.info('------------------显示当前时间------------------')
        date_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "date"'
        Log.info(date_cmd)
        date_msg = self.dbuser_node.sh(date_cmd).result()
        Log.info(date_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, date_msg)

        Log.info('------------------显示当GMT------------------')
        date_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "date -u"'
        Log.info(date_cmd)
        date_msg = self.dbuser_node.sh(date_cmd).result()
        Log.info(date_msg)
        self.assertIn(self.constant.gs_ssh_success_msg, date_msg)

    def tearDown(self):
        Log.info('----------------无需清理环境-----------------------')
        Log.info('-----Opengauss_Function_Tools_gs_ssh_Case0013执行结束-----')

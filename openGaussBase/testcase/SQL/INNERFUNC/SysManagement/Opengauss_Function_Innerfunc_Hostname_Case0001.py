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
Case Type   : 功能测试
Case Name   : hostname返回当前节点的hostname
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.执行SELECT hostname;返回当前节点的hostname
Expect      :
    步骤 1：数据库状态正常
    步骤 2：返回信息正确
History     :
"""

import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

common = Common()
commonsh = CommonSH('dbuser')
logger = Logger()


class Hostname(unittest.TestCase):

    def setUp(self):
        logger.info("---------------Opengauss_Function_Innerfunc_Hostname_Case0001开始执行-----------------")
        logger.info("-----------查询数据库状态-----------")

        commonsh.ensure_dbstatus_normal()

    def test_hostname(self):
        SqlMdg = commonsh.execut_db_sql('SELECT get_hostname();')

        hostname = commonsh.node.sh('hostname').result()
        logger.info(f'实际执行机的hostname：{hostname}')

        common.equal_sql_mdg(SqlMdg, 'get_hostname', hostname, '(1 row)', flag='1')

    def tearDown(self):
        logger.info('------------------Opengauss_Function_Innerfunc_Hostname_Case0001执行结束---------------')

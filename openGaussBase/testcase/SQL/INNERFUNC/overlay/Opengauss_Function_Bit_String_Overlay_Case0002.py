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
Case Name   : overlay替换位串位置的值（替换参数个数为边界值0/1/最大值/超出最大值）
Description : 描述
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除表防止新建失败
    步骤 3.overlay替换位串位置的值（参数为列、替换参数个数为边界值0/1/最大值/超过最大值）数值校验
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：环境清理成功
    步骤 3：函数返回结果正确
History     : 
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Bit_string_overlay_001(unittest.TestCase):

    def setUp(self):
        logger.info("------------Opengauss_Function_Bit_String_Overlay_Case0002开始执行------------------")
        logger.info("-----------查询数据库状态-----------")
        self.common = Common()
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()
        self.commonsh.ensure_dbstatus_normal()

    def test_bit_string_overlay_0012(self):
        bit_list = [('01111', B'0', '1', '1'), ('0111', B'0', '1', '2'), ('01', B'0', '1', '4'), ('0', B'0', '1', '5'),
                    ('0', B'0', '1', '10')]

        for i in range(len(bit_list)):
            Normal_SqlMdg = self.commonsh.execut_db_sql(
                f"SELECT overlay(B'11111' placing {bit_list[i][1]} from {bit_list[i][2]} for {bit_list[i][3]});")
            logger.info(Normal_SqlMdg)
            self.common.equal_sql_mdg(Normal_SqlMdg, 'overlay', bit_list[i][0], '(1 row)', flag='1')

    def tearDown(self):
        clear_sql = 'DROP table IF EXISTS bit_type_t1;'
        SqlMdg1 = self.commonsh.execut_db_sql(clear_sql)
        logger.info(SqlMdg1)
        logger.info('---------------Opengauss_Function_Bit_String_Overlay_Case0002执行结束-----------------')

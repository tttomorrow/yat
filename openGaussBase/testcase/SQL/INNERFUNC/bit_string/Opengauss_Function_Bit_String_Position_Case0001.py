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
Case Type   : 功能测试
Case Name   : position返回位串所在位置（参数为列、检索位串有一个或多个匹配、检索不到匹配位串、被检索或者检索位串为空）
Description : 描述
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除表防止新建失败
    步骤 3.position返回位串所在位置（参数为列、检索位串有一个或多个匹配、检索不到匹配位串、被检索或者检索位串为空）数值校验
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
common = Common()
commonsh = CommonSH('dbuser')
constant = Constant()


class Bit_string_position(unittest.TestCase):

    def setUp(self):
        logger.info("----------Opengauss_Function_Bit_String_Position_Case0001 开始执行--------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_bit_string_position_001(self):
        sql_cmd = '''DROP table IF EXISTS bit_type_t1;
                    CREATE TABLE bit_type_t1 (BT_COL1 BIT VARYING(5),BT_COL2 BIT VARYING(5));
                    INSERT INTO bit_type_t1 VALUES(B'0001', B'10001');
            '''
        SqlMdg = commonsh.execut_db_sql(sql_cmd)
        logger.info(SqlMdg)
        Normal_SqlMdg1 = commonsh.execut_db_sql("SELECT position(BT_COL1 in BT_COL2) from bit_type_t1;")
        common.equal_sql_mdg(Normal_SqlMdg1, 'position', '2', '(1 row)', flag='1')

    def test_bit_string_position_002(self):
        bit_list = [('2', B'01', B'10101'), ('2', B'11', B'01100000'), ('0', B'0', B'1111111'), ('1', B'', B'01100000'),
                    ('0', B'11', B'')]

        for i in range(len(bit_list)):
            Normal_SqlMdg = commonsh.execut_db_sql(f"SELECT position({bit_list[i][1]} in {bit_list[i][2]});")
            common.equal_sql_mdg(Normal_SqlMdg, 'position', bit_list[i][0], '(1 row)', flag='1')

    def tearDown(self):
        clear_sql = 'DROP table IF EXISTS bit_type_t1;'
        SqlMdg1 = commonsh.execut_db_sql(clear_sql)
        logger.info(SqlMdg1)
        logger.info('-----------Opengauss_Function_Bit_String_Position_Case0001 执行结束---------------')

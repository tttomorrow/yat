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
Case Name   : overlay替换位串位置的值（参数为列、参数起始位为边界值0/1/最大值/超出最大值、被检索位串为空）
Description : 描述
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除表防止新建失败
    步骤 3.overlay替换位串位置的值（参数为列、参数起始位为边界值0/1/最大值/超过最大值、被检索位串为空）数值校验
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：环境清理成功
    步骤 3：返回overlay后的结果正确
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


class Bit_string_overlay(unittest.TestCase):

    def setUp(self):
        logger.info("--------------Opengauss_Function_Bit_String_Overlay_Case0001 开始执行----------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_bit_string_overlay_001(self):
        sql_cmd = '''DROP table IF EXISTS bit_type_t1;
                    CREATE TABLE bit_type_t1 (BT_COL1 BIT VARYING(5),BT_COL2 BIT VARYING(5));
                    INSERT INTO bit_type_t1(BT_COL1) VALUES(B'1111');
            '''
        SqlMdg = commonsh.execut_db_sql(sql_cmd)
        logger.info(SqlMdg)
        Normal_SqlMdg = commonsh.execut_db_sql(
            "SELECT overlay(BT_COL1 placing B'0' from 1 for 3), overlay(BT_COL2 placing B'0' from 1 for 3) from bit_type_t1;")
        logger.info(Normal_SqlMdg)
        common.equal_sql_mdg(Normal_SqlMdg, 'overlay | overlay', '01      |', '(1 row)', flag='1')

    def test_bit_string_overlay_002(self):
        bit_list = [('011', B'0', '1', '3'), ('101', B'0', '2', '3'), ('1110', B'0', '4', '3'),
                    ('11110', B'0', '5', '3'), ('111110', B'0', '10', '3')]

        for i in range(len(bit_list)):
            Normal_SqlMdg1 = commonsh.execut_db_sql(
                f"SELECT overlay(B'11111' placing {bit_list[i][1]} from {bit_list[i][2]} for {bit_list[i][3]});")
            logger.info(Normal_SqlMdg1)
            common.equal_sql_mdg(Normal_SqlMdg1, 'overlay', bit_list[i][0], '(1 row)', flag='1')

    def tearDown(self):
        clear_sql = 'DROP table IF EXISTS bit_type_t1;'
        SqlMdg1 = commonsh.execut_db_sql(clear_sql)
        logger.info(SqlMdg1)
        logger.info('--------------Opengauss_Function_Bit_String_Overlay_Case0001 执行结束----------')

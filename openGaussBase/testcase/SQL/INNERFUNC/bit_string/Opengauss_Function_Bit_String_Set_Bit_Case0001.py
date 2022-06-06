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
Case Name   : set_bit返回位串位置的值（参数为列、位数为边界值0/1/最大值/超过最大值、被检索位串为空）
Description : 描述
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除表防止新建失败
    步骤 3.set_bit返回位串位置的值（参数为列、位数为边界值0/1/最大值/超过最大值、被检索位串为空）数值校验
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：环境清理成功
    步骤 3：函数结果正确
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


class Bit_string_set_bit(unittest.TestCase):

    def setUp(self):
        logger.info("--------------Opengauss_Function_Bit_String_Set_Bit_Case0001 开始执行------------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_bit_string_set_bit_001(self):
        sql_cmd = '''DROP table IF EXISTS bit_type_t1;
                    CREATE TABLE bit_type_t1 (BT_COL1 BIT VARYING(5),BT_COL2 BIT VARYING(5));
                    INSERT INTO bit_type_t1(BT_COL1) VALUES(B'0001');
                    '''
        SqlMdg = commonsh.execut_db_sql(sql_cmd)
        logger.info(SqlMdg)
        Normal_SqlMdg = commonsh.execut_db_sql("SELECT set_bit(BT_COL1,0,1), set_bit(BT_COL2,0,1) from bit_type_t1;")
        logger.info(Normal_SqlMdg)
        common.equal_sql_mdg(Normal_SqlMdg, 'set_bit | set_bit', '1001    |', '(1 row)', flag='1')

    def test_bit_string_set_bit_002(self):
        bit_list = [('01111', '0', '0'), ('10111', '0', '1'), ('11110', '0', '4')]

        for i in range(len(bit_list)):
            Normal_SqlMdg = commonsh.execut_db_sql(f"SELECT set_bit(B'11111',{bit_list[i][2]} , {bit_list[i][1]});")
            logger.info(Normal_SqlMdg)
            common.equal_sql_mdg(Normal_SqlMdg, 'set_bit', bit_list[i][0], '(1 row)', flag='1')

    def test_bit_string_set_bit_003(self):
        Abormal_SqlMdg = commonsh.execut_db_sql(f"SELECT set_bit(B'11111',5 , 0);")
        logger.info(Abormal_SqlMdg)
        self.assertTrue(Abormal_SqlMdg.find('ERROR:  bit index 5 out of valid range (0..4)') > -1)

    def tearDown(self):
        clear_sql = 'DROP table IF EXISTS bit_type_t1;'
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info(SqlMdg)
        logger.info('------------------Opengauss_Function_Bit_String_Set_Bit_Case0001 执行结束----------------')

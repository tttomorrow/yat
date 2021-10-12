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
Case Type   :  功能测试
Case Name   :  关于二进制的表达式测试
Description :
    1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    2.关于二进制的表达式测试
    3.清理环境
Expect      :
    1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    2.关于二进制的表达式测试
    3.清理环境
History     :
"""
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Expression_Case0025开始执行-----------------------------')
        self.Constant = Constant()

    def test_common_user_permission(self):
        # 0007 value和default为同一数据类型，覆盖常用数据类型
        sql_cmd = commonsh.execut_db_sql('''SELECT DECODE('A','A1',B'101'::bit(3),'B',B'10101'::bit(5),B'1010101'::bit(7));''')
        logger.info(sql_cmd)
        self.assertEqual("1010101", sql_cmd.split("\n")[-2].strip())
        sql_cmd = commonsh.execut_db_sql('''SELECT DECODE('A','A','2020-10-13'::timestamp,'B',E'jo\\\\\\001se'::bytea, E'jo\\\\\\007se'::bytea);''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)

        # 0008 NULLIF如果value1等于value2则返回NULL，否则返回value1。
        sql_cmd = commonsh.execut_db_sql('''SELECT NULLIF(E'jo\\\\\\000se'::bytea,E'jo\\\\\\000ae'::bytea);''')
        logger.info(sql_cmd)
        self.assertIn('\\x6a6f007365', sql_cmd)

        # 0008
        sql_cmd = commonsh.execut_db_sql('''SELECT NULLIF(B'10101'::bit(5),B'10101'::bit(5));''')
        logger.info(sql_cmd)
        self.assertTrue(sql_cmd.splitlines()[2].strip() == '')
        sql_cmd = commonsh.execut_db_sql('''SELECT NULLIF(E'jo\\\\\\000se'::bytea,E'jo\\\\\\000se'::bytea);''')
        logger.info(sql_cmd)
        self.assertTrue(sql_cmd.splitlines()[2].strip() == '')
        sql_cmd = commonsh.execut_db_sql('''SELECT NULLIF(E'jo\\\\\\000se'::bytea,B'10101'::bit(5));''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1],sql_cmd)

        # 可进行比较
        sql_cmd = commonsh.execut_db_sql('''SELECT greatest(B'101'::bit(3),B'111'::bit(3),B'10101'::bit(5)) as result;
        SELECT least(B'101'::bit(3),B'111'::bit(3),B'10101'::bit(5)) as result;''')
        logger.info(sql_cmd)
        self.assertIn('101', sql_cmd)
        self.assertIn('111', sql_cmd)

        # 0009 --无法比较:合理报错
        sql_cmd = commonsh.execut_db_sql('''
                                    SELECT greatest(empty_blob(),HEXTORAW('DEADBEEF'),E'\\\\\\xDEADBEEF'::BYTEA) as result;
                                    SELECT least(empty_blob(),HEXTORAW('DEADBEEF'),E'\\\\\\xDEADBEEF'::BYTEA) as result;
                                    SELECT greatest(HEXTORAW('DEADBEEF'),E'\\\\\\xDEADBEEF'::BYTEA) as result;
                                    SELECT least(HEXTORAW('DEADBEEF'),E'\\\\\\xDEADBEEF'::BYTEA) as result;
                                    ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertNotIn("row", sql_cmd)

        # 0010 value和default为同一数据类型
        sql_cmd = commonsh.execut_db_sql('''SELECT DECODE('A','A',E'jo\\\\\\000se'::bytea,'B',E'jo\\\\\\001se'::bytea, E'jo\\\\\\007se'::bytea);''')
        logger.info(sql_cmd)
        self.assertTrue(sql_cmd.splitlines()[2].strip() == "\\x6a6f007365")
         #0011 多参均不为null
        sql_cmd = commonsh.execut_db_sql('''
        SELECT COALESCE(B'10101'::bit(5)); 
        SELECT COALESCE('test',1,1::int,'test'::varchar,'test'::clob,
        'test'::text,'2020-10-13'::timestamp,B'10101'::bit(5),'false'::boolean,
        inet '0.0.5.0/24'::cidr,lseg '(1,2),(3,2)',E'\\\\xDEADBEEF'::BYTEA);
        SELECT COALESCE(E'\\\\\\xDEADBEEF'::BYTEA);
        ''')
        logger.info(sql_cmd)
        self.assertIn('10101', sql_cmd)
        self.assertIn('COALESCE types integer and character varying cannot be matched', sql_cmd)
        self.assertIn('\\xdeadbeef', sql_cmd)
        # 不支持的数据类型 合理报错
        sql_cmd = commonsh.execut_db_sql('''
                                    SELECT nvl(null,E'\\\\xDEADBEEF'::BYTEA);
                                    ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertNotIn("row", sql_cmd)


    # 清理环境
    def tearDown(self):
        logger.info('------------------------no need to clean--------------------------')
        logger.info('------------------------Opengauss_Function_Expression_Case0025执行结束--------------------------')
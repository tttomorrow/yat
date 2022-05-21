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
'''

Case Type： 功能测试
Case Name： substr入参正常对bytea进行截取
Descption:substr(string, from int [, for int])截取子串。

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境，设置参数
步骤 3.substr的入参是二进制字符串
'''
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

class byte_string_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_Function_Binarystring_Substr_Case0001开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_substr(self):

        logger.info("-----------from超范围返回'-----------")
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'Th\\\\\\000omas'::bytea , 88 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg1)
        self.assertTrue(Normal_SqlMdg1.splitlines()[3].strip() == '')

        logger.info("-----------for 超范围取到末尾-----------")
        Normal_SqlMdg2 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'Th\\\\\\000omas'::bytea , 3 , 89) AS RESULT;""")
        logger.info(Normal_SqlMdg2)
        self.assertTrue(Normal_SqlMdg2.splitlines()[3].strip(' ') == '\\000omas')

        logger.info("-----------from、for是小数四舍五入-----------")
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'Th\\\\\\000omas'::bytea , 2.3 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[3].strip(' ') == 'h\\000o')
        Normal_SqlMdg3 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'Th\\\\\\000omas'::bytea , 3 , 3.6) AS RESULT;""")
        logger.info(Normal_SqlMdg3)
        self.assertTrue(Normal_SqlMdg3.splitlines()[3].strip(' ') == '\\000oma')

        logger.info("-----------from是负倒数来，不同于pg-----------")
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'Th\\\\\\000omas'::bytea , -2.3 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[3].strip(' ') == 'as')
        Normal_SqlMdg4 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'Th\\\\\\000omas'::bytea , -2.6 , 5) AS RESULT;""")
        logger.info(Normal_SqlMdg4)
        self.assertTrue(Normal_SqlMdg4.splitlines()[3].strip(' ') == 'mas')

        logger.info("-----------from=0，转为1，不同于pg-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'josejosejose'::bytea , 0 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == 'jos')

        logger.info("-----------for=0,返回''-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'josejosejose'::bytea , 1 , 0) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip() == '')

        logger.info("-----------省略for,截取到结尾-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        select substr(E'Th\\\\\\000omas'::bytea,2) as result;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == 'h\\000omas')

        logger.info("-----------from、for>0-----------")
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'\\x5402036d6173' , 2 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == '020')
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(E'jose\\\\\\000\\\\\\000\\\\\\0000jose\\\\\\00000\\\\\\000000jose'::bytea , 2 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == 'ose')
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(left('ABCDEFGHIJK', 6)::bytea , 2 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == 'BCD')
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(overlay(E'Th\\\\\\000omas'::bytea placing E'\\\\\\002\\\\\\003'::bytea from 2 for 3) , 2 , 3) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == '\\002\\003m')
        Normal_SqlMdg5 = self.commonsh.execut_db_sql("""set bytea_output to 'escape';
        SELECT substr(lpad('1open', 5000, 'gauss')::bytea , 4998 , 4) AS RESULT;""")
        logger.info(Normal_SqlMdg5)
        self.assertTrue(Normal_SqlMdg5.splitlines()[3].strip(' ') == 'pen')

    def tearDown(self):
        SqlMdg2 = self.commonsh.execut_db_sql('''set bytea_output to 'hex';''')
        logger.info(SqlMdg2)
        logger.info('------------------------Opengauss_Function_Binarystring_Substr_Case0001执行结束--------------------------')
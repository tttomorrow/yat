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
Case Type   : GUC
Case Name   : 使用set方法在兼容TD数据库中设置参数td_compatible_truncation
              值为on，建表验证
Description :
        1.创建兼容TD的数据库
        2.默认off下，建表插入数据，超过指定长度
        3.修改参数为on，建表插入数据，超过指定长度
        4.清理环境
Expect      :
        1.创建兼容TD的数据库成功
        2.建表成功，插入数据报错
        3.插入成功，超过指定长度会截取
        4.清理环境完成
"""
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

commonsh = CommonSH('PrimaryDbUser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-------Opengauss_Function_Guc_VPC_Case0015start-------')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_User_Node = Node('PrimaryDbUser')

    def test_td_compatible_truncation(self):
        self.log.info('---步骤1:创建兼容TD的数据库---')
        sql_cmd = commonsh.execut_db_sql('''drop database if exists testdb;
            create database testdb DBCOMPATIBILITY ='C';''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        self.log.info('---步骤2:默认off下，建表插入数据，超过指定长度，会报错---')
        sql_cmd = '''show  td_compatible_truncation;\
                   drop table if exists test15 cascade;
                   create table test15 (ct_col1 character(4));\
                   insert into test15 values ('hellowo');'''
        self.log.info(sql_cmd)
        excute_cmd = f'''source {self.DB_ENV_PATH};
            gsql -d testdb \
            -p {self.Primary_User_Node.db_port} \
            -c "{sql_cmd}"'''
        self.log.info(excute_cmd)
        msg = self.Primary_User_Node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, msg)
        self.assertIn('ERROR:  value too long for type character(4)', msg)
        self.log.info('---步骤3:修改参数为on，建表插入数据，超过指定长度，会截取-')
        sql_cmd = '''set td_compatible_truncation to on;\
            drop table if exists test15_bak cascade;
            create table test15_bak (ct_col1 character(4));\
            insert into test15_bak values ('hellowo');'''
        self.log.info(sql_cmd)
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gsql -d testdb\
            -p {self.Primary_User_Node.db_port} \
            -c "{sql_cmd}"'''
        self.log.info(excute_cmd)
        msg = self.Primary_User_Node.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.SET_SUCCESS_MSG, msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg)

    def tearDown(self):
        self.log.info('---步骤5:清理环境---')
        sql_cmd = commonsh.execut_db_sql('''drop database if exists testdb;''')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Guc_VPC_Case0015finish-----')

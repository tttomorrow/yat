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
Case Type   : security-auditing
Case Name   : 关闭启数据库对象table的CREATE、DROP、ALTER操作审计功能，
                audit_system_object=15
Description :
    1.设置gs_guc reload -N all -I all -c  "audit_system_object=7"
    2.登录数据库，创建table对象，CREATE table table02(name char(10));
    3.修改table对象，ALTER table table02 add(id int) ;
    4.清理表，truncate table table02 ;
    5.删除table  对象，drop table table02;
    6.登录数据库，查看审计日志SELECT * FROM pg_query_audit('$start_time',
    '$end_time');时间设在最接近登录数据库的时间
Expect      :
    1.设置成功
    2.创建成功
    3.修改成功
    4.清理成功
    5.删除成功
    6.未查询到创建、修改、清理、删除table的信息
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0040 start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f'gs_guc reload -N all -I all -c "audit_system_object=7"'
        msg1 = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg1)
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd2 = 'create table table02(name char(10));' \
                   'alter table table02 add(id int);' \
                   'truncate table table02;' \
                   'drop table table02;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'CREATE TABLE', 'ALTER TABLE',
                                  'TRUNCATE TABLE', 'DROP TABLE')
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\');'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertFalse(
            msg3.find('create table table02(name char(10));') > -1)
        self.assertFalse(msg3.find('alter table table02 add(id int)') > -1)
        self.assertFalse(msg3.find('truncate table table02') > -1)
        self.assertFalse(msg3.find('drop table table02;') > -1)

    def tearDown(self):
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"audit_system_object=12295"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0040 end----')

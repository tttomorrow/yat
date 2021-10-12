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
Case Name   : 关闭数据库对象TRIGGER的CREATE、DROP、ALTER操作审计功能，
                audit_system_object=63
Description :
    1.设置gs_guc reload -N all -I all -c  "audit_system_object=63"
    2.登录数据库，创建TRIGGER对象，CREATE TRIGGER insert_trigger
               BEFORE INSERT ON test_trigger_src_tbl
               FOR EACH ROW
               EXECUTE PROCEDURE tri_insert_func();
    3.修改TRIGGER对象，ALTER TRIGGER insert_triggerON test_trigger_src_tbl
    RENAME TO insert_trigger_renamed;
    4.删除TRIGGER对象，DROP TRIGGER insert_trigger_renamed ON
    test_trigger_src_tbl;
    5.登录数据库，查看审计日志SELECT * FROM pg_query_audit('$start_time',
    '$end_time');时间设在最接近登录数据库的时间
Expect      :
    1.设置成功
    2.创建成功
    3.修改成功
    4.删除成功
    5.未查询到创建、删除TRIGGER的信息
History     :
"""
import unittest
from time import sleep
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '------Opengauss_Function_Security_Auditing_Case0044 start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        

    def test_security(self):
        excute_cmd = f'source {self.DB_ENV_PATH};' \
                     f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                     f'"audit_system_object=63"'
        msg1 = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg1)
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        sleep(5)
        sql_cmd2 = '''CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, 
        id3 INT);CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);

            CREATE OR REPLACE FUNCTION tri_insert_func() RETURNS TRIGGER AS
            \$\$
            DECLARE
            BEGIN
                INSERT INTO test_trigger_des_tbl VALUES(NEW.id1, NEW.id2, 
                NEW.id3);
                RETURN NEW;
            END
            \$\$ LANGUAGE PLPGSQL;
            CREATE TRIGGER insert_trigger
               BEFORE INSERT ON test_trigger_src_tbl
               FOR EACH ROW
               EXECUTE PROCEDURE tri_insert_func();
            ALTER TRIGGER insert_trigger ON test_trigger_src_tbl RENAME TO 
            insert_trigger_renamed;
            DROP TRIGGER insert_trigger_renamed ON test_trigger_src_tbl;
            DROP FUNCTION tri_insert_func();
            DROP TABLE test_trigger_src_tbl;
            DROP TABLE test_trigger_des_tbl;
            '''
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\');'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertFalse(msg3.find('CREATE TRIGGER insert_trigger') > -1)
        self.assertFalse(
            msg3.find('ALTER TRIGGER insert_trigger ON test_trigger_src_tbl '
                      'RENAME TO insert_trigger_renamed') > -1)
        self.assertFalse(msg3.find('DROP TRIGGER insert_trigger_renamed ON '
                                   'test_trigger_src_tbl') > -1)

    def tearDown(self):
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                      f'"audit_system_object=12295"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0044 end----')

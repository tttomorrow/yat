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
Case Type   : 触发器
Case Name   : 只有触发器所在表的所有者可以执行ALTER TRIGGER操作
Description :
    1.创建表：CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);
    2.创建触发器函数：CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS
    TRIGGER AS
     $$
    DECLARE
    BEGIN
    INSERT INTO test_trigger_des_tbl0 VALUES(NEW.id1, NEW.id2, NEW.id3);
         RETURN NEW;
    END
    $$ LANGUAGE PLPGSQL;
    3.创建触发器CREATE TRIGGER insert_trigger01 BEFORE INSERT ON
    test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
    4.修改触发器名：ALTER TRIGGER insert_trigger01 ON test_trigger_src_tbl0
    RENAME TO new_insert_trigger01;
Expect      :
    1.创表成功
    2.触发器函数创建成功
    3.触发器创建成功
    4.无权限修改
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Trigger(unittest.TestCase):
    def setUp(self):
        logger.info('-------Opengauss_Function_Trigger_Case0027 start-----')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()

    def test_trigger(self):
        logger.info('----------创建触发器 -----------')
        sql_cmd1 = f'CREATE USER wf WITH password \'{macro.COMMON_PASSWD}\';' \
                   f'CREATE TABLE test_trigger_src_tbl0(id1 INT, id2 INT, ' \
                   f'id3 INT);' \
                   f'CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, ' \
                   f'id3 INT);' \
                   f'CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS ' \
                   f'TRIGGER AS ' \
                   f'\$\$ ' \
                   f'DECLARE ' \
                   f'BEGIN ' \
                   f'INSERT INTO test_trigger_des_tbl0 VALUES(NEW.id1,' \
                   f' NEW.id2, NEW.id3);' \
                   f'RETURN NEW;' \
                   f'END ' \
                   f'\$\$ LANGUAGE PLPGSQL;' \
                   f'CREATE TRIGGER insert_trigger01 BEFORE INSERT ON ' \
                   f'test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE ' \
                   f'tri_insert_func01();'
        sql_cmd2 = 'ALTER TRIGGER insert_trigger01 ON test_trigger_src_tbl0 ' \
                   'RENAME TO new_insert_trigger01;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U  wf -W \'' \
                      f'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertTrue(msg2.find('must be owner of relation') > -1)

    def tearDown(self):
        logger.info('-----------清理资源-----------')
        sql_cmd1 = 'DROP TRIGGER insert_trigger01 ON test_trigger_src_tbl0;' \
                   'DROP FUNCTION tri_insert_func01() cascade;' \
                   'DROP TABLE test_trigger_src_tbl0;' \
                   'DROP TABLE test_trigger_des_tbl0;' \
                   'DROP USER wf;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('------Opengauss_Function_Trigger_Case0027 finish------')

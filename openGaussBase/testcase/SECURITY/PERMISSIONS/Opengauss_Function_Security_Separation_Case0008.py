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
Case Type   : security-Separation_rights
Case Name   : 三权分立后系统管理员对表有操作权限
Description :
    1.初始用户执行：CREATE USER sysadmin01 WITH SYSADMIN password 'Qazwsx@123';
    2.sysadmin01 用户执行：create table table01(id1 int,id2 int,id3 int);
    INSERT INTO table01 VALUES(2,3,5);
    SELECT * FROM table01 where id=2;
    update table01 set id2=22;
    delete from table01 where id3=5;
    ALTER TABLE table01 add01(id4 int);
Expect      :
    1.CREATE ROLE
    2.CREATE TABLE
    INSERT
    查询出表内容正确
    UPDATE
    DELETE
    ALTER TABLE
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


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info(
            '-----Opengauss_Function_Security_Separation_Case0008 start----')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info('-------------create user ------------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -D {macro.DB_INSTANCE_PATH} -c ' \
                      f'"enableSeparationOfDuty=on"' \
                      f'gs_om -t stop && gs_om -t start'
        msg0 = self.userNode.sh(excute_cmd0).result()
        logger.info(msg0)
        sql_cmd1 = f'CREATE USER sysadmin01 WITH SYSADMIN password ' \
                   f'\'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        sql_cmd2 = 'create table table01(id1 int,id2 int,id3 int);' \
                   'INSERT INTO table01 VALUES(2,3,5);' \
                   'SELECT * FROM table01 where id1=2;' \
                   'update table01 set id2=22;' \
                   'delete from table01 where id3=5;' \
                   'ALTER TABLE table01 add(id4 int);'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U sysadmin01 -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertTrue(msg2.find('CREATE TABLE') > -1)
        self.assertTrue(msg2.find('INSERT') > -1)
        self.assertTrue(msg2.find('2') > -1)
        self.assertTrue(msg2.find('DELETE') > -1)
        self.assertTrue(msg2.find('ALTER TABLE') > -1)

    def tearDown(self):
        logger.info('-----------恢复配置，并清理环境-----------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -D {macro.DB_INSTANCE_PATH}' \
                      f' -c "enableSeparationOfDuty=off";' \
                      f'gs_om -t stop && gs_om -t start'
        msg0 = self.userNode.sh(excute_cmd0).result()
        logger.info(msg0)
        sql_cmd1 = 'DROP TABLE IF EXISTS table01;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U sysadmin01 -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd1}"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        sql_cmd2 = 'DROP USER sysadmin01;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        logger.info(
            '-----Opengauss_Function_Security_Separation_Case0008 finish-----')

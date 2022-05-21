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
Case Type   : security-auditing
Case Name   : 关闭具体表的DML操作（SELECT除外）审计功能，设置audit_dml_state=0
Description :
            1.设置gs_guc reload -N all -I all -c "audit_dml_state=0"
            2.创建表table003,create table table003(id int,name char(10));
            3.给表中插入数据，insert into table003 values(3,'liming')
            4更新数据，update table003 set id=5;
            5.删除数据，delete from table003 where id=5;
            6.删除表，drop table table003；
            7.登录数据库，查看审计日志SELECT * FROM pg_query_audit('$start_time',
            '$end_time');时间设在最接近登录数据库的时间
Expect      :
            1.设置成功
            2.创建成功
            3.数据插入完成
            4.更新完成
            5.删除成功
            6.表删除成功
            7.未查询到DML操作的信息
History     :
"""
import unittest
import datetime
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0072 start------')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        excute_cmd1 = f'show audit_dml_state;'
        msg1 = self.sh_primy.execut_db_sql(excute_cmd1)
        self.logger.info(msg1)
        self.common.equal_sql_mdg(msg1, 'audit_dml_state', '0', '(1 row)',
                                  flag='1')
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd2 = 'create table table003(id int,name char(10));' \
                   'insert into table003 values(3,\'liming\');' \
                   'update table003 set id=5;' \
                   'delete from table003 where id=5;' \
                   'drop table table003;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'''select * from pg_query_audit('{start_time}','{end_time}');'''
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertFalse(
            msg3.find('insert into table003 values(3,\'liming\')') > -1)
        self.assertFalse(msg3.find('update table003 set id=5') > -1)
        self.assertFalse(msg3.find('delete from table003 where id=5') > -1)

    def tearDown(self):
        self.logger.info(
            '------Opengauss_Function_Security_Auditing_Case0072 end------')

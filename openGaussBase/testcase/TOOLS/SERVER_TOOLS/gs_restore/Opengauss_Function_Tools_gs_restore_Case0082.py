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
Case Type   : 服务端工具
Case Name   : 指定导入操作使用的角色名，不指定具体角色用户的角色密码
Description :
    1.创建数据
    2.导出数据
    3.导入数据
    4.清理环境
Expect      :
    1.创建数据成功
    2.导出数据成功
    3.导入数据失败
    4.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.root_user = Node('default')
        self.commonsh = CommonSH('dbuser')
        self.db_name = 'db_test'
        self.table_name = 't_gs_restore_Case0082'
        self.user_name = 'u_gs_restore_Case0082'
        self.role_name = 'rl_gs_restore_Case0082'
        self.tablespace_name = 'tsp_gs_restore_Case0082'
        self.function_name = 'f_gs_restore_Case0082'
        self.schema_name = 's_gs_restore_Case0082'

    def test_server_tools1(self):
        self.log.info("--Opengauss_Function_Tools_gs_restore_Case0082开始执行--")
        text = "-----创建数据;expect:创建成功-----"
        self.log.info(text)
        sql = f'create database {self.db_name};'
        sql_cmd = self.commonsh.execut_db_sql(sql,
                                              dbname=self.dbuser_node.db_name)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        sql = f'''create table {self.table_name} (id int,name char(20));
            insert into {self.table_name} values(1,'xixi'),\
            (2,'haha'),(3,'hehe');
            create user {self.user_name} identified by\
            '{macro.PASSWD_REPLACE}';
            create role {self.role_name} identified by \
            '{macro.PASSWD_REPLACE}';
            create tablespace {self.tablespace_name} relative \
            location 'tablespace/tablespace_1';
            alter tablespace {self.tablespace_name} rename to ds_location3;
            create schema {self.schema_name};
            create function {self.function_name}(i integer)
            returns integer
            as \$$
            begin
                return i+1;
            end;
            \$$ language plpgsql;
            select * from {self.table_name};
            '''
        sql_cmd = self.commonsh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行成功' + text)
        self.assertIn('3 rows', sql_cmd, '执行成功' + text)

        text = "----导出tar格式文件;expect:创建成功----"
        self.log.info(text)
        dump_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_dump -p {self.dbuser_node.db_port}  " \
            f"{self.db_name}  " \
            f"-f {macro.DB_INSTANCE_PATH}/test.tar -F t "
        self.log.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg,
                      '执行成功' + text)

        text = "---导入之前导出的数据,提示输入密码时,输入错误密码;" \
               "expect:导入失败;"
        self.log.info(text)
        dumpall_cmd = f'''source {macro.DB_ENV_PATH};
                   expect <<EOF
                   set timeout -1
                   spawn gs_restore -p {self.dbuser_node.db_port}  \
                   -d {self.db_name} -U {self.user_name} -W \
                    {macro.PASSWD_REPLACE} \
                    {macro.DB_INSTANCE_PATH}/test.tar  --role=role1
                       expect {{{{
                           "*assword:" {{{{ send mima@5566"\r"; \
                           exp_continue }}}}
                           eof {{{{ send_user "执行成功！\n" }}}}
                       }}}}\n''' + "EOF"
        self.log.info(dumpall_cmd)
        dumpall_result = self.dbuser_node.sh(dumpall_cmd).result()
        self.log.info(dumpall_result)
        self.assertIn(f'failed: FATAL:  '
                      f'Invalid username/password,login denied.',
                      dumpall_result, '执行失败:' + text)

        text = "---查看数据是否导入;expect:数据查看成功，未导入---"
        sql = f'select * from {self.table_name};'
        sql_cmd = self.commonsh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(sql_cmd)
        self.assertIn('3 rows', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = "---清理环境;expect:清理环境成功----"
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'drop database '
                                              f'{self.db_name};'
                                              f'drop tablespace '
                                              f'ds_location3;'
                                              f'revoke all privileges '
                                              f'from {self.user_name};'
                                              f'drop user {self.user_name};'
                                              f'drop role {self.role_name};')
        self.log.info(sql_cmd)
        rm_cmd = f"rm -rf {macro.DB_INSTANCE_PATH}/test.tar"
        self.log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info("-Opengauss_Function_Tools_gs_restore_Case0082执行结束-")

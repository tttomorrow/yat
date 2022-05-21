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
Case Name   : 指定导入操作使用的角色名，并指定具体角色用户的角色密码
Description :
    1.创建数据
    2.导出数据
    3.删除表
    4.导入数据
    5.校验数据是否导入
    6.清理环境
Expect      :
    1.创建数据成功
    2.导出数据成功
    3.删除表成功
    4.导入数据失败
    5.校验数据成功，数据未导入
    5.清理环境成功
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-Opengauss_Function_Tools_gs_restore_Case0083 开始执行-")
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.root_user = Node('default')
        self.commonsh = CommonSH('dbuser')
        self.db_name = 'd_gs_restore_case0083'
        self.table_name = 't_gs_restore_case0083'
        self.user_name = 'u_gs_restore_case0083'
        self.role_name = 'r_gs_restore_case0083'
        self.tablespace_name = 'tbspc_gs_restore_case0083'
        self.tablespace_rename = 're_tbspc_gs_restore_case0083'
        self.schema_name = 's_gs_restore_case0083'
        self.func_name = 'f_gs_restore_case0083'

    def test_server_tools1(self):
        text1 = '-----step1.创建数据; expect:创建数据成功-----'
        self.log.info(text1)
        sql = f'create database {self.db_name};'
        sql_cmd = self.commonsh.execut_db_sql(sql)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text1)
        sql = f'''create table {self.table_name} (id  int,name char(20));
            insert into {self.table_name} values(1,'xixi'),\
            (2,'haha'),(3,'hehe');
            create user {self.user_name} identified by \
            '{macro.PASSWD_REPLACE}';
            create role  {self.role_name} identified by \
            '{macro.PASSWD_REPLACE}';
            create tablespace {self.tablespace_name} relative \
            location 'tablespace/tablespace_1';
            alter tablespace {self.tablespace_name} rename to \
            {self.tablespace_rename};
            create schema {self.schema_name};
            create function {self.func_name}(i integer)
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
        assert_1 = self.constant.TABLE_CREATE_SUCCESS in sql_cmd
        assert_2 = self.constant.CREATE_ROLE_SUCCESS_MSG in sql_cmd
        assert_3 = sql_cmd.count(self.constant.CREATE_ROLE_SUCCESS_MSG) == 2
        assert_4 = self.constant.TABLESPCE_CREATE_SUCCESS in sql_cmd
        assert_5 = self.constant.TABLESPCE_ALTER_SUCCESS in sql_cmd
        assert_6 = self.constant.CREATE_SCHEMA_SUCCESS_MSG in sql_cmd
        assert_7 = self.constant.CREATE_FUNCTION_SUCCESS_MSG in sql_cmd
        assert_8 = '3 rows' in sql_cmd
        self.assertTrue(assert_1 and assert_2 and assert_3 and assert_4
                        and assert_5 and assert_6 and assert_7 and assert_8,
                        '执行失败:' + text1)

        text2 = '-----step2.导出数据; expect:导出tar格式文件成功-----'
        self.log.info(text2)
        dump_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_dump -p {self.dbuser_node.db_port} " \
            f"{self.db_name}  -f " \
            f"{os.path.join(f'{macro.DB_INSTANCE_PATH}', 'gs_restore.tar')} " \
            f"-F t"
        self.log.info(dump_cmd)
        dump_msg = self.dbuser_node.sh(dump_cmd).result()
        self.log.info(dump_msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, dump_msg,
                      '执行失败:' + text2)

        text3 = '-----step3.删除表; expect:删除表成功-----'
        self.log.info(text3)
        sql_cmd = self.commonsh.execut_db_sql(f"drop table "
                                              f"{self.table_name};",
                                              dbname=self.db_name)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_cmd,
                      '执行失败:' + text3)

        text4 = '-----step4.导入之前导出的数据; expect:校验数据成功，导入数据失败-----'
        self.log.info(text4)
        restore_cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gs_restore -p {self.dbuser_node.db_port} " \
            f"-d {self.db_name} -U {self.user_name} " \
            f"-W {macro.PASSWD_REPLACE} " \
            f"{os.path.join(f'{macro.DB_INSTANCE_PATH}', 'gs_restore.tar')}" \
            f" --role={self.role_name} --rolepassword={macro.PASSWD_REPLACE}"
        self.log.info(restore_cmd)
        restore_msg = self.dbuser_node.sh(restore_cmd).result()
        self.log.info(restore_msg)
        self.assertIn('ERROR:  permission denied', restore_msg,
                      '执行失败:' + text4)
        assert_1 = restore_msg.count('ERROR:  permission denied') == 5
        self.assertTrue(assert_1, '执行失败:' + text4)

        text5 = '-----step5.校验表数据是否导入; expect:表数据未导入-----'
        self.log.info(text5)
        sql_cmd = self.commonsh.execut_db_sql(f"select * from "
                                              f"{self.table_name};",
                                              dbname=self.db_name)
        self.log.info(sql_cmd)
        self.assertIn(f'ERROR:  relation "{self.table_name}" '
                      f'does not exist', sql_cmd, '执行失败:' + text5)

    def tearDown(self):
        text6 = '-----step6.清理环境; expect:清理环境成功-----'
        self.log.info(text6)
        sql_cmd = self.commonsh.execut_db_sql(f'drop database '
                                              f'{self.db_name};'
                                              f'drop tablespace '
                                              f'{self.tablespace_rename};'
                                              f'drop user {self.user_name};'
                                              f'drop role {self.role_name};')
        self.log.info(sql_cmd)
        rm_cmd = f"rm -rf " \
            f"{os.path.join(f'{macro.DB_INSTANCE_PATH}', 'gs_restore.tar')}"
        self.log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        assert_1 = self.constant.DROP_DATABASE_SUCCESS in sql_cmd
        assert_2 = self.constant.TABLESPCE_DROP_SUCCESS in sql_cmd
        assert_3 = self.constant.DROP_ROLE_SUCCESS_MSG in sql_cmd
        assert_4 = sql_cmd.count(self.constant.DROP_ROLE_SUCCESS_MSG) == 2
        assert_5 = '' in sql_cmd
        self.assertTrue(assert_1 and assert_2 and assert_3
                        and assert_4 and assert_5, '执行失败:' + text6)
        self.log.info("-Opengauss_Function_Tools_gs_restore_Case0083 执行结束-")

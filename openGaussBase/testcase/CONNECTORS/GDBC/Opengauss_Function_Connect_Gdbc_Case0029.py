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
Case Type   : go驱动
Case Name   : 连接数据库，设置默认权限
Description :
    1.新建用户并赋权
    2.配置pg_hba入口, sha256认证方法
    3.连接数据库，设置默认权限
    4.还原pg_hba文件
    5.删除用户
    6.刪除go_conn.go
Expect      :
    1.执行成功
    2.执行成功
    3.执行成功，回显无panic提示
    4.执行成功
    5.执行成功
    6.执行成功
History     :
"""
import os
import re
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.ComGo import ComGo
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnGO29(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.log = Logger()
        self.go = ComGo()
        self.cons = Constant()
        self.db_user = 'go_user_29'
        self.go_file = 'go_conn.go'
        self.t_name = 't_go_29'
        self.schema_name = 'schema_go_29'
        self.cur_os = self.pri_root.sh('cat /etc/system-release').result()
        self.pg_hba_path = os.path.join(macro.DB_INSTANCE_PATH,
                                        macro.PG_HBA_FILE_NAME)
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = f'----前置检查：已安装golang1.11.1以上版本----'
        self.log.info(text)
        res = self.go.check_install_go(self.pri_user, '1.11.1')
        self.assertTrue(res, f'执行失败: {text}')

    def test_1(self):
        text = '----step1: 新建用户并赋权 expect: 成功----'
        self.log.info(text)
        sql = f"drop user if exists {self.db_user} cascade;" \
            f"create user {self.db_user} with login password " \
            f"'{macro.COMMON_PASSWD}';" \
            f"drop schema if exists {self.schema_name};" \
            f"create schema {self.schema_name} authorization " \
            f"{self.db_user};" \
            f"alter default privileges in schema {self.schema_name} grant " \
            f"all privileges on tables to {self.db_user};"
        self.log.info(sql)
        res = self.pri_sh.execut_db_sql(sql)
        self.log.info(res)
        expect = f'{self.cons.DROP_ROLE_SUCCESS_MSG}.*' \
            f'{self.cons.CREATE_ROLE_SUCCESS_MSG}.*' \
            f'{self.cons.DROP_SCHEMA_SUCCESS_MSG}.*' \
            f'{self.cons.CREATE_SCHEMA_SUCCESS_MSG}.*' \
            f'{self.cons.ALTER_DEFAULT_PRIVILEGES}'
        reg_res = re.search(expect, res, re.S)
        self.assertIsNotNone(reg_res, f'执行失败: {text}')

        text = '----step2: 配置pg_hba入口 expect: 成功----'
        self.log.info(text)
        cmd = f'cp {self.pg_hba_path} {self.pg_hba_path}_bak && ' \
            f'source {macro.DB_ENV_PATH} && ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.pri_user.db_name} {self.db_user} ' \
            f'{self.pri_user.ssh_host}/32 sha256"'
        self.log.info(cmd)
        res = self.pri_user.sh(cmd).result()
        self.log.info(res)
        self.assertIn(self.cons.GSGUC_SUCCESS_MSG, res, f'执行失败: {text}')

        text = '----step3: 连接数据库，设置默认权限 expect: 成功----'
        self.log.info(text)
        conn_str = f'connStr := "host={self.pri_user.db_host} ' \
            f'port={self.pri_user.db_port} ' \
            f'user={self.db_user} ' \
            f'password={macro.COMMON_PASSWD} ' \
            f'dbname={self.pri_user.db_name} ' \
            f'sslmode=disable"'

        clean_sql = f"drop table if exists {self.schema_name}.{self.t_name}" \
            f" cascade;"
        s_sql = f"{clean_sql}" \
            f"create table {self.schema_name}.{self.t_name}(a int, b text);" \
            f"insert into {self.schema_name}.{self.t_name} values (" \
            f"generate_series(1,100000),generate_series(1,100000)||'test');" \
            f"delete from {self.schema_name}.{self.t_name} where a<100;" \
            f"update {self.schema_name}.{self.t_name} set b=b||'new';"
        query_sql = f"select count(*) from {self.schema_name}.{self.t_name};"
        f_contant = f'{self.go.get_head()}\n\n' \
            f'func cleanup(db *sql.DB) {{\n' \
            f'    {self.go.exec_sql(clean_sql)}' \
            f'\n\n    db.Close()\n' \
            f'}}\n\n' \
            f'func main() {{\n' \
            f'    {conn_str}\n' \
            f'    {self.go.conndb("connStr")}\n\n' \
            f'    defer cleanup(db)\n\n' \
            f'    {self.go.exec_sql(s_sql)}\n\n' \
            f'    {self.go.query_row(query_sql, **{"num": "int"})}\n' \
            f'}}'
        cmd = f'cat > {self.go_file} <<EOF\n' \
            f'{f_contant}\n' \
            f'EOF\n'
        if 'CentOS' in self.cur_os:
            cmd += f'source /etc/profile; go run {self.go_file}'
        else:
            cmd += f'go run {self.go_file}'
        cmd = cmd.replace('{', '{{')
        cmd = cmd.replace('}', '}}')
        self.log.info(cmd)
        res = self.pri_root.sh(cmd).result()
        self.log.info(res)
        self.assertNotIn('panic:', res, f'执行失败: {text}')
        self.assertIn('\n99901\n', res, f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        s4_text = '----step4: 还原pg_hba文件  expect: 成功----'
        self.log.info(s4_text)
        cmd = f'mv {self.pg_hba_path}_bak {self.pg_hba_path}'
        self.log.info(cmd)
        cmd_res = self.pri_user.sh(cmd).result()
        self.log.info(cmd_res)

        is_restart = self.pri_sh.restart_db_cluster()

        s5_text = '----step5: 删除用户  expect: 成功----'
        self.log.info(s5_text)
        sql = f'drop user if exists {self.db_user} cascade;'
        sql_res = self.pri_sh.execut_db_sql(sql)
        self.log.info(sql_res)

        s6_text = '----step6: 刪除go_conn.go expect: 成功----'
        self.log.info(s6_text)
        rm_cmd = f'rm -rf {self.go_file}'
        self.log.info(rm_cmd)
        rm_res = self.pri_root.sh(rm_cmd).result()
        self.log.info(rm_res)

        self.assertEqual(len(cmd_res), 0, f'执行失败: {s4_text}')
        self.assertTrue(is_restart, f'执行失败: {s4_text}')
        self.assertIn(self.cons.DROP_ROLE_SUCCESS_MSG,
                      sql_res,
                      f'执行失败: {s5_text}')
        self.assertIs(rm_res, '', f'执行失败: {s6_text}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)

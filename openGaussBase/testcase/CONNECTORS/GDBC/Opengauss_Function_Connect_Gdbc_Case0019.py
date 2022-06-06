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
Case Name   : 连接数据库，操作会话
Description :
    1.新建用户并赋权
    2.配置pg_hba入口, sha256认证方法
    3.连接数据库，操作会话
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


class ConnGO19(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.log = Logger()
        self.go = ComGo()
        self.cons = Constant()
        self.db_user = 'go_user_19'
        self.go_file = 'go_conn.go'
        self.t_name = 't_go_19'
        self.role_name = 'role_go_19'
        self.schema_name = 'schema_go_19'
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
            f"create user {self.db_user} with password " \
            f"'{macro.COMMON_PASSWD}';" \
            f"grant all privileges to {self.db_user};"
        self.log.info(sql)
        res = self.pri_sh.execut_db_sql(sql)
        self.log.info(res)
        expect = f'{self.cons.DROP_ROLE_SUCCESS_MSG}.*' \
            f'{self.cons.CREATE_ROLE_SUCCESS_MSG}.*' \
            f'{self.cons.ALTER_ROLE_SUCCESS_MSG}'
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

        text = '----step3: 连接数据库，操作会话 expect: 成功----'
        self.log.info(text)
        conn_str = f'connStr := "host={self.pri_user.db_host} ' \
            f'port={self.pri_user.db_port} ' \
            f'user={self.db_user} ' \
            f'password={macro.COMMON_PASSWD} ' \
            f'dbname={self.pri_user.db_name} ' \
            f'sslmode=disable"'

        clean_sql = f"drop table if exists {self.t_name} cascade;" \
            f"drop schema if exists {self.schema_name} cascade;" \
            f"drop role if exists {self.role_name};"
        # 创建模式ds
        q_str_1 = f"drop schema if exists {self.schema_name} cascade;" \
            f"create schema {self.schema_name};" \
            f"select n.nspname as name from pg_catalog.pg_namespace n " \
            f"where n.nspname !~ '^pg_' and " \
            f"n.nspname <> 'information_schema' and " \
            f"name='{self.schema_name}';"
        # 设置模式搜索路径
        q_str_2 = f"set search_path to {self.schema_name}, public;" \
            f"show search_path;"
        # 设置日期时间风格为传统的POSTGRES风格(日在月前)
        q_str_3 = "set datestyle to postgres, dmy;" \
                  "select to_char(now());"
        q_str_4 = "set datestyle to iso, ymd;" \
                  "select to_char(now());"
        # 设置时区为加州伯克利
        q_str_5 = "set time zone 'pst8pdt';show time zone;"
        # 设置时区为意大利
        q_str_6 = "set time zone 'europe/rome';show time zone;"
        # 设置当前模式
        q_str_7 = f"alter session set current_schema to {self.schema_name};" \
            f"show current_schema;"
        # 创建角色，并设置会话的角色
        q_str_8 = f"drop role if exists {self.role_name};" \
            f"create role {self.role_name} with password " \
            f"'{macro.PASSWD_INITIAL}';" \
            f"alter session set session authorization {self.role_name} " \
            f"password '{macro.PASSWD_INITIAL}';" \
            f"select definer_current_user();"
        # 切换到默认用户
        q_str_9 = "alter session set session authorization default;" \
                  "select definer_current_user();"
        # 设置XML OPTION为DOCUMENT
        e_str1 = "alter session set xml option document;"
        # 设置当前会话的字符编码为UTF8
        e_str2 = f"create table {self.t_name}(a int, b text);" \
            f"alter session set names 'utf8';" \
            f"insert into {self.t_name} values(2, '中文测试');"
        f_contant = f'{self.go.get_head()}\n\n' \
            f'func cleanup(db *sql.DB) {{\n' \
            f'    {self.go.exec_sql(clean_sql)}' \
            f'\n\n    db.Close()\n' \
            f'}}\n\n' \
            f'func r() {{\n' \
            f'    if r := recover(); r!= nil {{\n' \
            f'        fmt.Println("recovered from ", r)\n' \
            f'    }}\n' \
            f'}}\n\n' \
            f'func main() {{\n' \
            f'    {conn_str}\n' \
            f'    {self.go.conndb("connStr")}\n\n' \
            f'    defer r()\n' \
            f'    defer cleanup(db)\n\n' \
            f'    q_ary := []string{{}}\n'
        for q_str in [q_str_1, q_str_2, q_str_3, q_str_4, q_str_5, q_str_6,
                      q_str_7, q_str_8, q_str_9]:
            f_contant += f'    q_ary = append(q_ary, "{q_str}")\n'
        f_contant += f'    for _, v := range q_ary{{\n' \
            f'        var res string\n' \
            f'        err = db.QueryRow(v).Scan(&res)\n' \
            f'        if err != nil {{\n' \
            f'            panic(err)\n' \
            f'        }}\n' \
            f'        fmt.Println(res)\n' \
            f'    }}\n\n' \
            f'    e_ary := []string{{}}\n' \
            f'    e_ary = append(e_ary, "{e_str1}")\n' \
            f'    e_ary = append(e_ary, "{e_str2}")\n' \
            f'    for _, v := range e_ary{{\n' \
            f'        res, err := db.Exec(v)\n' \
            f'        if err != nil {{\n' \
            f'            panic(err)\n' \
            f'        }}\n' \
            f'        fmt.Println(res)\n' \
            f'    }}\n' \
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
        expect = f"{self.schema_name}.*" \
            f"{self.schema_name}, public.*" \
            f"Mon|Tue|Sat|Sun|Wed|Thu|Fri.*" \
            f"\\d{{4}}-\\d{{2}}-\\d{{2}}.*" \
            f"PST8PDT.*" \
            f"Europe/Rome.*" \
            f"{self.schema_name}.*" \
            f"{self.role_name}.*" \
            f"{self.db_user}"
        reg_res = re.search(expect, res, re.S)
        self.assertNotIn('panic:', res, f'执行失败: {text}')
        self.assertIsNotNone(reg_res, f'执行失败: {text}')

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

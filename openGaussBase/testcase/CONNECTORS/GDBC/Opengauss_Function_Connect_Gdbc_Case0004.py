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
Case Name   : 连接数据库，连接字符串多host定义
Description :
    1.新建用户并赋权
    2.配置pg_hba入口, sha256认证方法
    3.连接数据库，连接字符串多host定义
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

pri_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(pri_sh.get_node_num() <= 1, '单机环境不执行')
class ConnGO4(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.log = Logger()
        self.go = ComGo()
        self.cons = Constant()
        self.db_user = 'go_user_4'
        self.cur_os = self.pri_root.sh('cat /etc/system-release').result()
        self.pg_hba_path = os.path.join(macro.DB_INSTANCE_PATH,
                                        macro.PG_HBA_FILE_NAME)
        self.node_num = pri_sh.get_node_num()
        self.sta_user_list = []
        for i in range(self.node_num - 1):
            self.sta_user_list.append(Node(f'Standby{i + 1}DbUser'))
        self.go_file = 'go_conn.go'
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
            f"grant all privileges on database " \
            f"{self.pri_user.db_name} to {self.db_user};"
        self.log.info(sql)
        res = pri_sh.execut_db_sql(sql)
        self.log.info(res)
        expect = f'{self.cons.DROP_ROLE_SUCCESS_MSG}.*' \
            f'{self.cons.CREATE_ROLE_SUCCESS_MSG}.*' \
            f'{self.cons.GRANT_SUCCESS_MSG}'
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

        text = '----step3: 连接数据库，连接字符串多host定义,方式一 expect: 成功----'
        self.log.info(text)
        conn_str1 = f'connStr := "postgres://{self.db_user}:' \
            f'{macro.COMMON_PASSWD}@' \
            f'{self.pri_user.db_host}:{self.pri_user.db_port},'
        for n in self.sta_user_list:
            conn_str1 += f'{n.db_host}:{n.db_port},'
        conn_str1 = conn_str1.rstrip(',') + f'/{self.pri_user.db_name}' \
            f'?sslmode=disable"'
        sql = 'select current_catalog'
        f_contant = f'{self.go.get_head()}\n\n' \
            f'func cleanup(db *sql.DB) {{\n' \
            f'    db.Close()\n' \
            f'}}\n\n' \
            f'func main() {{\n' \
            f'    {conn_str1}\n' \
            f'    {self.go.conndb("connStr")}\n\n' \
            f'    defer cleanup(db)\n\n' \
            f'    {self.go.query_row(sql, **{"date": "string"})}\n' \
            f'}}'
        cmd = f'cat > {self.go_file} <<EOF\n' \
            f'{f_contant}\n' \
            f'EOF\n'
        if 'CentOS' in self.cur_os:
            cmd += f'source /etc/profile; go run {self.go_file}'
        else:
            cmd += f'go run {self.go_file}'
        self.log.info(cmd)
        cmd = cmd.replace('{', '{{')
        cmd = cmd.replace('}', '}}')
        res = self.pri_root.sh(cmd).result()
        self.log.info(res)
        self.assertNotIn('panic: ', res, f'执行失败: {text}')
        self.assertIn(self.pri_user.db_name, res, f'执行失败: {text}')

        text = '----step3: 连接数据库，连接字符串多host定义,方式二 expect: 成功----'
        self.log.info(text)
        conn_str2 = f'connStr := "user={self.db_user} ' \
            f'password={macro.COMMON_PASSWD} ' \
            f'host={self.pri_user.db_host},'
        for n in self.sta_user_list:
            conn_str2 += f'{n.db_host},'
        conn_str2 = conn_str2.rstrip(',') + f' port=' \
            f'{self.pri_user.db_port} dbname={self.pri_user.db_name} ' \
            f'sslmode=disable"'
        cmd = cmd.replace(conn_str1, conn_str2)
        self.log.info(cmd)
        res = self.pri_root.sh(cmd).result()
        self.log.info(res)
        self.assertNotIn('panic: ', res, f'执行失败: {text}')
        self.assertIn(self.pri_user.db_name, res, f'执行失败: {text}')

        text = '----step3: 连接数据库，连接字符串多host定义,方式三 expect: 成功----'
        self.log.info(text)
        conn_str3 = f'connStr := "user={self.db_user} ' \
            f'password={macro.COMMON_PASSWD} ' \
            f'host={self.pri_user.db_host},'
        for n in self.sta_user_list:
            conn_str3 += f'{n.db_host},'
        conn_str3 = conn_str3.rstrip(',') + f' port={self.pri_user.db_port},'
        for n in self.sta_user_list:
            conn_str3 += f'{n.db_port},'
        conn_str3 = conn_str3.rstrip(',') + f'' \
            f' dbname={self.pri_user.db_name} sslmode=disable"'
        cmd = cmd.replace(conn_str2, conn_str3)
        self.log.info(cmd)
        res = self.pri_root.sh(cmd).result()
        self.log.info(res)
        self.assertNotIn('panic: ', res, f'执行失败: {text}')
        self.assertIn(self.pri_user.db_name, res, f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        s4_text = '----step4: 还原pg_hba文件  expect: 成功----'
        self.log.info(s4_text)
        cmd = f'mv {self.pg_hba_path}_bak {self.pg_hba_path}'
        self.log.info(cmd)
        cmd_res = self.pri_user.sh(cmd).result()
        self.log.info(cmd_res)

        is_restart = pri_sh.restart_db_cluster()

        s5_text = '----step5: 删除用户  expect: 成功----'
        self.log.info(s5_text)
        sql = f'drop user if exists {self.db_user} cascade;'
        sql_res = pri_sh.execut_db_sql(sql)
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

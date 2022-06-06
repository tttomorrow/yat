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
Case Name   : 连接数据库，关闭当前节点
Description :
    1.新建用户并赋权
    2.配置pg_hba入口, sha256认证方法
    3.连接数据库，执行SHUTDOWN关闭当前节点
    4.查看数据库状态
    5.启动当前节点
    6.查看数据库状态
    7.连接数据库,执行SHUTDOWN FAST关闭当前节点
    8.查看数据库状态
    9.启动当前节点
    10.查看数据库状态
    11.连接数据库,执行SHUTDOWN immediate关闭当前节点
    12.查看数据库状态
    13.启动当前节点
    14.查看数据库状态
    15.还原pg_hba文件
    16.删除用户
    17.刪除go_conn.go
Expect      :
    1.执行成功
    2.执行成功
    3.执行成功, 回显无panic提示
    4.执行成功, 主节点状态为stop
    5.执行成功
    6.执行成功, 所有节点状态为normal
    7.执行成功, 回显无panic提示
    8.执行成功, 主节点状态为stop
    9.执行成功
    10.执行成功, 所有节点状态为normal
    11.执行成功, 回显无panic提示
    12.执行成功, 主节点状态为stop
    13.执行成功
    14.执行成功, 所有节点状态为normal
    15.执行成功
    16.执行成功
    17.执行成功
History     :
"""
import os
import re
import time
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.ComGo import ComGo
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnGO31(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.log = Logger()
        self.go = ComGo()
        self.cons = Constant()
        self.db_user = 'go_user_31'
        self.go_file = 'go_conn.go'
        self.t_name = 't_go_31'
        self.cur_os = self.pri_root.sh('cat /etc/system-release').result()
        self.pg_hba_path = os.path.join(macro.DB_INSTANCE_PATH,
                                        macro.PG_HBA_FILE_NAME)
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = f'----前置检查：已安装golang1.11.1以上版本----'
        self.log.info(text)
        res = self.go.check_install_go(self.pri_user, '1.11.1')
        self.assertTrue(res, f'执行失败: {text}')

        self.node_num = self.pri_sh.get_node_num()

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

        text = '----step3: 连接数据库，执行SHUTDOWN关闭当前节点 ' \
               'expect: 执行成功, 回显无panic提示----'
        self.log.info(text)
        conn_str = f'connStr := "host={self.pri_user.db_host} ' \
            f'port={self.pri_user.db_port} ' \
            f'user={self.db_user} ' \
            f'password={macro.COMMON_PASSWD} ' \
            f'dbname={self.pri_user.db_name} ' \
            f'sslmode=disable"'

        s_sql = "shutdown;"
        f_contant = f'{self.go.get_head()}\n\n' \
            f'func main() {{\n' \
            f'    {conn_str}\n' \
            f'    {self.go.conndb("connStr")}\n\n' \
            f'    {self.go.exec_sql(s_sql)}\n' \
            f'}}'
        go_cmd = f'cat > {self.go_file} <<EOF\n' \
            f'{f_contant}\n' \
            f'EOF\n'
        if 'CentOS' in self.cur_os:
            go_cmd += f'source /etc/profile; go run {self.go_file}'
        else:
            go_cmd += f'go run {self.go_file}'
        go_cmd = go_cmd.replace('{', '{{')
        go_cmd = go_cmd.replace('}', '}}')
        self.log.info(go_cmd)
        res = self.pri_root.sh(go_cmd).result()
        self.log.info(res)
        self.assertNotIn('panic:', res, f'执行失败: {text}')

        time.sleep(30)

        text = '----step4: 查看数据库状态 expect: 当前节点状态异常----'
        self.log.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.log.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.log.info(db_status)
        regex_res = re.findall('instance_state.*:.*Manually stopped',
                               db_status)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), 1, text)

        text = '----step5: 启动当前节点 expect: 成功----'
        self.log.info(text)
        expect_msg = self.cons.RESTART_SUCCESS_MSG
        node_status = self.pri_sh.execute_gsctl('start', expect_msg)
        self.assertTrue(node_status)

        text = '----step6: 查看数据库状态 expect: 数据库状态正常----'
        self.log.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.log.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.log.info(db_status)
        regex_res = re.findall('instance_state.*:.*Normal', db_status)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), self.node_num, text)

        text = '----step7: 连接数据库，执行SHUTDOWN FAST关闭当前节点 ' \
               'expect: 执行成功, 回显无panic提示----'
        self.log.info(text)
        go_cmd = go_cmd.replace(s_sql, 'shutdown fast')
        self.log.info(go_cmd)
        res = self.pri_root.sh(go_cmd).result()
        self.log.info(res)
        self.assertNotIn('panic:', res, f'执行失败: {text}')

        time.sleep(5)

        text = '----step8: 查看数据库状态 expect: 当前节点状态异常----'
        self.log.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.log.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.log.info(db_status)
        regex_res = re.findall('instance_state.*:.*Manually stopped',
                               db_status)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), 1, text)

        text = '----step9: 启动当前节点 expect: 成功----'
        self.log.info(text)
        expect_msg = self.cons.RESTART_SUCCESS_MSG
        node_status = self.pri_sh.execute_gsctl('start', expect_msg)
        self.assertTrue(node_status)

        text = '----step10: 查看数据库状态 expect: 数据库状态正常----'
        self.log.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.log.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.log.info(db_status)
        regex_res = re.findall('instance_state.*:.*Normal', db_status)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), self.node_num, text)

        text = '----step11: 连接数据库，执行SHUTDOWN immediate关闭当前节点 ' \
               'expect: 执行成功, 回显无panic提示----'
        self.log.info(text)
        go_cmd = go_cmd.replace('shutdown fast', 'shutdown immediate')
        self.log.info(go_cmd)
        res = self.pri_root.sh(go_cmd).result()
        self.log.info(res)
        self.assertNotIn('panic:', res, f'执行失败: {text}')

        time.sleep(5)

        text = '----step12: 查看数据库状态 expect: 当前节点状态异常----'
        self.log.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.log.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.log.info(db_status)
        regex_res = re.findall('instance_state.*:.*Manually stopped',
                               db_status)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), 1, text)

        text = '----step13: 启动当前节点 expect: 成功----'
        self.log.info(text)
        expect_msg = self.cons.RESTART_SUCCESS_MSG
        node_status = self.pri_sh.execute_gsctl('start', expect_msg)
        self.assertTrue(node_status)

        text = '----step14: 查看数据库状态 expect: 数据库状态正常----'
        self.log.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.log.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.log.info(db_status)
        regex_res = re.findall('instance_state.*:.*Normal', db_status)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), self.node_num, text)

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        s15_text = '----step15: 还原pg_hba文件  expect: 成功----'
        self.log.info(s15_text)
        cmd = f'mv {self.pg_hba_path}_bak {self.pg_hba_path}'
        self.log.info(cmd)
        cmd_res = self.pri_user.sh(cmd).result()
        self.log.info(cmd_res)

        is_restart = self.pri_sh.restart_db_cluster()

        s16_text = '----step16: 删除用户  expect: 成功----'
        self.log.info(s16_text)
        sql = f'drop user if exists {self.db_user} cascade;'
        sql_res = self.pri_sh.execut_db_sql(sql)
        self.log.info(sql_res)

        s17_text = '----step17: 刪除go_conn.go expect: 成功----'
        self.log.info(s17_text)
        rm_cmd = f'rm -rf {self.go_file}'
        self.log.info(rm_cmd)
        rm_res = self.pri_root.sh(rm_cmd).result()
        self.log.info(rm_res)

        self.assertEqual(len(cmd_res), 0, f'执行失败: {s15_text}')
        self.assertTrue(is_restart, f'执行失败: {s15_text}')
        self.assertIn(self.cons.DROP_ROLE_SUCCESS_MSG,
                      sql_res,
                      f'执行失败: {s16_text}')
        self.assertIs(rm_res, '', f'执行失败: {s17_text}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)

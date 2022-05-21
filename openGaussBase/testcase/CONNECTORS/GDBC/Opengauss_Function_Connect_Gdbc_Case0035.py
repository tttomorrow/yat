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
Case Name   : 连接数据库，定义表及约束
Description :
    1.新建用户并赋权
    2.配置pg_hba入口, sha256认证方法
    3.连接数据库，定义表及约束
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


class ConnGO35(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.log = Logger()
        self.go = ComGo()
        self.cons = Constant()
        self.db_user = 'go_user_35'
        self.go_file = 'go_conn.go'
        self.t_name = 't_go_35'
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
            f"grant all privileges on database " \
            f"{self.pri_user.db_name} to {self.db_user};"
        self.log.info(sql)
        res = self.pri_sh.execut_db_sql(sql)
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

        text = '----step3: 连接数据库，定义表及约束 expect: 成功----'
        self.log.info(text)
        conn_str = f'connStr := "host={self.pri_user.db_host} ' \
            f'port={self.pri_user.db_port} ' \
            f'user={self.db_user} ' \
            f'password={macro.COMMON_PASSWD} ' \
            f'dbname={self.pri_user.db_name} ' \
            f'sslmode=disable"'

        clean_sql = f"drop table if exists {self.t_name}_1 cascade;" \
            f"drop table if exists {self.t_name}_2 cascade;"
        s_sql = f'{clean_sql}' \
            f'create table if not exists {self.t_name}_1(' \
            f'w_city             varchar(60)   primary key,' \
            f'w_address          text);' \
            f'create table if not exists {self.t_name}_2(' \
            f'w_warehouse_sk     integer       not null,' \
            f'w_warehouse_id     char(16)      not null,' \
            f'w_warehouse_name   varchar(20)   unique deferrable,' \
            f'w_warehouse_sq_ft  integer       ,' \
            f'w_street_number    char(10)      check (' \
            f'w_street_number is not null),' \
            f'w_street_name      varchar(60)   ,' \
            f'w_street_type      char(15)      ,' \
            f'w_suite_number     char(10)      ,' \
            f'w_city             varchar(60)   references {self.t_name}_1(' \
            f'w_city),' \
            f'w_county           varchar(30)   ,' \
            f'w_state            char(2)       default \'go\',' \
            f'w_zip              char(10)      ,' \
            f'w_country          varchar(20)   ,' \
            f'w_gmt_offset       decimal(5,2)  ,' \
            f'constraint w_cstr_key2 primary key(w_warehouse_sk, ' \
            f'w_warehouse_id)' \
            f')with(fillfactor=70);'
        s_sql1 = f"insert into {self.t_name}_1 values ('bj', 'bj101');" \
            f"insert into {self.t_name}_2 values (101, '101', 'nw', 1, " \
            f"'sn', 'sn', 'st', 'sn', 'bj', 'bjbj', 'gh', 'zip', 'wc'," \
            f" 10.1);"
        # 违反非空约束
        s_sql2 = f"insert into {self.t_name}_2 values (101, '', 'nw', 1," \
            f" 'sn', 'sn', 'st', 'sn', 'bj', 'bjbj', 'gh', 'zip', 'wc', " \
            f"10.1);"
        # 违反唯一约束
        s_sql3 = f"insert into {self.t_name}_2 values (102, '102', 'nw', " \
            f"1, 'sn', 'sn', 'st', 'sn', 'bj', 'bjbj', 'gh', 'zip', 'wc', " \
            f"10.1);"
        # 违反check约束
        s_sql4 = f"insert into {self.t_name}_2 values (102, '102', 'nw2', " \
            f"1, '', 'sn', 'st', 'sn', 'bj', 'bjbj', 'gh', 'zip', 'wc', " \
            f"10.1);"
        # 外键约束查询
        query_sql = f"select count(a.*) as num_a, count(b.*) as num_b from" \
            f" {self.t_name}_1 a, {self.t_name}_2 b where a.w_city=b.w_city;"
        param_dict = {"num_a": "int", "num_b": "int"}
        # default约束成功
        s_sql5 = f"insert into {self.t_name}_2(w_warehouse_sk, " \
            f"w_warehouse_id, w_warehouse_name, w_street_number, " \
            f"w_city) values (102, '102', 'nw2', 'sn2', 'bj');"
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
            f'func execute(sql string, db *sql.DB) {{\n' \
            f'    defer r()\n' \
            f'    res, err := db.Exec(sql)\n' \
            f'    if err != nil {{\n' \
            f'        panic(err)\n' \
            f'    }}\n' \
            f'    fmt.Println(res)\n' \
            f'}}\n\n' \
            f'func main() {{\n' \
            f'    {conn_str}\n' \
            f'    {self.go.conndb("connStr")}\n\n' \
            f'    defer cleanup(db)\n\n' \
            f'    {self.go.exec_sql(s_sql)}\n\n' \
            f'    {self.go.exec_sql(s_sql1, False)}\n\n' \
            f'    execute("{s_sql2}", db)\n\n' \
            f'    execute("{s_sql3}", db)\n\n' \
            f'    execute("{s_sql4}", db)\n\n' \
            f'    {self.go.query_row(query_sql, **param_dict)}\n\n' \
            f'    execute("{s_sql5}", db)\n\n' \
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
        expect = f"{{0x.*0}}\n{{0x.*1}}\n" \
            f"recovered from  pq: null value in column \"w_warehouse_id\" " \
            f"violates not-null constraint\n" \
            f"recovered from  pq: duplicate key value violates unique " \
            f"constraint \"{self.t_name}_2_w_warehouse_name_key\"\n" \
            f"recovered from  pq: new row for relation \"{self.t_name}_2\" " \
            f"violates check constraint " \
            f"\"{self.t_name}_2_w_street_number_check\"\n1 1\n" \
            f"{{0x.*1}}\n{{0x.*0}}"
        reg_res = re.search(expect, res)
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

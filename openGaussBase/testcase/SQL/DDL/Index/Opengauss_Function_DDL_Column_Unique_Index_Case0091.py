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
Case Type   : column unique index
Case Name   : 创建列存普通表,gs_dump导出表后，添加唯一约束等，导入表
Description :
    1、创建普通列存表,插入数据
    2、gs_dump以纯文本格式导出表关系及数据
    3、向表中字段添加主键\唯一约束\唯一索引
    4、gsql导入表
    5、再次插入表中已存在数据
    6、清理环境
Expect      :
    1、建表成功，插入数据成功
    2、导出表成功
    3、添加约束及索引成功
    4、导入数据成功
    5、插入数据失败
    6、清理环境成功
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class DDLTestCase(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.constant = Constant()
        self.table = 't_columns_unique_index_0091'
        self.index = 'i_columns_unique_index_0091'
        self.dump_path = os.path.join(macro.DB_INSTANCE_PATH, 'dump.sql')

        self.log.info('======检查数据库状态======')
        result = self.sh_primysh.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def test_column_unique_index(self):
        self.log.info('---Opengauss_Function_DDL_Column_Unique_Index_Case0091'
                      '开始执行---')
        text = '-----step1:创建普通列存表，插入数据   expect:成功-----'
        self.log.info(text)
        sql_cmd1 = f'''drop table if exists {self.table};
            create table {self.table}(name character(10),
            age int,salary money) with(orientation=column);
            insert into {self.table} values('a_'||generate_series(1,1000),
            generate_series(1,1000),generate_series(1,1000));
            '''
        sql_res1 = self.sh_primysh.execut_db_sql(sql_cmd1)
        self.log.info(sql_res1)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in sql_res1
                        and self.constant.INSERT_SUCCESS_MSG in sql_res1,
                        '执行失败' + text)

        text = '-----step2:gs_dump以纯文本格式导出表关系及数据   expect:成功------'
        self.log.info(text)
        cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_dump {self.user_node.db_name} \
            -f {self.dump_path} \
            -t {self.table} \
            -p {self.user_node.db_port} \
            -F p
            '''
        self.log.info(cmd1)
        msg1 = self.user_node.sh(cmd1).result()
        self.log.info(msg1)
        self.assertIn('dump database {} successfully'.format(
            self.user_node.db_name), msg1.split('\n')[-2].strip(),
            '执行失败' + text)

        text = '-----step3:向表中字段添加主键&唯一约束&唯一索引   expect:成功-----'
        self.log.info(text)

        shell1 = f"""grep -nr 'orientation=column' {self.dump_path}"""
        self.log.info(shell1)
        res1 = self.user_node.sh(shell1).result().split(':')[0]
        self.log.info(res1)
        lines = int(res1)+1

        shell2 = f'''sed -i "{lines} ialter table {self.table} add primary\
            key(name);alter table {self.table} add constraint cons_91 \
            unique(age);create unique index {self.index} on {self.table} \
            using btree(salary);" {self.dump_path}'''
        self.log.info(shell2)
        res2 = self.user_node.sh(shell2).result()
        self.log.info(res2)
        self.assertEqual('', res2, '执行失败' + text)

        text = '-----step4:gsql导入表   expect:成功-----'
        self.log.info(text)
        cmd2 = f'''source {macro.DB_ENV_PATH};
            gsql {self.user_node.db_name} \
            -p {self.user_node.db_port} \
            -c "drop table if exists {self.table};"
            gsql {self.user_node.db_name} \
            -p {self.user_node.db_port} \
            -f {self.dump_path}'''
        msg2 = self.user_node.sh(cmd2).result()
        self.log.info(msg2)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, msg2)

        text = '------step5:查看数据，再次插入已存在数据   expect:成功------'
        self.log.info(text)
        sql_cmd3 = f'''select count(*) from {self.table};
            insert into {self.table} values('a_'||generate_series(1,1000),
            generate_series(1,1000),generate_series(1,1000));'''
        self.log.info(sql_cmd3)

        sql_res3 = self.sh_primysh.execut_db_sql(sql_cmd3)
        self.log.info(sql_res3)
        self.assertTrue('1000' in sql_res3.splitlines()[2].strip()
                        and self.constant.unique_index_error_info in sql_res3,
                        '执行失败' + text)

    def tearDown(self):
        self.log.info('------step6:清理环境   expect:成功------')
        del_cmd = f'''source {macro.DB_ENV_PATH};
            gsql {self.user_node.db_name} \
            -p {self.user_node.db_port} \
            -c "drop table {self.table} cascade;"
            rm -rf {self.dump_path}
            '''
        self.log.info(del_cmd)
        del_res = self.user_node.sh(del_cmd).result()
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, del_res)
        self.log.info('---Opengauss_Function_DDL_Column_Unique_Index_Case0091'
                      '执行结束---')

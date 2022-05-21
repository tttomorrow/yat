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
Case Name   : 创建兼容的数据库类型为PG的数据库,然后导出数据,是否可以正常导出
Description :
    1.连接数据库，创建兼容PG格式的数据库
    create database databasename dbcompatibility 'PG';
    2.在创建好的数据库中,创建数据
    3.连接创建好的数据库,导出数据
    gs_dump databasename -p port -f /data/dump1.sql
    4.清理环境
    rm -rf /data/dump1.sql
    drop database databasename;
Expect      :
    1.创建兼容PG格式的数据库成功
    2.数据创建成功
    3.数据导出成功
    4.清理完成
History     : 
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Tools_gs_dump_Case0126start---')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.constant = Constant()
        self.dump_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump.sql')
        self.db_name1 = "db_dump0126_01"
        self.db_name2 = "db_dump0126_02"
        self.tb_name = "t_dump0126"

    def test_tools_dump(self):
        text = '---step1:创建兼容的数据库类型为PG的数据库;expect:创建成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''
            drop database if exists {self.db_name1};
            drop database if exists {self.db_name2};
            create database {self.db_name1} dbcompatibility 'PG';
            create database {self.db_name2};
            ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '---step2:在创建的数据库中创建表和数据;expect:创建成功---'
        self.log.info(text)
        sql_cmd = f'''drop table if  exists {self.tb_name};
            create table {self.tb_name} (id int);
            insert into {self.tb_name} values (generate_series(1,10));
            select count(*) from {self.tb_name};'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name1}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)
        self.assertIn('10', sql_result, '执行失败:' + text)

        text = '---step3.1:连接创建好的数据库,执行导出操作;expect:导出成功---'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_dump {self.db_name1} \
            -p {self.Primary_Node.db_port} \
            -f {self.dump_path};
            '''
        self.log.info(dump_cmd)
        dump_result = self.Primary_Node.sh(dump_cmd).result()
        self.log.info(dump_result)
        self.assertIn(f'dump database {self.db_name1} successfully',
                      dump_result,
                      '执行失败:' + text)

        text = '-----step3.2:连接新的数据库进行导入;expect:导入成功---'
        self.log.info(text)
        gsql_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gsql {self.db_name2} " \
            f"-p {self.Primary_Node.db_port} " \
            f"-f {self.dump_path};"
        self.log.info(gsql_cmd)
        gsql_result = self.Primary_Node.sh(gsql_cmd).result()
        self.log.info(gsql_result)
        self.assertIn('CREATE TABLE', gsql_result,
                      '执行失败:' + text)
        self.log.info('---在导入的数据库中查询表和数据,表和数据都存在---')
        sql_cmd = f"select count(*) from {self.tb_name};"
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name2}')
        self.log.info(sql_result)
        count_num = sql_result.splitlines()[2].strip()
        self.log.info(count_num)
        self.assertIn('1 row', sql_result, '执行失败:' + text)
        self.assertEqual(count_num, '10', '执行失败:' + text)

    def tearDown(self):
        text = '--------------step4:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.dump_path};'
        self.log.info(rm_cmd)
        result = self.Root_Node.sh(rm_cmd).result()
        self.log.info(result)
        sql_cmd = self.pri_sh.execut_db_sql(
            f'drop database if exists  {self.db_name1};'
            f'drop database if exists  {self.db_name2};')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Tools_gs_dump_Case0126finish------')

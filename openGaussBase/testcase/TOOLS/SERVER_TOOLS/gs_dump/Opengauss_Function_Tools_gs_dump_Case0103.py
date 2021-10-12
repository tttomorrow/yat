"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : 修改dump导出的数据文件后,再导入(纯文本格式:修改sql语句)
Description :
    1.创建数据；
    2.执行导出操作：
    gs_dump databasename -p port -f dump1.sql
    3.修改导出的文件
    4.导入修改后的文件
    gsql -p port -d databasename -r -f  dump1.sql
    5.清理环境：
    drop database databasename;
    rm -rf dump1.sql;
Expect      :
    1.数据创建成功
    2.导出成功
    3.修改导出的文件成功
    4.导入时未修改的语句和数据正常导入，修改过的报错
    5.清理成功
History     : 
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.log.info(
            '---Opengauss_Function_Tools_gs_dump_Case0103start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.com = Common()
        self.dump_path1 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump1.sql')
        self.db_name1 = "db_dump0103_01"
        self.db_name2 = "db_dump0103_02"
        self.tb_name1 = "t_dump0103_01"
        self.tb_name2 = "t_dump0103_02"

    def test_tools_dump(self):
        text = '---step1:创建测试数据;expect:创建成功---'
        self.log.info(text)
        self.log.info('------创建成功数据库-------')
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''
            drop database if exists {self.db_name1};
            drop database if exists {self.db_name2};
            create database {self.db_name1};
            create database {self.db_name2};
            ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.log.info('---在创建的数据库中创建表和数据---')
        sql_cmd = f'''drop table if  exists {self.tb_name1};
            create table {self.tb_name1} (id int);
            insert into {self.tb_name1} values (generate_series(1,10));
            select count(*) from {self.tb_name1};'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name1}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)
        self.assertIn('10', sql_result, '执行失败:' + text)

        text = '---step2:执行导出操作;expect:导出成功---'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_dump {self.db_name1} \
            -p {self.Primary_Node.db_port} \
            -f {self.dump_path1};
            '''
        self.log.info(dump_cmd)
        dump_result = self.Primary_Node.sh(dump_cmd).result()
        self.log.info(dump_result)
        self.assertIn(f'dump database {self.db_name1} successfully',
                      dump_result,
                      '执行失败:' + text)

        text = '-----step3.修改导出的文件中的sql语句;expect:修改成功-----'
        self.log.info(text)
        sed_cmd = f"sed -i 's\COPY {self.tb_name1}\COPY {self.tb_name2}\g' " \
            f"{self.dump_path1};" \
            f"cat {self.dump_path1};"
        self.log.info(sed_cmd)
        sed_result = self.Primary_Node.sh(sed_cmd).result()
        self.log.info(sed_result)
        self.assertIn(f'COPY t_dump0103_02', sed_result, '执行失败:' + text)

        text = '---step4:导入修改后的文件;expect:未修改的语句和数据正常导入，修改过的报错---'
        self.log.info(text)
        gsql_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gsql -d {self.db_name2} " \
            f"-p {self.Primary_Node.db_port} -r " \
            f"-f  {self.dump_path1};"
        self.log.info(gsql_cmd)
        gsql_result = self.Primary_Node.sh(gsql_cmd).result()
        self.log.info(gsql_result)
        self.assertIn(f'ERROR:  relation "{self.tb_name2}" does not exist',
                      gsql_result, '执行失败:' + text)
        self.assertIn(f'CREATE TABLE', gsql_result, '执行失败:' + text)

        self.log.info('---在导入的数据库中查询表和数据，表1存在，但无数据---')
        sql_cmd = f"select count(*) from {self.tb_name1};"
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name2}')
        self.log.info(sql_result)
        count_num = sql_result.splitlines()[2].strip()
        self.log.info(count_num)
        self.assertIn('1 row', sql_result, '执行失败:' + text)
        self.assertEqual(count_num, '0', '执行失败:' + text)

    def tearDown(self):
        text = '--------------step5:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.dump_path1};'
        self.log.info(rm_cmd)
        result = self.Root_Node.sh(rm_cmd).result()
        self.log.info(result)
        sql_cmd = self.pri_sh.execut_db_sql(
            f'drop database if exists  {self.db_name1};'
            f'drop database if exists  {self.db_name2};')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Tools_gs_dump_Case0103finish------')
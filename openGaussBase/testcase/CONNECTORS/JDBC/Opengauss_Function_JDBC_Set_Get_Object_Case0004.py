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
Case Type   : 数据库系统
Case Name   : 数据库兼容PG模式，localdatetime类型setObject插入Date类型数据
Description :
    1.写配置文件
    2.编译java工具
    3.运行java工具
Expect      :
History     :
"""
import unittest
import os
from datetime import date, timedelta
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class Jdbcisreadonly(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.db_primary_user_node = Node(node='PrimaryDbUser')
        self.db_primary_root_node = Node(node='PrimaryRoot')
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_JDBC_Set_Get_Object_Case0004 start")
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath,
                                       "jdbc_case0001.properties")
        self.sql_path = os.path.join(self.targetpath, "jdbc_set_get_object")
        self.java_name = "jdbc_set_get_object_case0004"
        self.common = Common()
        self.commsh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.db_name = "db_jdbc_1"

    def test_index(self):
        self.log.info('------------1.创建数据库-------------')
        result = self.commsh.execut_db_sql(
            f"drop database if exists {self.db_name};"
            f"create database {self.db_name} DBCOMPATIBILITY='PG';")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('--------2.写配置文件-------')
        cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')}"
        self.db_primary_user_node.sh(cmd)
        cmd = f"grep -nr '127.0.0.1/32' " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        line = self.db_primary_root_node.sh(
            cmd).result().splitlines()[0].split(':')[0]
        self.log.info(line)
        cmd = f'sed -i "{str(int(line)+1)}ihost all all ' \
            f'{self.db_primary_user_node.db_host}/32 sha256" ' \
            f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")}; ' \
            f'cat {os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")}'
        self.log.info(cmd)
        result = self.db_primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.common.scp_file(self.db_primary_root_node,
                             f"{self.java_name}.java", self.targetpath)
        result = self.db_primary_root_node.sh(
            f"touch {self.properties}").result()
        self.log.info(result)
        config = f'echo "password=' \
            f'{self.db_primary_user_node.db_password}"> {self.properties}'
        self.db_primary_root_node.sh(config)
        config = f'echo "port={self.db_primary_user_node.db_port}">> ' \
            f'{self.properties}'
        self.db_primary_root_node.sh(config)
        config = f'echo "hostname={self.db_primary_user_node.db_host}">> ' \
            f'{self.properties}'
        self.db_primary_root_node.sh(config)
        config = f'echo "user={self.db_primary_user_node.db_user}">> ' \
            f'{self.properties}'
        self.db_primary_root_node.sh(config)
        config = f'echo "dbname={self.db_name}">> ' \
            f'{self.properties}'
        self.db_primary_root_node.sh(config)
        config = f'echo "stringtype=unspecified">> {self.properties}'
        self.db_primary_root_node.sh(config)
        config = f'cat {self.properties}'
        result = self.db_primary_root_node.sh(config).result()
        self.assertTrue("password=" in result and "port=" in result
                        and "hostname=" in result and "user=" in result
                        and "dbname=" in result)

        self.log.info('--------------2. 编译java工具------------------')
        self.db_primary_root_node.scp_put(macro.JDBC_PATH,
                                          f"{self.targetpath}/postgresql.jar")
        cmd = f"javac -encoding utf-8 -cp " \
            f"{os.path.join(self.targetpath, 'postgresql.jar')} " \
            f"{os.path.join(self.targetpath, f'{self.java_name}.java')}"
        self.log.info(cmd)
        result = self.db_primary_root_node.sh(cmd).result()
        self.log.info(result)

        self.log.info("-------------3.运行java工具---------------------")
        cmd = f" java -cp {os.path.join(self.targetpath, 'postgresql.jar')}" \
            f":{self.targetpath} " \
            f"{self.java_name} -F {self.properties}"
        self.log.info(cmd)
        result = self.db_primary_root_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('第1行结果：\x00994-08-17', result)
        self.assertIn('第2行结果：\x00055-12-03', result)
        self.assertIn('第3行结果：null', result)
        self.assertIn('第5行结果：1970-01-01', result)
        self.assertIn('第6行结果：2021-01-29', result)
        self.assertIn('第8行结果：2020-02-29', result)
        today = date.today().strftime("%Y-%m-%d")
        self.assertIn(f'第4行结果：{today}', result)
        self.assertIn(f'第7行结果：{today}', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"rm -rf {self.targetpath}"
        self.log.info(cmd)
        self.db_primary_root_node.sh(cmd)
        cmd = f"rm -rf " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};" \
            f"mv " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        self.db_primary_user_node.sh(cmd)

        result = self.commsh.execut_db_sql(
            f"drop database if exists {self.db_name};")
        self.log.info(result)
        self.log.info("Opengauss_Function_JDBC_Set_Get_Object_Case0004 end")
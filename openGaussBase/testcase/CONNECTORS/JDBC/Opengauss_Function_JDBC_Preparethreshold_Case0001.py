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
Case Type   : 数据库系统
Case Name   : jdbc连接配置prepareThreshold=1
Description :
    1.创建表
    2.测试jdbc代码
    3.执行jdbc
    4.查看数据库状态
Expect      :
History     :
"""
import unittest
import os
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
        self.log.info("Opengauss_Function_JDBC_Preparethreshold_Case0001 "
                      "start")
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath,
                                       "jdbc_case0001.properties")
        self.sql_path = os.path.join(self.targetpath, "jdbc_set_get_object")
        self.java_name = "jdbc_preparethreshold_case0001"
        self.tb_name = "test"
        self.common = Common()
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.pg_log = \
            os.path.join(macro.PG_LOG_PATH, macro.DN_NODE_NAME.split('/')[0])

    def test_index(self):
        self.log.info("------------查询数据库状态--------------------")
        result = self.commonshpri.stop_db_cluster()
        self.assertTrue(result)
        result = self.commonshpri.start_db_cluster()
        self.assertTrue(result)
        result = self.commonshpri.get_db_cluster_status('status')
        self.assertTrue(result)

        self.log.info('---------1.创建表-------------------')
        sql = f"drop table if exists {self.tb_name};" \
            f"create table {self.tb_name}(id int , c2 int, name text);" \
            f"insert into {self.tb_name}(id,c2, name) " \
            f"select 1,n, n||'_test' " \
            f"from generate_series(1,50) n;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn("INSERT 0 50", result)

        self.log.info('--------2.写配置文件-------')
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
        config = f'echo "dbname={self.db_primary_user_node.db_name}">> ' \
            f'{self.properties}'
        self.db_primary_root_node.sh(config)
        config = f'echo "stringtype=unspecified">> {self.properties}'
        self.db_primary_root_node.sh(config)
        config = f'cat {self.properties}'
        result = self.db_primary_root_node.sh(config).result()
        self.assertTrue("password=" in result and "port=" in result
                        and "hostname=" in result and "user=" in result
                        and "dbname=" in result)

        self.log.info('--------------3. 编译java工具------------------')
        self.db_primary_root_node.scp_put(macro.JDBC_PATH,
                                          f"{self.targetpath}/postgresql.jar")
        cmd = f"javac -encoding utf-8 -cp " \
            f"{os.path.join(self.targetpath, 'postgresql.jar')} " \
            f"{os.path.join(self.targetpath, f'{self.java_name}.java')}"
        self.log.info(cmd)
        result = self.db_primary_root_node.sh(cmd).result()
        self.log.info(result)

        self.log.info("-------------4.运行java工具---------------------")
        cmd = f" java -cp {os.path.join(self.targetpath, 'postgresql.jar')}" \
            f":{self.targetpath} " \
            f"{self.java_name} -F {self.properties}"
        result = self.common.get_sh_result(self.db_primary_root_node, cmd)
        self.log.info(result)
        self.assertIn(
            "?prepareThreshold=1&currentSchema=public&autosave=always",
            result)

        self.log.info("------------5.查询数据库状态--------------------")
        result = self.commonshpri.get_db_cluster_status('status')
        self.assertTrue(result)
        cmd = f"ls -lt {self.pg_log}"
        self.log.info(cmd)
        result = self.db_primary_user_node.sh(cmd).result()
        file_name = result.splitlines()[1].split(' ')[-1]
        self.log.info(file_name)

        cmd = f"cat {os.path.join(self.pg_log, file_name)} | grep 'PANIC'"
        self.log.info(cmd)
        result = self.common.get_sh_result(self.db_primary_root_node, cmd)
        self.assertNotIn('PANIC', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"drop table if exists {self.tb_name};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)

        cmd = f"rm -rf {self.targetpath}"
        self.log.info(cmd)
        self.db_primary_root_node.sh(cmd)
        self.log.info("-Opengauss_Function_JDBC_Preparethreshold_Case0001 "
                      "end-")

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
Case Name   : OffSetDateTime类型setObject插入TIMESTAMP with out timezone类型数据
Description :
    1.写配置文件
    2.编译java工具
    3.运行java工具
Expect      :
History     :
"""
import unittest
import os
from datetime import date, timedelta, datetime
import datetime
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common


class Jdbcisreadonly(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.db_primary_user_node = Node(node='PrimaryDbUser')
        self.db_primary_root_node = Node(node='PrimaryRoot')
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_JDBC_Set_Get_Object_Case0013 start")
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath,
                                       "jdbc_case0001.properties")
        self.sql_path = os.path.join(self.targetpath, "jdbc_set_get_object")
        self.java_name = "jdbc_set_get_object_case0013"
        self.common = Common()

    def test_index(self):
        self.log.info('--------1.写配置文件-------')
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
                      result)
        self.assertIn('第3行结果：null', result)

        result_time = self.db_primary_root_node.sh(
            "date '+%Y-%m-%d %H:%M:%S'").result()
        self.log.info(result_time)
        today = []
        today.append((datetime.datetime.strptime(result_time,
                                                 '%Y-%m-%d %H:%M:%S'
                                                 )).strftime('%Y-%m-%dT%H'))
        today.append((datetime.datetime.strptime(result_time,
                                                 '%Y-%m-%d %H:%M:%S') -
                      datetime.timedelta(seconds=+5)
                      ).strftime('%Y-%m-%dT%H'))
        self.log.info(today)
        today = (datetime.datetime.now()).strftime('%Y-%m-%dT%H')
        list_flg = [4, 5, 11]
        for i in list_flg:
            self.assertTrue(f'第{i}行结果：{today[0]}' in result or
                            f'第{i}行结果：{today[1]}' in result)

        self.assertIn(f'第6行结果：2020-03-01T16:59:59Z', result)
        self.assertIn(f'第7行结果：2020-02-29T16:59:59Z', result)
                      result)
        self.assertIn('第10行结果：1970-01-01T00:00Z', result)

        today = []
        today.append((datetime.datetime.strptime(
            result_time, '%Y-%m-%d %H:%M:%S')).strftime("%Y-%m-%dT00:00"))
        today.append((datetime.datetime.strptime(
            result_time, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(
            seconds=+5)).strftime(
            '%Y-%m-%dT00:00'))
        today.append((datetime.datetime.strptime(
            result_time, '%Y-%m-%d %H:%M:%S') -
                      datetime.timedelta(days=-1)).strftime(
            '%Y-%m-%dT00:00'))
        today.append((datetime.datetime.strptime(
            result_time, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(
            days=-1, seconds=+5)).strftime(
            '%Y-%m-%dT00:00'))
        today.append((datetime.datetime.strptime(
            result_time, '%Y-%m-%d %H:%M:%S') -
                      datetime.timedelta(days=+1)).strftime(
            '%Y-%m-%dT00:00'))
        today.append((datetime.datetime.strptime(
            result_time, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(
            days=+1, seconds=+5)).strftime(
            '%Y-%m-%dT00:00'))
        self.log.info(today)

        self.assertTrue(f'第12行结果：{today[0]}' in result or
                        f'第12行结果：{today[1]}' in result)
        self.assertTrue(f'第13行结果：{today[2]}' in result or
                        f'第13行结果：{today[3]}' in result)
        self.assertTrue(f'第14行结果：{today[4]}' in result or
                        f'第14行结果：{today[5]}' in result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"rm -rf {self.targetpath}"
        self.log.info(cmd)
        self.db_primary_root_node.sh(cmd)
        self.log.info("Opengauss_Function_JDBC_Set_Get_Object_Case0013 end")
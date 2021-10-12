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
Case Name   : LocalDateTime类型setObject并发用例
Description :
    1.写配置文件
    2.编译java工具
    3.建表
    4.并发执行java脚本
    5.查询结果
    6.重复step4-5 50次
Expect      :
History     :
"""
import unittest
import os
import datetime
import time
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread


class Jdbcisreadonly(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.db_primary_user_node = Node(node='PrimaryDbUser')
        self.db_primary_root_node = Node(node='PrimaryRoot')
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_JDBC_Set_Get_Object_Case0018 start")
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath,
                                       "jdbc_case0001.properties")
        self.sql_path = os.path.join(self.targetpath, "jdbc_set_get_object")
        self.java_name = "jdbc_set_get_object_case0018"
        self.tb_name = "jdbc_set_get_object_case0018"
        self.common = Common()
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')

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

        self.log.info("---------------3.创建表----------------------")
        cmd = f"drop table if exists {self.tb_name};" \
            f"create table {self.tb_name}(t_time timestamp);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info("-------------4.运行java工具---------------------")
        for index in range(50):
            self.log.info(f"======round {index}========")
            today = self.db_primary_root_node.sh(
                "date '+%Y-%m-%d 00:00:00'").result()
            yesterday = (datetime.datetime.strptime(
                today, '%Y-%m-%d 00:00:00') - datetime.timedelta(days=+1)
                         ).strftime('%Y-%m-%d 00:00:00')
            tomorrow = (datetime.datetime.strptime(
                today, '%Y-%m-%d 00:00:00') - datetime.timedelta(days=-1)
                        ).strftime('%Y-%m-%d 00:00:00')
            self.log.info(f"today is {today}, tomorrow is "
                          f"{tomorrow}, yesterday is {yesterday}")

            cmd = f" java -cp " \
                f"{os.path.join(self.targetpath, 'postgresql.jar')}" \
                f":{self.targetpath} " \
                f"{self.java_name} -F {self.properties}"
            self.log.info(cmd)
            insert_thread = []
            for i in range(9):
                insert_thread.append(ComThread(
                    self.common.get_sh_result,
                    args=(self.db_primary_root_node, cmd)))
                insert_thread[i].setDaemon(True)
                insert_thread[i].start()
            time.sleep(2)
            for i in range(9):
                insert_thread[i].join(30)
                result = insert_thread[i].get_result()
                self.assertNotIn('error', result)

            cmd = f"select * from {self.tb_name} order by 1 desc;"
            insert_result = self.commonshpri.execut_db_sql(cmd)
            self.log.info(insert_result)
            self.assertIn("(126 rows)", insert_result)
            self.assertEqual(insert_result.count('infinity'), 36)
            self.assertEqual(insert_result.count('-infinity'), 18)
            self.assertEqual(insert_result.count('1970-01-01 00:00:00'), 9)
            self.assertEqual(insert_result.count('2020-02-29 23:59:59'), 18)

            result_time = self.db_primary_root_node.sh(
                "date '+%Y-%m-%d %H:%M:%S'").result()
            self.log.info(result_time)
            now = []
            now.append((datetime.datetime.strptime(
                result_time, '%Y-%m-%d %H:%M:%S') -
                        datetime.timedelta(minutes=1)
                        ).strftime('%Y-%m-%d %H:%M'))
            now.append((datetime.datetime.strptime(
                result_time, '%Y-%m-%d %H:%M:%S') -
                        datetime.timedelta(minutes=-1)
                        ).strftime('%Y-%m-%d %H:%M'))
            now.append((datetime.datetime.strptime(
                result_time, '%Y-%m-%d %H:%M:%S')).strftime('%Y-%m-%d %H:%M'))

            self.log.info(f"now is {now}")
            self.assertTrue((insert_result.count(now[0]) +
                            insert_result.count(now[1]) +
                            insert_result.count(now[2])) >= 27)
            self.assertGreaterEqual(insert_result.count(tomorrow), 9)
            self.assertGreaterEqual(insert_result.count(yesterday), 9)
            self.assertGreaterEqual(insert_result.count(today), 9)

            for line in range(2, 10):
                self.assertEqual(' ', insert_result.splitlines()[line])

            cmd = f"delete from {self.tb_name};"
            result = self.commonshpri.execut_db_sql(cmd)
            self.log.info(result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"drop table if exists {self.tb_name};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        cmd = f"rm -rf {self.targetpath}"
        self.log.info(cmd)
        self.db_primary_root_node.sh(cmd)
        self.log.info("-Opengauss_Function_JDBC_Set_Get_Object_Case0018 end-")

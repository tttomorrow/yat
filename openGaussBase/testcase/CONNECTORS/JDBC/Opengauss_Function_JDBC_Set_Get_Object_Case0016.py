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
Case Name   : LocalTime类型setObject并发用例
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
from datetime import date, timedelta
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
        self.log.info("Opengauss_Function_JDBC_Set_Get_Object_Case0016 start")
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath,
                                       "jdbc_case0001.properties")
        self.sql_path = os.path.join(self.targetpath, "jdbc_set_get_object")
        self.java_name = "jdbc_set_get_object_case0016"
        self.tb_name = "jdbc_set_get_object_case0016"
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
            f"create table {self.tb_name}(t_time time);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info("-------------4.运行java工具---------------------")
        today = date.today().strftime("%Y-%m-%d %H:%M:%S")
        tomorrow = (date.today() +
                    timedelta(days=+1)).strftime("%Y-%m-%d %H:%M:%S")
        yesterday = (date.today() +
                     timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
        self.log.info(f"today is {today}, tomorrow is "
                      f"{tomorrow}, yesterday is {yesterday}")
        for index in range(50):
            self.log.info(f"======round {index}========")
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
            self.assertIn("(81 rows)", insert_result)
            self.assertGreaterEqual(insert_result.count('24:00:00'), 9)
            self.assertGreaterEqual(insert_result.count('00:00:00'), 27)
            self.assertGreaterEqual(insert_result.count('23:59:59'), 9)
            self.assertGreaterEqual(insert_result.count('12:00:00'), 9)

            result_time = self.db_primary_root_node.sh(
                "date '+%H:%M:'").result()
            self.log.info(result_time)

            now = [(datetime.datetime.strptime(result_time, '%H:%M:') -
                    datetime.timedelta(minutes=+1)).strftime('%H:%M:'), 
                   (datetime.datetime.strptime(result_time, '%H:%M:')
                    ).strftime('%H:%M:'),
                   (datetime.datetime.strptime(result_time, '%H:%M:') -
                    datetime.timedelta(minutes=-1)).strftime('%H:%M:')]
            self.log.info(f"now is {now}")
            flg1 = [time_flg for time_flg in now if "24:00" in time_flg]
            flg2 = [time_flg for time_flg in now if "23:59" in time_flg]
            flg3 = [time_flg for time_flg in now if "12:00" in time_flg]
            flg4 = [time_flg for time_flg in now if "00:00" in time_flg]
            self.log.info(f"{flg1}, {flg2}, {flg3}, {flg4}")
            if len(flg1) == 0 and len(flg2) == 0 and len(flg3) == 0 \
                    and len(flg4) == 0:
                self.assertTrue((insert_result.count(now[0]) +
                                 insert_result.count(now[1]) +
                                 insert_result.count(now[2])) == 18)

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
        self.log.info("-Opengauss_Function_JDBC_Set_Get_Object_Case0016 end-")

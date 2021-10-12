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
Case Name   : 修改数据库时区，使用getObject获取数据
Description :
    1.修改Timezone
    2.写配置文件
    3.编译java工具
    4.建表并插入数据
    5.并发执行java脚本
Expect      :
History     :
"""
import unittest
import os
import datetime
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
        self.log.info("Opengauss_Function_JDBC_Set_Get_Object_Case0022 start")
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath,
                                       "jdbc_case0001.properties")
        self.sql_path = os.path.join(self.targetpath, "jdbc_set_get_object")
        self.java_name = "jdbc_set_get_object_case0022"
        self.tb_name_time = "jdbc_set_get_object_case0022_time"
        self.tb_name_date = "jdbc_set_get_object_case0022_date"
        self.tb_name_stamptz = "jdbc_set_get_object_case0022_stamptz"
        self.tb_name_stamp = "jdbc_set_get_object_case0022_stamp"
        self.common = Common()
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')

    def test_index(self):
        self.log.info('---------1.修改Timezone-------------------')
        result = self.commonshpri.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            "TimeZOne='Asia/Seoul'")
        self.assertTrue(result)
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

        self.log.info("---------------4.创建表并插入数据----------------------")
        cmd = f"drop table if exists {self.tb_name_date};" \
            f"create table {self.tb_name_date}(t_date date);" \
            f"drop table if exists {self.tb_name_time};" \
            f"create table {self.tb_name_time}(t_date time);" \
            f"drop table if exists {self.tb_name_stamptz};" \
            f"create table {self.tb_name_stamptz}(t_date timestamptz);" \
            f"drop table if exists {self.tb_name_stamp};" \
            f"create table {self.tb_name_stamp}(t_date timestamp);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        time_result = self.db_primary_root_node.sh(
            "date '+%Y-%m-%d %H:%M'").result()
        date_now = [(datetime.datetime.strptime(
            time_result, '%Y-%m-%d %H:%M') - datetime.timedelta(
            hours=-1, minutes=-1)).strftime('%Y-%m-%d %H:%M'),
                    (datetime.datetime.strptime(
                        time_result, '%Y-%m-%d %H:%M') - datetime.timedelta(
                        hours=-1)).strftime('%Y-%m-%d %H:%M')]
        self.log.info(f"date is {date_now}")

        date_now_zone = [(datetime.datetime.strptime(
            time_result, '%Y-%m-%d %H:%M') - datetime.timedelta(
            hours=+8, minutes=-1)).strftime('%Y-%m-%d %H:%M'),
                    (datetime.datetime.strptime(
                        time_result, '%Y-%m-%d %H:%M') - datetime.timedelta(
                        hours=+8)).strftime('%Y-%m-%d %H:%M')]
        self.log.info(f"date_now_zone is {date_now_zone}")

        cmd = f"insert into {self.tb_name_date} values('now');" \
            f"insert into {self.tb_name_time} values('now');" \
            f"insert into {self.tb_name_stamptz} values('now');" \
            f"insert into {self.tb_name_stamp} values('now');"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('INSERT', result)

        self.log.info("-------------5.运行java工具---------------------")
        cmd = f" java -cp {os.path.join(self.targetpath, 'postgresql.jar')}" \
            f":{self.targetpath} " \
            f"{self.java_name} -F {self.properties}"
        select_result = self.common.get_sh_result(
            self.db_primary_root_node, cmd)
        self.assertGreaterEqual(select_result.count(
            f"LocalDate结果：{date_now[0].split(' ')[0]}")
                         + select_result.count(
            f"LocalDate结果：{date_now[1].split(' ')[0]}"), 1)
        self.assertLessEqual(select_result.count(
            f"LocalDate结果：{date_now[0].split(' ')[0]}")
                         + select_result.count(
            f"LocalDate结果：{date_now[1].split(' ')[0]}"), 2)
        self.assertEqual(select_result.count(
            f"LocalTime结果：{date_now[0].split(' ')[1]}")
                         + select_result.count(
            f"LocalTime结果：{date_now[1].split(' ')[1]}"), 1)

        self.log.info(f"OffsetDateTime结果："
                      f"{date_now_zone[0].replace(' ' ,'T')}")
        self.assertTrue(f"OffsetDateTime结果："
                        f"{date_now_zone[0].replace(' ' ,'T')}"
                        in select_result or
                        f"{date_now_zone[1].replace(' ' ,'T')}"
                        in select_result)
        self.assertTrue(f"LocalDateTime结果："
                        f"{date_now[0].replace(' ' ,'T')}"
                        in select_result or
                        f"{date_now[1].replace(' ' ,'T')}"
                        in select_result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"drop table if exists {self.tb_name_stamptz};" \
            f"drop table if exists {self.tb_name_time};" \
            f"drop table if exists {self.tb_name_date};"\
            f"drop table if exists {self.tb_name_stamp};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        result = self.commonshpri.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, "TimeZOne='PRC'")
        self.log.info(result)
        cmd = f"rm -rf {self.targetpath}"
        self.log.info(cmd)
        self.db_primary_root_node.sh(cmd)
        self.log.info("-Opengauss_Function_JDBC_Set_Get_Object_Case0022 end-")

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
Case Type   : GUC
Case Name   : unique_sql自动淘汰-JDBC-PBE验证-P阶段开启自动淘汰
Description :
    1.核对参数默认值
    show enable_auto_clean_unique_sql;
    show enable_resource_track;
    show instr_unique_sql_count;
    show unique_sql_clean_ratio;
    2.写配置文件
    3.编译java工具
        3.1、开启自动淘汰 准备P
        3.2、执行100+1 unique_sql触发自动淘汰 查看记录条数
        3.3、调用B，查看hash table中sql文本串是否为空，
        3.4、清空记录 执行100+1 unique_sql触发自动淘汰，
        3.5、再次调用E，查看hash table中sql文本串是否为空
    4.运行java工具
Expect      :
    1.核对参数默认值
    2.写配置文件成功
    3.编译java工具成功
        3.1、准备P 开启自动淘汰成功
        3.2、执行100+1 unique_sql触发自动淘汰成功 记录条数81
        3.3、调用B，查看hash table中sql文本串不为空
        3.4、清空记录成功 执行100+1 unique_sql触发自动淘汰成功 记录条数81
        3.5、再次调用E，查看hash table中sql文本串不为空
    4.运行java工具成功
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

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class Gucquerytestcase(unittest.TestCase):

    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0039开始执行==")
        self.user_node = Node(node="PrimaryDbUser")
        self.root_node = Node(node="PrimaryRoot")
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath,
                                       "jdbc_uniqque_case0001.properties")
        self.sql_path = os.path.join(self.targetpath, "jdbc_unique_sql")
        self.java_name = "Opengauss_Function_Guc_Query_Case0039"
        self.common = Common()
        self.constant = Constant()
        LOGGER.info("重启数据库")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_guc_query(self):
        LOGGER.info("步骤1：核对参数默认值")
        sql_cmd = COMMONSH.execut_db_sql("show enable_auto_clean_unique_sql;")
        LOGGER.info(sql_cmd)
        if "on" not in sql_cmd:
            res = COMMONSH.execute_gsguc("reload",
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"enable_auto_clean_unique_sql=on")
            LOGGER.info(res)
        sql_cmd = COMMONSH.execut_db_sql("show enable_resource_track;")
        LOGGER.info(sql_cmd)
        if "on" not in sql_cmd:
            result = COMMONSH.execute_gsguc("reload",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"enable_resource_track=on")
            LOGGER.info(result)
        sql_cmd = COMMONSH.execut_db_sql("show instr_unique_sql_count;")
        LOGGER.info(sql_cmd)
        if "100" not in sql_cmd:
            result = COMMONSH.execute_gsguc("reload",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"instr_unique_sql_count=100")
            LOGGER.info(result)
        sql_cmd = COMMONSH.execut_db_sql("show unique_sql_clean_ratio;")
        LOGGER.info(sql_cmd)
        if "0.2" not in sql_cmd:
            result = COMMONSH.execute_gsguc("reload",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"unique_sql_clean_ratio=0.2")
            LOGGER.info(result)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        sql_cmd = COMMONSH.execut_db_sql("show enable_resource_track;"
                                         "show unique_sql_clean_ratio;"
                                         "show instr_unique_sql_count;"
                                         "show enable_auto_clean_unique_sql;")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off", sql_cmd)
        self.assertIn("on", sql_cmd)
        self.assertIn("100", sql_cmd)
        self.assertIn("0.2", sql_cmd)

        LOGGER.info("步骤2：写配置文件")
        self.common.scp_file(self.root_node,
                             f"{self.java_name}.java", self.targetpath)
        result = self.root_node.sh(
            f"touch {self.properties}").result()
        LOGGER.info(result)
        config = f'echo "password={self.user_node.db_password}"> ' \
                 f'{self.properties}'
        self.root_node.sh(config)
        config = f'echo "port={self.user_node.db_port}">> ' \
                 f'{self.properties}'
        self.root_node.sh(config)
        config = f'echo "hostname={self.user_node.db_host}">> ' \
                 f'{self.properties}'
        self.root_node.sh(config)
        config = f'echo "user={self.user_node.db_user}">> ' \
                 f'{self.properties}'
        self.root_node.sh(config)
        config = f'echo "dbname={self.user_node.db_name}">> ' \
                 f'{self.properties}'
        self.root_node.sh(config)
        config = f'echo "stringtype=unspecified">> {self.properties}'
        self.root_node.sh(config)
        config = f'cat {self.properties}'
        result = self.root_node.sh(config).result()
        self.assertTrue("password=" in result and "port=" in result
                        and "hostname=" in result and "user=" in result
                        and "dbname=" in result)

        LOGGER.info("步骤3：编译java工具")
        self.root_node.scp_put(macro.JDBC_PATH,
                               f"{self.targetpath}/postgresql.jar")
        cmd = f"javac -encoding utf-8 -cp " \
              f"{os.path.join(self.targetpath, 'postgresql.jar')} " \
              f"{os.path.join(self.targetpath, f'{self.java_name}.java')}"
        LOGGER.info(cmd)
        result = self.root_node.sh(cmd).result()
        LOGGER.info(result)

        LOGGER.info("步骤4：运行java工具")
        cmd = f" java -cp {os.path.join(self.targetpath, 'postgresql.jar')}" \
              f":{self.targetpath} " \
              f"{self.java_name} -F {self.properties}"
        LOGGER.info(cmd)
        result = self.root_node.sh(cmd).result()
        LOGGER.info(result)
        LOGGER.info("断言调用执行结果")
        self.assertIn("清空hash tablet\t\n", result)
        self.assertIn("查询记录条数2\t\n", result)
        self.assertIn("再次查询记录条数4\t\n", result)
        self.assertIn("查询触发自动淘汰后条数82\t\n", result)
        self.assertIn("查询B/E阶段自动淘汰后记录条数83\t\n", result)
        self.assertIn("查询插入的数据2\t查询插入的数据4\t查询插入的数据6\t\n", result)

        LOGGER.info("查询调用记录和调用次数")
        result = COMMONSH.execut_db_sql("select query,n_calls "
            "from dbe_perf.statement "
            "where query like '%insert into jdbc_unique_table%';")
        LOGGER.info(result)
        self.assertTrue("insert into jdbc_unique_table" in result)
        self.assertNotIn("ERROR", result)
        self.assertIn("1\n", result)

    def tearDown(self):
        LOGGER.info("this is tearDown")
        LOGGER.info("清理环境")
        cmd = f"rm -rf {self.targetpath}"
        LOGGER.info(cmd)
        self.root_node.sh(cmd)
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"unique_sql_clean_ratio=0.1")
        LOGGER.info(result)
        result = COMMONSH.execute_gsguc("reload",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"enable_auto_clean_unique_sql=off")
        LOGGER.info(result)
        LOGGER.info("重启数据库")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_Query_Case0039 执行结束==")

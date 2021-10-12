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
Case Type   : GUC-备机xlog归档
Case Name   : 1主2备 1备archive_dest/archive_command不正确 期望：备机归档成功，日志提示地址错误
Description :
    1.主备查询参数默认值
    show synchronous_standby_names;
    show synchronous_commit;
    show archive_mode;
    show archive_dest;
    2.设置备1 为同步备 备2 异步备 开启归档设置 归档地址错误
    主机设置
    gs_guc reload -D {dn1} -c "synchronous_standby_names='dn_6002'"
    备1设置
    gs_guc reload -D {dn1} -c "archive_mode=on"
    gs_guc reload -D {dn1} -c "archive_dest='/home/$user/testxlog1'"
    备2设置
    gs_guc reload -D {dn1} -c "archive_mode=on"
    gs_guc reload -D {dn1} -c "archive_command=
    'cp --remove-destination %p /home/$user/testxlog2/%f' "
    3.查看主备归档路径 主机执行xlog切换 查看主备归档路径
    ll /home/$user/xlog
    select pg_switch_xlog();
    ll /home/$user/xlog
    4.恢复环境
    rm -rf /home/$user/xlog
    gs_guc reload -D {dn1} -c "synchronous_standby_names='*'"
    gs_guc reload -D {dn1} -c "archive_mode=off"
    gs_guc reload -D {dn1} -c "archive_dest=''"
    gs_guc reload -D {dn1} -c "archive_command='(disabled)'"
Expect      :
    1.显示默认值
    2.设置成功，重启成功
    3.切换成功  .ready文件生成正常，但2备不生成归档日志
    4.清理环境
History     :
"""

import time
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class Guctestcase(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_WAL_Case0098 start==")
        self.userNode = Node("PrimaryDbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.s_com1 = CommonSH("Standby1DbUser")
        self.s_com2 = CommonSH("Standby2DbUser")
        self.common = Common()
        self.constant = Constant()
        self.path = f"{macro.DB_INSTANCE_PATH}/../sxlog"
        self.command = f"cp --remove-destination %p {self.path}2/%f"
        self.log_path = f"{macro.PG_LOG_PATH}/dn_6003"
        LOGGER.info("重启检查数据库状态")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.full_node_list = [self.userNode, self.s_node1, self.s_node2]
        self.full_com_list = [COMMONSH, self.s_com1, self.s_com2]

        LOGGER.info("查询synchronous_standby_names默认值")
        result = COMMONSH.execut_db_sql("show synchronous_standby_names")
        LOGGER.info(f"primary synchronous_standby_names is {result}")
        self.synchronous_standby_names_p = result.strip().splitlines()[-2]

    def set_guc(self, param, value, method="set", com=COMMONSH, single=False):
        sql_cmd = com.execut_db_sql(f"show {param}")
        LOGGER.info(sql_cmd)
        if f"{value}" != sql_cmd.splitlines()[-2].strip():
            com.execute_gsguc(method,
                              self.constant.GSGUC_SUCCESS_MSG,
                              f"{param}={value}",
                              single=f"{single}")
        LOGGER.info(f"{param} is {value}")

    def switch_xlog(self, com=COMMONSH):
        for j in range(60):
            result = com.execut_db_sql("select pg_is_in_recovery()")
            LOGGER.info(result)
            if "f\n" in result:
                result = com.execut_db_sql("select pg_switch_xlog();")
                LOGGER.info(result)
                self.assertTrue("/" in result)
                break
            else:
                time.sleep(10)

    def count_xlog_increase(self, node, sql):
        for i in range(3):
            num_x1 = int(node.sh(sql).result())
            LOGGER.info(num_x1)
            time.sleep(10)
            num_x2 = int(node.sh(sql).result())
            LOGGER.info(num_x2)
            if num_x1 != num_x2:
                time.sleep(10)
            else:
                break

        LOGGER.info("切换pg_xlog触发归档")
        self.switch_xlog()

        time.sleep(30)
        LOGGER.info("核对归档文件+1")
        num_x3 = int(node.sh(sql).result())
        LOGGER.info(num_x3)
        self.assertEqual(num_x2 + 1, num_x3)

    def test_standby_xlog(self):
        LOGGER.info("执行前：主备所有节点查询参数,确保默认值")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)

        LOGGER.info("执行前 删除所有节点上归档目录")
        LOGGER.info("1主2备删除归档地址")
        for node in self.full_node_list:
            sql = f"rm -rf {self.path}1 {self.path}2;" \
                  f"ls {self.path}1;ls {self.path}2"
            LOGGER.info(sql)
            result = self.common.get_sh_result(node, sql)
            LOGGER.info(result)
            self.assertIn("No such file or directory", result)

        LOGGER.info("步骤1：主机设置")
        self.set_guc("synchronous_standby_names", "'dn_6002'", "reload",
                     single=True)
        self.set_guc("synchronous_commit", "on", "reload")

        sql_cmd = COMMONSH.execut_db_sql("show synchronous_standby_names;"
                                         "show synchronous_commit;"
                                         "show archive_dest;")
        LOGGER.info(sql_cmd)
        self.assertIn("dn_6002\n", sql_cmd)
        self.assertNotIn("off\n", sql_cmd)
        self.assertIn("on\n", sql_cmd)
        self.assertIn("\n", sql_cmd)

        LOGGER.info("步骤2：备1备2分别设置")
        self.set_guc("archive_dest", f"'{self.path}1'", "reload", self.s_com1,
                     True)
        self.set_guc("archive_mode", "on", "reload", self.s_com1, True)

        self.set_guc("archive_command", f"'{self.command}'", "reload",
                     self.s_com2, True)
        self.set_guc("archive_mode", "on", "reload", self.s_com2, True)

        sql_cmd = self.s_com1.execut_db_sql(
            "show archive_mode;show archive_dest")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off\n", sql_cmd)
        self.assertIn("on\n", sql_cmd)
        self.assertIn(f"{self.path}1\n", sql_cmd)

        sql_cmd = self.s_com2.execut_db_sql(
            "show archive_mode;show archive_command")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off\n", sql_cmd)
        self.assertIn("on\n", sql_cmd)
        self.assertIn(f"{self.command}\n", sql_cmd)

        LOGGER.info("步骤3：切换日志查看归档")
        time.sleep(30)
        result = self.common.get_sh_result(self.s_node1, f"ls {self.path}1")
        LOGGER.info(result)
        self.assertNotIn("No such file or directory", result)
        LOGGER.info("备1归档文件+1")
        sql = f'''cd {self.path}1;ls -l|grep "^-"| wc -l'''
        self.count_xlog_increase(self.s_node1, sql)

        LOGGER.info("主机+备2归档文件为0")
        sql = f'''cd {self.path}2;ls -l|grep "^-"| wc -l'''
        result = self.userNode.sh(sql).result()
        LOGGER.info(result)
        self.assertIn("No such file or directory", result)
        result = self.s_node2.sh(sql).result()
        LOGGER.info(result)
        self.assertIn("No such file or directory", result)

        LOGGER.info("获取最新日志 查看日志提示")
        sql = f'''cd {self.log_path};\
            echo "`pwd`/`ls -t {self.log_path}|head -n1`"'''
        file_name = self.common.get_sh_result(self.s_node2, sql)
        LOGGER.info(file_name)
        sql = f"cat {file_name} | grep 'not exists'"
        result = self.s_node2.sh(sql).result()
        LOGGER.info(result)
        self.assertIn("", result)
        self.assertNotIn("No such file or directory", result)

    def tearDown(self):
        LOGGER.info("步骤4：恢复默认值")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)
            self.set_guc("archive_timeout", 0, "reload")

        self.set_guc("synchronous_standby_names",
                     f"'{self.synchronous_standby_names_p}'",
                     "reload", COMMONSH, True)

        LOGGER.info("1主2备删除归档地址")
        for node in self.full_node_list:
            sql = f"rm -rf {self.path}1 {self.path}2;" \
                  f"ls {self.path}1;ls {self.path}2"
            LOGGER.info(sql)
            result = self.common.get_sh_result(node, sql)
            LOGGER.info(result)

        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_WAL_Case0098 finish==")

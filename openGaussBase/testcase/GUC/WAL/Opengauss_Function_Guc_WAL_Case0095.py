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
Case Name   : 1主2备 主机不开启归档  1同步+1异步备机不开启归档模式 期望：主备均不归档 日志不提示
Description :
    1.主备查询参数默认值
    show synchronous_standby_names;
    show synchronous_commit;
    show archive_mode;
    show archive_command;
    show archive_timeout;
    2.1主2备创建xlog归档地址
    rm -rf /home/$user/xlog
    mkdir /home/$user/xlog
    3.1主2备设置为1同步1异步并开启归档
    主机设置
    gs_guc reload -D {dn1} -c "synchronous_standby_names='dn_6002'"
    gs_guc reload -D {dn1} -c "archive_timeout=30"
    2备机设置
    gs_guc reload -D {dn1} -c "archive_command=
    'cp --remove-destination %p /home/$user/xlog/%f'"
    4.查看主备归档路径 等待30s 查看主备归档路径
    ll /home/$user/xlog
    select pg_sleep(30);
    ll /home/$user/xlog
    5.1主2备恢复并清理环境
    rm -rf /home/$user/xlog
    gs_guc reload -D {dn1} -c "synchronous_standby_names='*'"
    gs_guc reload -D {dn1} -c "archive_mode=off"
    gs_guc reload -D {dn1} -c "archive_command='(disabled)'"
    gs_guc reload -D {dn1} -c "archive_timeout=0"
Expect      :
    1.显示默认值
    2.创建归档地址成功
    3.设置成功，重启成功
    4.1主2备不归档 归档路径下无归档文件生成
    5.清理环境
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
        LOGGER.info("==Opengauss_Function_Guc_WAL_Case0095 start==")
        self.userNode = Node("PrimaryDbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.s_com1 = CommonSH("Standby1DbUser")
        self.s_com2 = CommonSH("Standby2DbUser")
        self.common = Common()
        self.constant = Constant()
        self.path = f"{macro.DB_INSTANCE_PATH}/../sxlog"
        LOGGER.info("重启检查数据库状态")
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.full_com_list = [COMMONSH, self.s_com1, self.s_com2]
        self.full_node_list = [self.userNode, self.s_node1, self.s_node2]

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

    def test_standby_xlog(self):
        LOGGER.info("执行前：主备所有节点查询参数,确保默认值")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)

        LOGGER.info("步骤1：1主2备创建归档地址")
        for node in self.full_node_list:
            sql = f"rm -rf {self.path};mkdir {self.path};ls {self.path}"
            LOGGER.info(sql)
            result = self.common.get_sh_result(node, sql)
            LOGGER.info(result)
            self.assertNotIn("No such file or directory", result)

        LOGGER.info("步骤2+3：主机设置")
        self.set_guc("synchronous_standby_names", "'dn_6002'", "reload",
                     COMMONSH, True)
        self.set_guc("synchronous_commit", "on", "reload")
        self.set_guc("archive_timeout", "60", "reload")

        sql_cmd = COMMONSH.execut_db_sql("show synchronous_standby_names;"
                                         "show synchronous_commit;"
                                         "show archive_mode;"
                                         "show archive_timeout;"
                                         "show archive_dest;")
        LOGGER.info(sql_cmd)
        self.assertIn("dn_6002", sql_cmd)
        self.assertIn("off\n", sql_cmd)
        self.assertIn("on\n", sql_cmd)
        self.assertIn("1min\n", sql_cmd)

        LOGGER.info("步骤2+3：备1+2设置")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com, True)
            self.set_guc("archive_dest", f"'{self.path}'",
                         "reload", com, True)
            self.set_guc("archive_timeout", 30, "reload", com, True)

            sql_cmd = com.execut_db_sql("show archive_mode;"
                                        "show archive_dest;"
                                        "show archive_timeout;")
            LOGGER.info(sql_cmd)
            self.assertNotIn("on\n", sql_cmd)
            self.assertIn("off\n", sql_cmd)
            self.assertIn("30s\n", sql_cmd)
            self.assertIn(f"{self.path}\n", sql_cmd)

        LOGGER.info("步骤4：查看1主2备机归档")
        sql = f'''cd {self.path};ls -l|grep "^-"| wc -l'''
        for node in self.full_node_list:
            num_x1 = int(node.sh(sql).result())
            LOGGER.info(num_x1)
            self.assertEqual(num_x1, 0)

            LOGGER.info("等待archive_timeout:30s")
            time.sleep(30)

            LOGGER.info("核对1主2备 归档文件为0")
            num_x2 = int(node.sh(sql).result())
            LOGGER.info(num_x2)
            self.assertEqual(num_x2, 0)

    def tearDown(self):
        LOGGER.info("步骤5：恢复默认值")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)
            self.set_guc("archive_timeout", 0, "reload")

        self.set_guc("synchronous_standby_names",
                     f"'{self.synchronous_standby_names_p}'",
                     "reload", COMMONSH, True)

        LOGGER.info("1主2备删除归档地址")
        for node in self.full_node_list:
            sql = f"rm -rf {self.path};ls {self.path}"
            LOGGER.info(sql)
            result = self.common.get_sh_result(node, sql)
            LOGGER.info(result)

        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_WAL_Case0095 finish==")

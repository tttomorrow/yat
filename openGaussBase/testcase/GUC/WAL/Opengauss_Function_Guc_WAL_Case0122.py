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
Case Name   : 1+2failover后，新主机开启归档模式，设置1同步不开启归档 1异步开启归档 期望：异步归档成功
Description :
    1.主备查询参数默认值
    show synchronous_standby_names;
    show synchronous_commit;
    show archive_mode;
    show archive_dest;
    2.1主2备创建xlog归档地址
    rm -rf /home/$user/xlog
    mkdir /home/$user/xlog
    3.备1上执行failover 进行主备切换
    gs_ctl failover -D dn1
    gs_om -t refreshconf
    在主机上以备机启动
    gs_ctl start -D dn1 -M standby
    4.设置1同步不开启归档 1异步开启归档
    新主机
    gs_guc reload -D {dn1} -c "synchronous_standby_names='dn_6002'"
    gs_guc reload -D {dn1} -c "archive_mode=on"
    原主机现备1
    gs_guc reload -D {dn1} -c "archive_mode=on"
    gs_guc reload -D {dn1} -c "archive_dest='/home/$user/xlog'"
    备2
    gs_guc reload -D {dn1} -c "archive_mode=off"
    gs_guc reload -D {dn1} -c "archive_dest='/home/$user/xlog'"
    gs_om -t restart
    5.执行切换日志后 查看归档路径 归档文件
    select pg_switch_xlog();
    ll /home/$user/xlog
    6.恢复环境
    gs_ctl switchover -D dn1
    gs_om -t refreshconf
    rm -rf /home/$user/xlog
    gs_guc reload -D {dn1} -c "archive_mode=off"
    gs_guc reload -D {dn1} -c "archive_dest=''"
    gs_om -t restart
Expect      :
    1.显示默认值
    2.1主2备创建xlog归档地址成功
    3.failover成功 在主机上以备机启动成功
    4.设置1同步不开启归档 1异步开启归档成功
    5.pg_switch_xlog后主备归档文件数量均不变
    6.恢复环境
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
        LOGGER.info("==Opengauss_Function_Guc_WAL_Case0122 start==")
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

    def count_xlog_increase(self, node, sql, com):
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
        self.switch_xlog(com)

        time.sleep(10)
        LOGGER.info("核对归档文件+1")
        num_x3 = int(node.sh(sql).result())
        LOGGER.info(num_x3)
        if num_x2 + 1 == num_x3:
            return True
        else:
            return False

    def test_standby_xlog(self):
        LOGGER.info("步骤1:主备所有节点查询参数,确保默认值")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)
            self.set_guc("archive_timeout", "0", "reload", com)

        LOGGER.info("步骤2：1主2备创建归档地址")
        for node in self.full_node_list:
            sql = f"rm -rf {self.path};mkdir {self.path};ls {self.path}"
            LOGGER.info(sql)
            result = self.common.get_sh_result(node, sql)
            LOGGER.info(result)
            self.assertNotIn("No such file or directory", result)

        LOGGER.info("步骤3：执行failover")
        result = COMMONSH.stop_db_instance()
        LOGGER.info(result)
        self.assertIn("server stopped", result)

        result = self.s_com2.execute_gsctl("failover",
                                           "failover completed")
        LOGGER.info(result)
        self.assertTrue(result)

        result = self.s_com2.exec_refresh_conf()
        LOGGER.info(result)
        self.assertTrue(result)

        LOGGER.info("原主机以备机启动")
        result = COMMONSH.execute_gsctl("build",
                                        "server started",
                                        param="-M standby")
        LOGGER.info(result)
        self.assertTrue(result)

        result = COMMONSH.execute_gsctl("build",
                                        "server started",
                                        param="-b full")
        LOGGER.info(result)
        self.assertTrue(result)

        result = self.s_com2.get_db_cluster_status("detail")
        LOGGER.info(result)
        self.assertTrue("S Primary Normal" in result
                        and "P Standby Normal" in result
                        and "S Standby Normal" in result)

        LOGGER.info("步骤4：主机设置")
        self.set_guc("synchronous_standby_names", "'dn_6002'", "reload",
                     self.s_com2, True)
        self.set_guc("synchronous_commit", "on", "reload", self.s_com2)

        sql_cmd = self.s_com2.execut_db_sql("show synchronous_standby_names;"
                                            "show synchronous_commit;"
                                            "show archive_dest;")
        LOGGER.info(sql_cmd)
        self.assertIn("dn_6002", sql_cmd)
        self.assertNotIn("off\n", sql_cmd)
        self.assertIn("on\n", sql_cmd)

        LOGGER.info("异步备设置开启归档")
        result = self.s_com2.get_db_cluster_status("detail")
        LOGGER.info(result)
        self.set_guc("archive_dest", f"'{self.path}'",
                     "reload", COMMONSH, True)
        self.set_guc("archive_mode", "on", "reload", COMMONSH, True)
        result = self.s_com2.get_db_cluster_status("detail")
        LOGGER.info(result)
        sql_cmd = COMMONSH.execut_db_sql("show archive_mode;"
                                         "show archive_dest;")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off\n", sql_cmd)
        self.assertIn("on\n", sql_cmd)
        self.assertIn(f"{self.path}\n", sql_cmd)

        LOGGER.info("sleep 60 等待已有xlog完成归档")
        time.sleep(60)

        LOGGER.info("步骤5：查看主备归档")
        sql = f'''cd {self.path};ls -l|grep "^-"| wc -l'''
        for i in range(3):
            num_x1 = int(self.s_node1.sh(sql).result())
            LOGGER.info(num_x1)
            time.sleep(10)
            num_x2 = int(self.s_node1.sh(sql).result())
            LOGGER.info(num_x2)
            if num_x1 != num_x2:
                time.sleep(10)
            else:
                break

        LOGGER.info("备2 查看归档文件")
        result = self.count_xlog_increase(self.userNode, sql, self.s_com2)
        LOGGER.info(result)
        self.assertTrue(result)

        LOGGER.info("新主机-原2 和 备1 归档文件为0")
        num_x4 = int(self.s_node1.sh(sql).result())
        LOGGER.info(num_x4)
        self.assertEqual(0, num_x4)
        num_x5 = int(self.s_node2.sh(sql).result())
        LOGGER.info(num_x5)
        self.assertEqual(0, num_x5)

    def tearDown(self):
        LOGGER.info("步骤6：恢复默认值")
        LOGGER.info("主备切换")
        result = self.s_com2.get_db_cluster_status("detail")
        LOGGER.info(result)
        if "S Primary" in result or "P Standby" in result:
            result = COMMONSH.execute_gsctl("restart",
                                            "server started",
                                            param="-M standby")
            LOGGER.info(result)
            result = COMMONSH.execute_gsctl("build",
                                            "server started",
                                            param="-b full")
            LOGGER.info(result)
            result = COMMONSH.execute_gsctl("switchover",
                                            "switchover completed")
            LOGGER.info(result)

            result = COMMONSH.exec_refresh_conf()
            LOGGER.info(result)

        LOGGER.info("恢复参数")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)

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
        LOGGER.info("==Opengauss_Function_Guc_WAL_Case0122 finish==")

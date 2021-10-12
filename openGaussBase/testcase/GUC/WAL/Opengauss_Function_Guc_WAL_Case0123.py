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
Case Name   : 1+2switchover后failover，在新主机开启归档，设置2同步备机归档 期望:2备机归档成功
Description :
    1.主备查询参数默认值
    show synchronous_standby_names;
    show synchronous_commit;
    show archive_mode;
    show archive_dest;
    2.1主2备创建xlog归档地址
    rm -rf /home/$user/xlog
    mkdir /home/$user/xlog
    3.备1执行执行switchover 进行主备切换
    gs_ctl switchover -D dn1
    gs_om -t refreshconf
    4.备2上执行failover 进行主备切换
    gs_ctl failover -D dn1
    gs_om -t refreshconf
    在新主机上以备机启动
    gs_ctl start -D dn1 -M standby
    5.设置新主机和现备1+2 开启归档设置
    gs_guc reload -D {dn1} -c "synchronous_standby_names='*'"
    gs_guc reload -D {dn1} -c "archive_mode=on"
    gs_guc reload -D {dn1} -c "archive_dest='/home/$user/xlog'"
    gs_om -t restart
    6.执行切换日志后 查看归档路径 归档文件
    select pg_switch_xlog();
    ll /home/$user/xlog
    7.恢复环境
    gs_ctl switchover -D dn1
    gs_om -t refreshconf
    gs_ctl switchover -D dn1
    gs_om -t refreshconf
    rm -rf /home/$user/xlog
    gs_guc reload -D {dn1} -c "archive_mode=off"
    gs_guc reload -D {dn1} -c "archive_dest=''"
    gs_om -t restart
Expect      :
    1.显示默认值
    2.1主2备创建xlog归档地址成功
    3.switchover成功
    4.failover成功
    5.开启归档设置成功
    6.pg_switch_xlog后备1归档文件+1
    7.清理环境
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


@unittest.skipIf(1 == CommonSH("PrimaryDbUser").get_node_num(), "单机不执行")
class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.primary_sh = CommonSH("PrimaryDbUser")
        self.log.info("==Opengauss_Function_Guc_WAL_Case0123 start==")
        self.userNode = Node("PrimaryDbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.s_com1 = CommonSH("Standby1DbUser")
        self.s_com2 = CommonSH("Standby2DbUser")
        self.common = Common()
        self.constant = Constant()
        self.path = f"{macro.DB_INSTANCE_PATH}/../sxlog"
        self.log.info("重启检查数据库状态")
        status = self.primary_sh.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = self.primary_sh.restart_db_cluster()
        self.log.info(status)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.full_com_list = [self.primary_sh, self.s_com1, self.s_com2]
        self.full_node_list = [self.userNode, self.s_node1, self.s_node2]
        self.test_node_list = [self.userNode, self.s_node1]

        self.log.info("查询synchronous_standby_names默认值")
        self.log.info(f"{self.userNode.db_name}")
        result = self.primary_sh.execut_db_sql(
            "show synchronous_standby_names")
        self.log.info(f"primary synchronous_standby_names is {result}")
        self.synchronous_standby_names_p = result.strip().splitlines()[-2]
        self.log.info("查询log_min_messages默认值")
        result = self.primary_sh.execut_db_sql("show log_min_messages;")
        self.log.info(result)
        self.log.info(f"primary log_min_messages is {result}")
        self.log_min_messages = result.strip().splitlines()[-2].strip()

    def set_guc(self, param, value, method="set",
                com=CommonSH("PrimaryDbUser"), single=False):
        sql_cmd = com.execut_db_sql(f"show {param}")
        self.log.info(sql_cmd)
        if f"{value}" != sql_cmd.splitlines()[-2].strip():
            com.execute_gsguc(method,
                              self.constant.GSGUC_SUCCESS_MSG,
                              f"{param}={value}",
                              single=f"{single}")
        self.log.info(f"{param} is {value}")

    def switch_xlog(self, com=CommonSH("PrimaryDbUser")):
        for j in range(60):
            result = com.execut_db_sql("select pg_is_in_recovery()")
            self.log.info(result)
            if "f\n" in result:
                result = com.execut_db_sql("select pg_switch_xlog();")
                self.log.info(result)
                self.assertTrue("/" in result)
                break
            else:
                time.sleep(10)

    def count_xlog_increase(self, node, sql, com):
        for i in range(3):
            num_x1 = int(node.sh(sql).result())
            self.log.info(num_x1)
            time.sleep(10)
            num_x2 = int(node.sh(sql).result())
            self.log.info(num_x2)
            if num_x1 != num_x2:
                time.sleep(10)
            else:
                break

        self.log.info("切换pg_xlog触发归档")
        self.switch_xlog(com)

        time.sleep(10)
        self.log.info("核对归档文件+1")
        num_x3 = int(node.sh(sql).result())
        self.log.info(num_x3)
        if num_x2 + 1 == num_x3:
            return True
        else:
            return False

    def test_standby_xlog(self):
        text = "--step1:执行前:主备所有节点查询参数,确保默认值;expect:成功"
        self.log.info(text)
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)
            self.set_guc("archive_timeout", "0", "reload", com)
            self.set_guc("log_min_messages", "debug1", "reload", com)

        text = "--step2:1主2备创建归档地址;expect:成功"
        self.log.info(text)
        for node in self.full_node_list:
            sql = f"rm -rf {self.path};mkdir {self.path};ls {self.path}"
            self.log.info(sql)
            result = self.common.get_sh_result(node, sql)
            self.log.info(result)
            self.assertNotIn("No such file or directory", result,
                             "执行失败" + text)

        text = "--step3:执行switchover;expect:成功"
        self.log.info(text)
        result = self.s_com1.execute_gsctl("switchover",
                                           "switchover completed")
        self.log.info(result)
        self.assertTrue(result, "执行失败" + text)

        result = self.s_com1.exec_refresh_conf()
        self.log.info(result)
        self.assertTrue(result, "执行失败" + text)

        text = "--step4:执行failover;expect:成功"
        self.log.info(text)
        result = self.s_com1.stop_db_instance()
        self.log.info(result)
        self.assertIn("server stopped", result, "执行失败" + text)

        result = self.s_com2.execute_gsctl("failover",
                                           "failover completed")
        self.log.info(result)
        self.assertTrue(result, "执行失败" + text)

        result = self.s_com2.exec_refresh_conf()
        self.log.info(result)
        self.assertTrue(result, "执行失败" + text)

        self.log.info("原主机以备机启动")
        result = self.s_com1.execute_gsctl("start",
                                           "server started",
                                           param="-M standby")
        self.log.info(result)
        self.assertTrue(result, "执行失败" + text)

        result = self.primary_sh.execute_gsctl("build",
                                               "server started",
                                               param="-b full")
        self.log.info(result)
        self.assertTrue(result, "执行失败" + text)

        result = self.s_com2.get_db_cluster_status("detail")
        self.log.info(result)
        self.assertTrue("S Primary Normal" in result
                        and "P Standby Normal" in result
                        and "S Standby Normal" in result, "执行失败" + text)

        text = "--step5:主机设置;expect:成功"
        self.log.info(text)
        self.set_guc("synchronous_standby_names", "'*'", "reload",
                     self.s_com2, True)
        self.set_guc("synchronous_commit", "on", "reload", self.s_com2)

        sql_cmd = self.s_com2.execut_db_sql("show synchronous_standby_names;"
                                            "show synchronous_commit;"
                                            "show archive_mode;")
        self.log.info(sql_cmd)
        self.assertIn("*\n", sql_cmd, "执行失败" + text)
        self.assertIn("off\n", sql_cmd, "执行失败" + text)
        self.assertIn("on\n", sql_cmd, "执行失败" + text)

        text = "1主+2备机设置开启归档;expect:成功"
        self.log.info(text)
        for com in self.full_com_list:
            self.set_guc("archive_dest", f"'{self.path}'",
                         "reload", com, True)
            self.set_guc("archive_mode", "on", "reload", com, True)
            self.log.info("核对参数设置")
            sql_cmd = com.execut_db_sql("show archive_mode;"
                                        "show archive_dest;")
            self.log.info(sql_cmd)
            self.assertNotIn("off\n", sql_cmd, "执行失败" + text)
            self.assertIn("on\n", sql_cmd, "执行失败" + text)
            self.assertIn(f"{self.path}\n", sql_cmd, "执行失败" + text)
            self.log.info("核对参数完成")

        self.log.info("sleep 60 等待已有xlog完成归档")
        time.sleep(60)

        text = "--step6:查看主备归档;expect:归档文件+1"
        self.log.info(text)
        sql = f'''cd {self.path};ls -l|grep "^-"| wc -l'''
        for node in self.full_node_list:
            for i in range(3):
                num_x1 = int(node.sh(sql).result())
                self.log.info(num_x1)
                time.sleep(30)
                num_x2 = int(node.sh(sql).result())
                self.log.info(num_x2)
                if num_x1 != num_x2:
                    time.sleep(30)
                else:
                    break

        self.log.info("所有节点 查看归档文件")
        for node in self.test_node_list:
            result = self.count_xlog_increase(node, sql, self.s_com2)
            self.log.info(result)
            self.assertTrue(result, "执行失败" + text)

        self.log.info("核对现主机-备2")
        result = self.common.get_sh_result(self.s_node2, f"ls -l {self.path}")
        self.log.info("已归档文件")
        self.log.info(result)
        result = self.common.get_sh_result(self.s_node2,
                                           f"ls -l {macro.PG_XLOG_PATH}")
        self.log.info("现有xlog")
        self.log.info(result)
        result = self.common.get_sh_result(self.s_node2,
            f"ls -l {macro.DB_INSTANCE_PATH}/archive_status")
        self.log.info("现有archive_status")
        self.log.info(result)
        self.log.info("--计数--")
        num_s21 = int(self.s_node2.sh(sql).result())
        self.log.info(num_s21)
        self.log.info("--切换--")
        self.switch_xlog(self.s_com2)
        self.log.info("--再次计数--")
        num_s22 = int(self.s_node2.sh(sql).result())
        self.log.info(num_s22)
        self.log.info("核对现主机-备2")
        result = self.common.get_sh_result(self.s_node2, f"ls -l {self.path}")
        self.log.info("已归档文件")
        self.log.info(result)
        result = self.common.get_sh_result(self.s_node2,
                                           f"ls -l {macro.PG_XLOG_PATH}")
        self.log.info("现有xlog")
        self.log.info(result)
        result = self.common.get_sh_result(self.s_node2,
            f"ls -l {macro.DB_INSTANCE_PATH}/archive_status")
        self.log.info("现有archive_status")
        self.log.info(result)
        self.log.info("--执行断言--")
        self.assertEqual(num_s21 + 1, num_s22, "执行失败" + text)

    def tearDown(self):
        text = "--step7:恢复默认值expect:成功"
        self.log.info(text)
        self.log.info("主备切换")
        result = self.s_com2.get_db_cluster_status("detail")
        self.log.info(result)
        if "S Primary" in result or "P Standby" in result:
            result = self.primary_sh.execute_gsctl("start",
                                                   "server started",
                                                   param="-M standby")
            self.log.info(result)
            result = self.primary_sh.execute_gsctl("build",
                                                   "server started",
                                                   param="-b full")
            self.log.info(result)
            result = self.primary_sh.execute_gsctl("switchover",
                                                   "switchover completed")
            self.log.info(result)

            result = self.primary_sh.exec_refresh_conf()
            self.log.info(result)

        self.log.info("恢复参数")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)
            self.set_guc("log_min_messages", f"{self.log_min_messages}",
                         "reload")

        self.set_guc("synchronous_standby_names",
                     f"'{self.synchronous_standby_names_p}'",
                     "reload", self.primary_sh, True)

        self.log.info("1主2备删除归档地址")
        for node in self.full_node_list:
            sql = f"rm -rf {self.path};ls {self.path}"
            self.log.info(sql)
            result = self.common.get_sh_result(node, sql)
            self.log.info(result)

        status = self.primary_sh.restart_db_cluster()
        self.log.info(status)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败" + text)
        self.log.info("==Opengauss_Function_Guc_WAL_Case0123 finish==")

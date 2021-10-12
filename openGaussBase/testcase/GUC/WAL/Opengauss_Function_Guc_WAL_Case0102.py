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
Case Name   : 设置清理参数，归档开启后再关闭，等待一部分日志被清理，再开启归档
Description :
    1.主备查询参数默认值
    show synchronous_standby_names;
    show synchronous_commit;
    show archive_mode;
    show archive_dest;
    show checkpoint_segments;
    2.1主2备创建xlog归档地址
    rm -rf /home/$user/xlog
    mkdir /home/$user/xlog
    3.设置同步备 开启归档设置
    主机执行
    gs_guc reload -D {dn1} -c "checkpoint_segments=55"
    备机2执行
    gs_guc reload -D {dn1} -c "archive_mode=on"
    gs_guc reload -D {dn1} -c "archive_dest='/home/$user/xlog'"
    4.查看主备归档路径文件数量 等待归档数量稳定
    ll /home/$user/xlog
    5.关闭备机2归档
    gs_guc reload -D {dn1} -c "archive_mode=off"
    6.主机循环100次执行日志切换
    for i in range(100):
        select pg_switch_xlog();
    7.开启备机2归档
    gs_guc reload -D {dn1} -c "archive_mode=off"
    8.查看主备归档路径 确认主机正在写的日志之前全部归档，预置不归档
    ll /home/$user/xlog
    按修改时间排序-对比主xlog与备机归档的xlog
    主机xlog数量比备机xlog多1 有1正在写
    当前写的xlog不能被归档
    当前写的xlog之前的所有xlog被归档
    9.恢复环境
    rm -rf /home/$user/xlog
    gs_guc reload -D {dn1} -c "archive_mode=off"
    gs_guc reload -D {dn1} -c "checkpoint_segments=64"
    gs_guc reload -D {dn1} -c "archive_dest=''"
Expect      :
    1.显示默认值
    2.创建归档地址成功
    3.设置成功 开启归档成功
    4.归档文件数量稳定为num
    5.关闭备机2归档成功
    6.切换成功
    7.开启归档成功
    8.主机不归档 备机归档文件小于num+100
    主机正在写的日志之前全部归档，预置不归档
    9.清理环境
History     :switch切换xlog直到最新的xlog被清理
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
        LOGGER.info("==Opengauss_Function_Guc_WAL_Case0102 start==")
        self.userNode = Node("PrimaryDbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.s_com1 = CommonSH("Standby1DbUser")
        self.s_com2 = CommonSH("Standby2DbUser")
        self.common = Common()
        self.constant = Constant()
        self.path = f"{macro.DB_INSTANCE_PATH}/../sxlog"
        self.xlog_path = f"{macro.PG_XLOG_PATH}"

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

        time.sleep(10)
        LOGGER.info("核对1主1备 归档文件+1")
        num_x3 = int(node.sh(sql).result())
        LOGGER.info(num_x3)
        self.assertEqual(num_x2 + 1, num_x3)

    def test_standby_xlog(self):
        LOGGER.info("执行前：主备所有节点查询参数,确保默认值")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)

        LOGGER.info("步骤1：备2创建归档地址")
        sql = f"rm -rf {self.path};mkdir {self.path};ls {self.path}"
        LOGGER.info(sql)
        result = self.common.get_sh_result(self.s_node2, sql)
        LOGGER.info(result)
        self.assertNotIn("No such file or directory", result)

        LOGGER.info("步骤2+3：主机设置")
        self.set_guc("synchronous_standby_names", "'*'",
                     "reload", COMMONSH, True)
        self.set_guc("synchronous_commit", "on", "reload")

        sql_cmd = COMMONSH.execut_db_sql("show synchronous_standby_names;"
                                         "show synchronous_commit;"
                                         "show archive_dest;")
        LOGGER.info(sql_cmd)
        self.assertIn("*", sql_cmd)
        self.assertNotIn("off\n", sql_cmd)
        self.assertIn("on\n", sql_cmd)

        LOGGER.info("步骤2+3：备2设置开启归档")
        self.set_guc("archive_mode", "on", "reload", self.s_com2, True)
        self.set_guc("archive_dest", f"'{self.path}'",
                     "reload", self.s_com2, True)
        self.set_guc("archive_timeout", 0, "reload", self.s_com2, True)

        sql_cmd = self.s_com2.execut_db_sql("show archive_mode;"
                                            "show archive_dest;"
                                            "show archive_timeout;")
        LOGGER.info(sql_cmd)
        self.assertNotIn("off\n", sql_cmd)
        self.assertIn("on\n", sql_cmd)
        self.assertIn("0\n", sql_cmd)
        self.assertIn(f"{self.path}\n", sql_cmd)

        LOGGER.info("sleep 60 等待已有xlog完成归档")
        time.sleep(60)

        LOGGER.info("步骤4+5：查看备2归档")
        sql = f'''cd {self.path};ls -l|grep "^-"| wc -l'''
        self.switch_xlog()
        LOGGER.info("备2归档文件+1")
        self.count_xlog_increase(self.s_node2, sql)

        LOGGER.info("步骤6：关闭备2归档")
        self.set_guc("archive_mode", "off", "reload", self.s_com2, True)

        LOGGER.info("步骤7：在主机执行switch切换xlog直到最新的xlog被清理")
        sql = f"cd {self.xlog_path};ls -t {self.xlog_path} | head -n1"
        LOGGER.info(sql)
        last_file = self.userNode.sh(sql).result()
        LOGGER.info(last_file)
        self.assertIn("0000", last_file)
        new_last_file = ""
        for i in range(100):
            LOGGER.info(i)
            all_file = self.s_node2.sh(f"ls {self.xlog_path}").result()
            LOGGER.info(all_file)
            self.switch_xlog()
            time.sleep(5)
            if all_file.find(last_file) == -1:
                sql = f'''cd {self.xlog_path};\
                    ls -t {self.xlog_path}/0000* | head -n1'''
                LOGGER.info(sql)
                new_last_file = self.s_node2.sh(sql).result()
                LOGGER.info(new_last_file)
                self.assertIn("0000", new_last_file)
                break

        if new_last_file == "":
            LOGGER.info("执行时间截止前最新的xlog未被清理，执行失败")
            self.assertTrue(False)

        LOGGER.info("步骤8：打开备2归档")
        self.set_guc("archive_mode", "on", "reload", self.s_com2, True)

        LOGGER.info("步骤9：查看备2归档")
        sql = f'''cd {self.path};ls -l|grep "^-"| wc -l'''
        self.switch_xlog()
        LOGGER.info("备2归档文件+1")
        self.count_xlog_increase(self.s_node2, sql)
        LOGGER.info("new_last_file")
        LOGGER.info(new_last_file)
        result = self.common.get_sh_result(self.s_node2,
                                           f"ls {new_last_file}")
        LOGGER.info(result)
        self.assertNotIn("No such file or directory", result)

    def tearDown(self):
        LOGGER.info("步骤9：恢复默认值")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)

        self.set_guc("synchronous_standby_names",
                     f"'{self.synchronous_standby_names_p}'",
                     "reload", COMMONSH, True)

        LOGGER.info("备2删除归档地址")
        sql = f"rm -rf {self.path};ls {self.path}"
        LOGGER.info(sql)
        result = self.common.get_sh_result(self.s_node2, sql)
        LOGGER.info(result)

        status = COMMONSH.restart_db_cluster()
        LOGGER.info(status)
        status = COMMONSH.get_db_cluster_status("detail")
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("==Opengauss_Function_Guc_WAL_Case0102 finish==")

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
Case Name   : 归档期间重启 gs_om重启后正常归档
Description :
    1.1主2备创建xlog归档地址
    rm -rf /home/$user/xlog
    mkdir /home/$user/xlog
    2.主备查询参数默认值
    show synchronous_standby_names;
    show synchronous_commit;
    show archive_mode;
    show archive_dest;
    3.设置备1 开启归档设置
    gs_guc reload -D {dn1} -c "archive_mode=on"
    gs_guc reload -D {dn1} -c "archive_timeout=60"
    gs_guc reload -D {dn1} -c "archive_dest='/home/$user/xlog'"
    4.重启数据库
    gs_om -t restart
    5.查看归档路径 归档文件
    ll /home/$user/xlog
    sleep(60)
    ll /home/$user/xlog
    6.恢复环境
    rm -rf /home/$user/xlog
    gs_guc reload -D {dn1} -c "archive_mode=off"
    gs_guc reload -D {dn1} -c "archive_timeout=0"
    gs_guc reload -D {dn1} -c "archive_dest=''"
Expect      :
    1.创建归档地址成功
    2.显示默认值
    3.设置成功
    4.重启成功
    5.正常归档 切换后备机归档文件+1
    6.清理环境
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
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
        self.log.info("==Opengauss_Function_Guc_WAL_Case0114 start==")
        self.userNode = Node("PrimaryDbUser")
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.s_com1 = CommonSH("Standby1DbUser")
        self.s_com2 = CommonSH("Standby2DbUser")
        self.common = Common()
        self.constant = Constant()
        self.path = f"{macro.DB_INSTANCE_PATH}/../sxlog"
        text = "重启检查数据库状态"
        self.log.info(text)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        status = self.primary_sh.restart_db_cluster()
        self.log.info(status)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败" + text)
        self.full_com_list = [self.primary_sh, self.s_com1, self.s_com2]
        self.full_node_list = [self.userNode, self.s_node1, self.s_node2]

        self.log.info("查询synchronous_standby_names默认值")
        result = self.primary_sh.execut_db_sql("show "
                                               "synchronous_standby_names")
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
                              single=single)
        self.log.info(f"{param} is {value}")

    def test_standby_xlog(self):
        text = "--step1:1主2备创建归档地址;expect:成功"
        self.log.info(text)
        for node in self.full_node_list:
            sql = f"rm -rf {self.path};mkdir {self.path};ls {self.path}"
            self.log.info(sql)
            result = self.common.get_sh_result(node, sql)
            self.log.info(result)
            self.assertNotIn("No such file or directory", result,
                             "执行失败" + text)

        self.log.info("--step2:主备所有节点查询参数,确保默认值;expect:成功")
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)
            self.set_guc("archive_timeout", "0", "reload", com)
            self.set_guc("log_min_messages", "debug1", "reload", com)

        text = "--step3:主备分别设置 开启备1归档;expect:成功"
        self.log.info(text)
        self.set_guc("synchronous_standby_names", "'dn_6002'", "reload",
                     self.primary_sh, True)
        self.set_guc("synchronous_commit", "on", "reload")

        sql_cmd = self.primary_sh.execut_db_sql(
            "show synchronous_standby_names;"
            "show synchronous_commit;"
            "show archive_dest;")
        self.log.info(sql_cmd)
        self.assertIn("dn_6002", sql_cmd, "执行失败" + text)
        self.assertNotIn("off\n", sql_cmd, "执行失败" + text)
        self.assertIn("on\n", sql_cmd, "执行失败" + text)

        self.log.info("备1设置开启归档")
        self.set_guc("archive_timeout", 60, "reload")
        self.set_guc("archive_mode", "on", "reload", self.s_com1, True)
        self.set_guc("archive_dest", f"'{self.path}'",
                     "reload", self.s_com1, True)

        sql_cmd = self.s_com1.execut_db_sql("show archive_mode;"
                                            "show archive_dest;"
                                            "show archive_timeout;")
        self.log.info(sql_cmd)
        self.assertNotIn("off\n", sql_cmd, "执行失败" + text)
        self.assertIn("on\n", sql_cmd, "执行失败" + text)
        self.assertIn("1min\n", sql_cmd, "执行失败" + text)
        self.assertIn(f"{self.path}\n", sql_cmd, "执行失败" + text)

        self.log.info("sleep 60 等待已有xlog完成归档")
        time.sleep(60)

        self.log.info("起线程切换日志期间立即重启数据库")
        self.log.info("--step4:查看主备归档")
        sql = f'''cd {self.path};ls -l|grep "^-"| wc -l'''
        for i in range(3):
            num_x1 = int(self.s_node1.sh(sql).result())
            self.log.info(num_x1)
            time.sleep(10)
            num_x2 = int(self.s_node1.sh(sql).result())
            self.log.info(num_x2)
            if num_x1 != num_x2:
                time.sleep(10)
            else:
                break

        self.log.info("测试前核对备1归档数量")
        num_x2 = int(self.s_node1.sh(sql).result())
        self.log.info(num_x2)

        self.log.info("--step4:起线程gs_om重启数据库;expect:成功")
        result = self.primary_sh.restart_db_cluster()
        self.log.info(result)
        self.assertTrue(result, "执行失败" + text)

        self.log.info("--step5:核对归档文件;expect:备1归档文件增加，备2为0")
        self.log.info("查看集群归档开启情况")
        sql_cmd = self.primary_sh.execut_db_sql("show archive_timeout;"
                                                "show archive_mode")
        self.log.info(sql_cmd)
        sql_cmd = self.s_com1.execut_db_sql("show archive_timeout;"
                                            "show archive_mode;"
                                            "show archive_dest")
        self.log.info(sql_cmd)
        sql_cmd = self.s_com2.execut_db_sql("show archive_timeout;"
                                            "show archive_mode")
        self.log.info(sql_cmd)
        self.log.info("sleep archive_timeout后继续增加")
        time.sleep(100)
        num_x3 = int(self.s_node1.sh(sql).result())
        self.log.info(num_x3)
        self.assertGreater(num_x3, num_x2, "执行失败" + text)
        time.sleep(100)
        num_x4 = int(self.s_node1.sh(sql).result())
        self.log.info(num_x4)
        self.assertGreater(num_x4, num_x3, "执行失败" + text)

        self.log.info("备2归档文件为0")
        num_x4 = int(self.s_node2.sh(sql).result())
        self.log.info(num_x4)
        self.assertEqual(0, num_x4, "执行失败" + text)

    def tearDown(self):
        text = "--step6:恢复默认值;expect:成功"
        self.log.info(text)
        for com in self.full_com_list:
            self.set_guc("archive_mode", "off", "reload", com)
            self.set_guc("archive_dest", "''", "reload", com)
            self.set_guc("log_min_messages", f"'{self.log_min_messages}'",
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
        self.log.info("==Opengauss_Function_Guc_WAL_Case0114 finish==")

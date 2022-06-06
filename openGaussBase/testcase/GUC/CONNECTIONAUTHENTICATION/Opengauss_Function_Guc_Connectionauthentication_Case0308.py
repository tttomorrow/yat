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
Case Type   : GUC参数--连接认证
Case Name   : alter system set修改参数max_connections小于等于max_wal_senders值
Description :
    1、查看max_wal_senders默认值
    2、设置max_connections参数为15并重启数据库
    3、设置max_connections参数为16并重启数据库
    4、恢复默认值
Expect      :
    1、max_wal_senders默认值为16
    2、重启数据库失败
    3、重启数据库失败
    4、恢复默认值成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GUC(unittest.TestCase):
    def setUp(self):
        LOGGER.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0308start-')
        self.constant = Constant()
        self.user_node = Node("PrimaryDbUser")

    def test_listen_addresses(self):
        LOGGER.info("步骤1：查询max_wal_senders值")
        sql_cmd = COMMONSH.execut_db_sql("show max_wal_senders;")
        LOGGER.info(sql_cmd)
        self.default_value = sql_cmd.split("\n")[-2].strip()
        LOGGER.info("步骤2:设置max_connections为15并重启数据库")
        sql_cmd = COMMONSH.execut_db_sql("alter system set "
                                         "max_connections to 15;")
        LOGGER.info(sql_cmd)
        sql_cmd = COMMONSH.restart_db_cluster()
        LOGGER.info(sql_cmd)
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertFalse("Normal" in status or "Degraded" in status)

    def tearDown(self):
        LOGGER.info("步骤3:恢复默认值")
        sql_cmd = COMMONSH.execute_gsguc("set",
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         "max_connections=5000")
        LOGGER.info(sql_cmd)
        self.assertTrue(sql_cmd)
        sql_cmd = COMMONSH.restart_db_cluster()
        LOGGER.info(sql_cmd)
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0308finish-')

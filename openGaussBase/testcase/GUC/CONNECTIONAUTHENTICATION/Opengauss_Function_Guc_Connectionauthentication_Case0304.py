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
Case Name   :gs_guc set修改参数listen_address为多个ip，ip间使用逗号分隔
Description :
    1、查看listen_addresses默认值
    2、设置listen_addresses参数为多个ip并重启数据库
    4、使用非套接字和套接字连接数据库
    5、恢复默认值
Expect      :
    1、listen_addresses默认值为监听本机TCP/IP地址
    2、修改listen_addresses参数为空成功
    3、设置并重启数据库成功
    4、使用套接字、非套接字连接数据库成功
    5、恢复默认值成功
History     :
"""
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GUC(unittest.TestCase):
    def setUp(self):
        LOGGER.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0304start-')
        self.constant = Constant()
        self.user_node = Node("PrimaryDbUser")

    def test_listen_addresses(self):
        LOGGER.info("步骤1:查询listen_addresses值")
        sql_cmd = COMMONSH.execut_db_sql("show listen_addresses;")
        LOGGER.info(sql_cmd)
        self.default_value = sql_cmd.split("\n")[-2].strip()
        LOGGER.info("步骤2:设置listen_addresses参数为多个ip")
        sql_cmd = COMMONSH.execute_gsguc("set",
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         "listen_addresses='127.0.0.1,::1'",
                                         node_name=f"{self.user_node}",
                                         single=True)
        LOGGER.info(sql_cmd)
        self.assertTrue(sql_cmd)
        sql_cmd = COMMONSH.restart_db_cluster()
        LOGGER.info(sql_cmd)
        status = COMMONSH.get_db_cluster_status()
        LOGGER.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info("步骤3:使用非套接字和套接字连接数据库")
        result = self.user_node.sh(f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d postgres \
            -p {self.user_node.db_port} \
            -h 127.0.0.1 \
            -U {self.user_node.ssh_user} \
            -W {self.user_node.ssh_password} \
            -c "show listen_addresses;"''').result()
        LOGGER.info(result)
        self.assertIn("127.0.0.1,::1", result)
        result = self.user_node.sh(f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d postgres \
            -p {self.user_node.db_port} \
            -U {self.user_node.ssh_user} \
            -W {self.user_node.ssh_password} \
            -c "show listen_addresses;"''').result()
        LOGGER.info(result)
        self.assertIn("127.0.0.1,::1", result)

    def tearDown(self):
        LOGGER.info("步骤4:恢复默认值")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"listen_addresses="
                                        f"'{self.default_value}'",
                                        node_name=f"{self.user_node}",
                                        single=True)
        LOGGER.info(result)
        result = COMMONSH.restart_db_cluster()
        LOGGER.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        LOGGER.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0304finish-')

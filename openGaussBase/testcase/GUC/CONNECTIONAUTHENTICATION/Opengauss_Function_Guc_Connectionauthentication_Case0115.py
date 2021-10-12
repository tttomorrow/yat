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
Case Name   : set修改参数unix_socket_permissions为0400
Description :
    1、查看unix_socket_permissions和listen_addresses默认值；
    show listen_addresses;
    show unix_socket_permissions;
    2、设置listen_addresses参数为*
    gs_guc set -D {dn1} -c "listen_addresses='*'"
    gs_om -t stop;gs_om -t start
    3、使用套接字和非套接字连接
    备注:不加-h则走套接字连接
    gsql -d postgres -p {port} -r -h 127.0.0.1
    -c "select 1;" -U {om} -W {passwd}
    gsql -d postgres -p {port} -r -c "select 1;"
    4、修改unix_socket_permissions为0400
    gs_guc set -N all  -D all -c "unix_socket_permissions='0400'"
    5、使用套接字连接成功，非套接字连接失败
    gsql -d postgres -p {port} -r -h 127.0.0.1
    -c "select 1;" -U {om} -W {passwd}
    gsql -d postgres -p {port} -r -c "select 1;"
    6、恢复默认值
    gs_guc set -N all -D all -c "unix_socket_permissions='0700'"
    gs_guc set -D {dn1} -c "listen_addresses='{主机ip}'"
Expect      :
    1、查看unix_socket_permissions默认值
    2、修改listen_addresses参数为* 成功
    3、使用套接字和非套接字连接成功
    4、修改unix_socket_permissions为0400 成功
    5、使用套接字连接成功，非套接字连接失败
    6、恢复默认值
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.primary_sh = CommonSH("PrimaryDbUser")
        self.casename = "Opengauss_Function_Guc_" \
                        "Connectionauthentication_Case0115"
        self.log.info(f"{self.casename} start")
        self.constant = Constant()
        self.dbuser = Node("dbuser")
        text = "重启核对数据库状态正常"
        self.log.info(text)
        self.primary_sh.restart_db_cluster()
        is_started = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started,
                        "执行失败" + text)
        self.user_node = Node("PrimaryDbUser")

    def test_guc(self):
        text = "--step1:查询unix_socket_permissions ;expect:默认值0700"
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql("show listen_addresses;")
        self.log.info(sql_cmd)
        self.default_value = sql_cmd.split("\n")[-2].strip()
        sql_cmd = self.primary_sh.execut_db_sql(
            "show unix_socket_permissions;")
        self.log.info(sql_cmd)
        self.assertEqual("0700", sql_cmd.split("\n")[-2].strip(),
                         "执行失败" + text)

        text = "--step2:设置listen_addresses参数为*;expect:成功"
        self.log.info(text)
        res = self.primary_sh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            "listen_addresses='*'",
                                            node_name=f"{self.user_node}",
                                            single=True)
        self.assertTrue(res, "执行失败" + text)
        result = self.primary_sh.restart_db_cluster()
        self.log.info(result)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败" + text)

        text = "--step3:使用套接字和非套接字连接;expect:成功"
        self.log.info(text)
        result = self.user_node.sh(f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d {self.dbuser.db_name} \
            -p {self.user_node.db_port} \
            -h 127.0.0.1 \
            -U {self.user_node.ssh_user} \
            -W {self.user_node.ssh_password} \
            -c "select 1"''').result()
        self.log.info(result)
        self.assertTrue("failed" not in result or "bash" not in result,
                        "执行失败" + text)
        self.assertIn("1\n", result, "执行失败" + text)
        result = self.user_node.sh(f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d {self.dbuser.db_name} \
            -p {self.user_node.db_port} \
            -U {self.user_node.ssh_user} \
            -W {self.user_node.ssh_password} \
            -c "select 1"''').result()
        self.log.info(result)
        self.assertTrue("failed" not in result or "bash" not in result,
                        "执行失败" + text)
        self.assertIn("1\n", result, "执行失败" + text)

        text = "--step4:修改unix_socket_permissions为0400等;" \
               "expect:修改失败，show参数为默认值"
        self.log.info(text)
        res = self.primary_sh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            "unix_socket_permissions='0400'")
        self.assertTrue(res, "执行失败" + text)
        result = self.primary_sh.restart_db_cluster()
        self.log.info(result)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败" + text)

        text = "--step5:再次连接;expect:使用套接字连接成功，非套接字连接失败"
        self.log.info(text)
        result = self.user_node.sh(f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d {self.dbuser.db_name} \
            -p {self.user_node.db_port} \
            -h 127.0.0.1 \
            -U {self.user_node.ssh_user} \
            -W {self.user_node.ssh_password} \
            -c "select 1"''').result()
        self.log.info(result)
        self.assertTrue("failed" not in result or "bash" not in result,
                        "执行失败" + text)
        self.assertIn("1\n", result, "执行失败" + text)
        result = self.user_node.sh(f'''source {macro.DB_ENV_PATH};\
            gsql \
            -d {self.dbuser.db_name} \
            -p {self.user_node.db_port} \
            -U {self.user_node.ssh_user} \
            -W {self.user_node.ssh_password} \
            -c "select 1"''').result()
        self.log.info(result)
        self.assertTrue("failed to connect Unknown" in result, "执行失败" + text)

    def tearDown(self):
        text = "--step6:恢复默认值;expect:成功"
        self.log.info(text)
        res = self.primary_sh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"unix_socket_permissions=0700")
        self.log.info(res)
        res = self.primary_sh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"listen_addresses="
                                            f"'{self.default_value}'",
                                            node_name=f"{self.user_node}",
                                            single=True)
        self.log.info(res)
        result = self.primary_sh.restart_db_cluster()
        self.log.info(result)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败" + text)
        self.log.info(f"{self.casename} finish")

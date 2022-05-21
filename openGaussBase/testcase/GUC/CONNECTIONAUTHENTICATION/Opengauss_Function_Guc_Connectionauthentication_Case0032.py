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
Case Type   : GUC
Case Name   : local_bind_address参数使用gs_guc set设置为非字符类型
Description : 1、查看local_bind_address默认值；
              source {env}
              show local_bind_address;
              2、使用设置gs_guc set设置local_bind_address为非字符类型
              gs_guc set -D {cluster/dn1} -c "listen_addresses=123456"
              3、恢复默认值
Expect      : 1、显示默认值；
              2、修改失败；
              3、恢复默认值成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

COMMONSH = CommonSH("PrimaryDbUser")


class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.name = "Opengauss_Function_Guc_Connectionauthentication_Case0032"
        self.log.info(f"=={self.name}.py start==")
        self.dbUserNode1 = Node(node="PrimaryDbUser")
        self.ipadd = self.dbUserNode1.db_host
        self.hostname = self.dbUserNode1.sh("cat /etc/hostname").result()

    def test_guc(self):
        self.log.info("步骤1：查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql("show local_bind_address;")
        self.log.info(sql_cmd)
        self.assertIn(self.ipadd, sql_cmd)

        self.log.info("步骤2：修改为123456 修改失败")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"local_bind_address=123456",
                                        self.hostname,
                                        single=True)
        self.assertFalse(result)

        self.log.info("步骤3：恢复为本机ip")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"local_bind_address='{self.ipadd}'",
                                        self.hostname,
                                        single=True)
        self.assertTrue(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show local_bind_address;")
        self.log.info(sql_cmd)
        if str(self.ipadd) != sql_cmd.splitlines()[-2].strip():
            result = COMMONSH.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"local_bind_address="
                                            f"'{self.ipadd}'",
                                            self.hostname,
                                            single=True)
            self.log.info(result)
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(f"=={self.name}.py finish==")

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
Case Name   : sysadmin_reserved_connections参数使用gs_guc set设置
Description : 1、查看sysadmin_reserved_connections默认值；
              source /opt/opengauss810/env
              gs_guc check -D /opt/opengauss810/cluster/dn1
              -c sysadmin_reserved_connections
              2、使用设置gs_guc set设置sysadmin_reserved_connections
              gs_guc set -D /opt/opengauss810/cluster/dn1
              -c "sysadmin_reserved_connections=11"
              3、校验是否修改成功；
              show max_wal_senders;
              4、恢复默认值
Expect      : 1、显示默认值；
              2、参数修改成功；
              3、查看参数修改成功；
              4、修改成功；
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.casename = "Opengauss_Function_Guc_" \
                        "Connectionauthentication_Case0066"
        self.log.info(f"{self.casename} start")
        self.rootNode = Node()
        self.dbuser = Node("dbuser")
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        self.dbUserNode = Node(node='PrimaryRoot')
        self.statusCmd = f'source {macro.DB_ENV_PATH};' \
                         f'gs_om -t status --detail'
        self.param = "sysadmin_reserved_connections"

    def test_startdb(self):
        text = "--step1:查看sysadmin_reserved_connections默认值，并校验;expect:成功"
        self.log.info(text)
        result = self.primary_sh.execute_gsguc('check', '3',
                                               f'{self.param}')
        self.assertTrue(result, "执行失败" + text)

        text = "--step2:设置sysadmin_reserved_connections，重启使其生效;expect:重启成功并生效"
        self.log.info(text)
        result = self.primary_sh.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'{self.param}=11')
        self.assertTrue(result, "执行失败" + text)

        text = "重启数据库"
        self.log.info(text)
        self.primary_sh.restart_db_cluster()
        is_started = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started,
                        "执行失败" + text)

        text = "--step3:校验参数是否修改成功;expect:修改成功"
        self.log.info(text)
        checksql = f"source {macro.DB_ENV_PATH};" \
                   f"gsql -d {self.dbuser.db_name} " \
                   f"-p {self.dbUserNode1.db_port} " \
                   f"-c 'show {self.param}';"
        self.log.info(checksql)
        checkresult = self.dbUserNode1.sh(checksql).result()
        self.assertIn('11', checkresult, "执行失败" + text)

    def tearDown(self):
        text = "--step4:恢复默认值;expect:成功"
        self.log.info(text)
        re = self.primary_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f'{self.param}=3')
        self.primary_sh.restart_db_cluster()
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue(re)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        "执行失败" + text)
        self.log.info(f"{self.casename} finish")

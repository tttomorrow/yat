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
Case Name   : port参数使用gs_guc reload设置
Description : 1、查看port默认值，并校验；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c port
              2、使用设置gs_guc reload设置为port为系统未使用端口,
              可使用lsof -i:55810命令校验端口使用情况。
              lsof -i:55810
              gs_guc reload -D {cluster/dn1} -c "port=55810"
              3、重启数据库使其生效；
              gs_om -t stop && gs_om -t start
              4、使用新端口链接数据库，校验预期功能；
              gsql -d postgres -p 55810
              5、恢复默认值
              gs_guc set -D {cluster/dn1} -c "port=12306"
Expect      : 1、显示默认值为安装数据库时指定端口；
              2、参数修改成功；
              3、数据库重启成共；
              4、使用新端口连接成功，预期结果正常；
              5、恢复默认值成功，恢复为数据库安装时指定端口；
History     :
"""
import random
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
                        "Connectionauthentication_Case0002"
        self.log.info(f"{self.casename} start")
        self.rootNode = Node()
        self.dbuser = Node("dbuser")
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        self.dbUserNode = Node(node='PrimaryRoot')
        self.statusCmd = f'source {macro.DB_ENV_PATH};' \
                         f'gs_om -t status --detail'

    def test_startdb(self):
        text = "--step1:查看port默认值;expect:数据库端口"
        self.log.info(text)
        result = self.primary_sh.execut_db_sql('show port;')
        self.log.info(result)
        self.assertIn(str(self.dbUserNode1.db_port), result, "执行失败" + text)

        text = "--step2:设置随机端口号，并使用设置gs_guc reload设置;expect:成功"
        self.log.info(text)
        port = 0
        for i in range(1000):
            port = random.randint(10000, 65535)
            check_cmd = f'lsof -i:{str(port)}'
            check_result = self.dbUserNode1.sh(check_cmd).result()
            if str(port) not in check_result:
                break
        guc_cmd = f"source {macro.DB_ENV_PATH};gs_guc reload " \
                  f"-D {macro.DB_INSTANCE_PATH} -c 'port=\'{str(port)}\''"
        self.log.info(guc_cmd)
        guc_result = self.dbUserNode1.sh(guc_cmd).result()
        self.log.info(guc_result)

        text = "--step3:重启数据库使其生效;expect:成功"
        self.log.info(text)
        self.primary_sh.restart_db_cluster()
        is_started = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started,
                        "执行失败" + text)

        text = "--step4:验证预期结果(因调用新端口，故不能调用公共函数);expect:成功"
        self.log.info(text)
        check_sql = f"source {macro.DB_ENV_PATH};" \
                    f"gsql -d {self.dbuser.db_name} " \
                    f"-p {str(port)} -c 'show port';"
        self.log.info(check_sql)
        check_result = self.dbUserNode1.sh(check_sql).result()
        self.assertIn(str(port), check_result, "执行失败" + text)

        text = "--step5:使用旧端口连接数据库;expect:报错"
        self.log.info(text)
        log_in = f"source {macro.DB_ENV_PATH};" \
                 f"gsql " \
                 f"-d {self.dbuser.db_name} " \
                 f"-p {self.dbUserNode1.db_port} " \
                 f"-U {self.dbUserNode1.ssh_user} " \
                 f"-W {self.dbUserNode1.ssh_password} " \
                 f"-c 'show port';"
        self.log.info(log_in)
        check_result = self.dbUserNode1.sh(log_in).result()
        self.log.info(check_result)
        self.assertIn('failed to connect', check_result, "执行失败" + text)

    def tearDown(self):
        text = "--step6:恢复默认值;expect:成功"
        self.log.info(text)
        res = self.primary_sh.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"port="
                                            f"{self.dbUserNode1.db_port}")
        self.primary_sh.restart_db_cluster()
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue(res)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        "执行失败" + text)
        self.log.info(f"{self.casename} finish")

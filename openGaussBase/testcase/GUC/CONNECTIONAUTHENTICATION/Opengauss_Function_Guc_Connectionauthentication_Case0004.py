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
Case Name   : 使用alter system set修改参数port，观察预期结果；
Description : 1、查看port默认值；
              source {macro.DB_ENV_PATH}
              show  port;
              2、使用alter system set修改数据库参数port;
              3、重启数据库使其生效；
              gs_om -t stop && gs_om -t start
              4、使用新端口连接数据库，校验预期功能；
              5、使用旧端口连接数据库
              6、恢复默认值
Expect      : 1、显示默认值为安装数据库时指定端口；
              2、参数修改成功；
              3、数据库重启成功；
              4、使用新端口连接成功，预期结果正常；
              5、使用旧端口连接数据库失败
              6、恢复默认值成功，恢复为数据库安装时指定端口；
History     :
             优化assert及步骤
"""

import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info(f'-----{os.path.basename(__file__)} start -----')
        self.dbUserNode1 = Node(node='PrimaryDbUser')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.default_value = self.common.show_param('port')

    def test_startdb(self):
        text = '----step1:查询系统未使用端口;expect:成功----'
        self.log.info(text)
        port = self.common.get_not_used_port(self.dbUserNode1)
        self.log.info(port)
        self.assertNotEqual(0, port, '执行失败:' + text)

        text = '--step2:使用alter system set设置port;expect:成功--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f"alter system set port to "
                                                f"{str(port)};")
        self.log.info(sql_cmd)
        self.assertIn("ALTER SYSTEM SET", sql_cmd, "执行失败" + text)

        text = '--step3:重启数据库使其生效;expect:成功--'
        self.log.info(text)
        self.primary_sh.restart_db_cluster()
        is_started = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in is_started or "Normal" in is_started,
                        "执行失败" + text)

        text = '--step4:验证预期结果(因调用新端口，故不能调用公共函数);' \
               'expect:成功--'
        self.log.info(text)
        check_sql = f"source {macro.DB_ENV_PATH};" \
                    f"gsql " \
                    f"-d {self.dbUserNode1.db_name} " \
                    f"-p {str(port)} " \
                    f"-c 'show port';"
        self.log.info(check_sql)
        check_result = self.dbUserNode1.sh(check_sql).result()
        self.log.info(check_result)
        self.assertIn(str(port), check_result, "执行失败" + text)

        text = '--step5:使用旧端口连接数据库;expect:报错--'
        self.log.info(text)
        log_in = f"source {macro.DB_ENV_PATH};" \
                 f"gsql " \
                 f"-d {self.dbUserNode1.db_name} " \
                 f"-p {self.dbUserNode1.db_port} " \
                 f"-U {self.dbUserNode1.ssh_user} " \
                 f"-W {self.dbUserNode1.ssh_password} " \
                 f"-c 'show port';"
        self.log.info(log_in)
        check_result = self.dbUserNode1.sh(log_in).result()
        self.log.info(check_result)
        self.assertIn('failed to connect', check_result, "执行失败" + text)

    def tearDown(self):
        text = '--step6:恢复默认值;expect:成功--'
        self.log.info(text)
        res = self.primary_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"port="
                                            f"{self.default_value}")
        self.primary_sh.restart_db_cluster()
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue(res)
        self.log.info('--测试数据库已恢复连接--')
        sql_cmd = self.primary_sh.execut_db_sql(f"select 1;")
        self.log.info(sql_cmd)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        "执行失败" + text)
        self.assertEqual('1', sql_cmd.splitlines()[2].strip(),
                         "执行失败" + text)
        self.log.info(f'-----{os.path.basename(__file__)} end -----')

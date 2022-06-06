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
Case Type   : 系统内部使用工具
Case Name   : 使用gs_probackup add-instance命令同时指定--remote-proto=ssh 、
              --remote-host=<ip>、--remote-port=<port>、
              --remote-user=<其他user>、--remote-path，合理报错
Description :
    1.创建备份目录
    2.进行初始化
    3.创建测试用户
    4.在备份路径内初始化一个新的备份实例
    5.清理环境
Expect      :
    1.创建成功
    2.初始化成功
    3.创建用户成功
    4.初始化失败，权限拒绝
    5.清理环境完成
             及teardown中增加断言
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Pri_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Pri_SH.get_node_num(), '单机环境不执行')
class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Standby1_User_Node = Node('Standby1DbUser')

        self.log = Logger()
        self.constant = Constant()
        self.re_path = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                    'app', 'bin')
        self.re_lib = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                   'app', 'lib')
        self.gs_probackup_path = os.path.join(macro.DB_INSTANCE_PATH,
                                              'gs_probackup_testdir0144')
        self.us_name = "us_gs_probackup_case0144"
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0144 start----')

    def test_server_tools(self):
        text = '--step1:创建备份目录;expect:创建成功----'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.gs_probackup_path}" ]
                        then
                            mkdir -p {self.gs_probackup_path}
                        fi'''
        primary_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.log.info(primary_result)
        self.assertEqual(primary_result, '', '执行失败:' + text)

        text = '--step2:进行初始化;expect:初始化成功---'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_path};"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg, '执行失败:' + text)

        text = '--step3:创建测试用户;expect:创建用户成功---'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(f"drop user if exists "
                                       f"{self.us_name};create user "
                                       f"{self.us_name} password "
                                       f"'{macro.COMMON_PASSWD}';")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '--step4:在备份路径内初始化一个新的备份实例;expect:合理报错--'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance " \
                   f"-B {self.gs_probackup_path} " \
                   f"-D {macro.DB_INSTANCE_PATH} " \
                   f"--instance=test_0144 " \
                   f"--remote-user={self.us_name} " \
                   f"--remote-host={self.Standby1_User_Node.db_host} " \
                   f"--remote-port=22 " \
                   f"--remote-proto=ssh " \
                   f"--remote-path={self.re_path} " \
                   f"--remote-lib={self.re_lib};"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn('Permission denied', init_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.gs_probackup_path}'
        self.log.info(clear_cmd)
        clear_msg = self.Primary_User_Node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        sql_cmd = Pri_SH.execut_db_sql(f"drop user if exists {self.us_name} "
                                       f"cascade;")
        self.log.info(sql_cmd)
        self.log.info('断言teardown成功')
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0144 end----')

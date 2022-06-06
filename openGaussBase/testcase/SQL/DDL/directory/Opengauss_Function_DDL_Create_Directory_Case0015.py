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
Case Type   : DDL_Create_Directory
Case Name   : enable_access_server_directory参数的alter system set设置方式
Description :
    1.使用alter system set修改参数
    2.使用alter system set恢复默认值
Expect      :
    1.设置成功
    2.恢复成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class CreateDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()

    def test_create_directory(self):
        text = "-----step3:使用alter system set修改参数，expect:设置成功-----"
        self.logger.info(text)
        alter_cmd = f"alter system set enable_access_server_directory to on;" \
            f"select pg_sleep(20);" \
            f"show enable_access_server_directory;"
        alter_msg = self.sh_primary.execut_db_sql(alter_cmd)
        self.logger.info(alter_msg)
        self.assertIn(self.constant.alter_system_success_msg,
                      alter_msg.splitlines()[0], '执行失败' + text)
        self.assertIn('on', alter_msg.splitlines()[-2].strip(),
                      '执行失败' + text)

        text = "-----step2:使用alter system set恢复默认值，expect:恢复成功-----"
        self.logger.info(text)
        alter_cmd = f"alter system set enable_access_server_directory to off;" \
            f"select pg_sleep(20);" \
            f"show enable_access_server_directory;"
        alter_msg = self.sh_primary.execut_db_sql(alter_cmd)
        self.logger.info(alter_msg)
        self.assertIn(self.constant.alter_system_success_msg,
                      alter_msg.splitlines()[0], '执行失败' + text)
        self.assertIn('off', alter_msg.splitlines()[-2].strip(),
                      '执行失败' + text)

    def tearDown(self):
        self.logger.info("-----无需清理环境-----")
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
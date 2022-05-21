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
Case Type   : 服务端工具
Case Name   : 用户检查CPU使用率，本地执行，参数-o将检查结果输出到指定文件夹
Description :
    1.查看主机名
    2.创建存放检查结果文件夹
    3.用户检查CPU使用率，将检查结果输出到指定文件夹
    4.判断检查结果是否生成
    5.清理环境
Expect      :
    1.查看主机名成功
    2.创建存放检查结果文件夹成功
    3.用户检查CPU使用率，将检查结果输出到指定文件夹成功
    4.判断检查结果生成成功
    5.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0309start--')
        self.primary_dbuser = Node('PrimaryDbUser')
        self.primary_root = Node('PrimaryRoot')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('-----步骤1.查看主机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname)

        self.log.info('------步骤2.创建存放检查结果文件夹------')
        mkdir_cmd = f'mkdir /home/test_check/ ;' \
            f'chmod -R 777 /home/test_check/;' \
            f'ls /home'
        self.log.info(mkdir_cmd)
        mkdir_msg = self.primary_root.sh(mkdir_cmd).result()
        self.log.info(mkdir_msg)
        self.assertIn('test_check', mkdir_msg)

        self.log.info('---步骤3.用户检查CPU使用率，将检查结果输出到指定文件夹---')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_check -i CheckCPU  -o /home/test_check/;'
        self.log.info(check_cmd)
        check_msg = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertTrue(self.constant.GS_CHECK_SUCCESS_MSG2[0]
                        in check_msg or self.constant.GS_CHECK_SUCCESS_MSG2[1]
                        in check_msg and self.constant.GS_CHECK_SUCCESS_MSG2[2]
                        in check_msg)

        self.log.info('-------步骤4.判断检查结果是否生成-------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cd /home/test_check/;' \
            f'tar -zxvf CheckReport*.tar.gz;' \
            f'cat CheckResult*'
        self.log.info(check_cmd)
        check_msg = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertIn(f'gs_check_{hostname}.log', check_msg)
        self.assertIn(f'All check items run completed', check_msg)

        self.log.info('-----检查数据库状态，是否有备机，若有，继续断言-----')
        status = self.commonsh.get_db_cluster_status('detail')
        self.assertTrue("Degraded" in status or "Normal" in status)
        if 'Standby' not in status:
            self.log.info('--单机环境，后续不执行，直接通过--')
        else:
            self.standby_node = Node('Standby1Root')
            self.assertIn(f'gs_check_{self.standby_node.db_host}.log',
                          check_msg)

    def tearDown(self):
        self.log.info("------------------步骤5.清理环境------------------")
        rm_cmd = f'rm -rf /home/test_check/'
        self.log.info(rm_cmd)
        rm_msg = self.primary_root.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0309finish--')

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
Case Name   : 修改单个检查项参数，以CheckFilehandle为例
Description :
     1.修改单个检查项参数，以CheckFilehandle为例
     2.检查修改后的单个检查项
     3.恢复参数值
Expect      :
     1.修改单个检查项参数成功
     2.检查修改后的单个检查项
     3.恢复参数值成功
History     :
"""

import os
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_check_Case0392_开始---')
        self.dbuser_node = Node('dbuser')
        self.root_node = Node('default')
        self.clear_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'gspylib', 'inspection', 'output', 'CheckReport*')
        self.items_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'gspylib', 'inspection', 'config', 'items.xml')
        self.Constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        text = '---step1.修改单个检查项参数,以CheckFilehandle为例;expect:修改成功---'
        self.log.info(text)
        sed_cmd1 = f"sed -i 's/Threshold_Warning=800000/"  \
            f"Threshold_Warning=500000/g' " \
            f"{self.items_path};" \
            f"sed -i 's/进程数是否超过80万/进程数是否超过50万/g' "  \
            f" {self.items_path};"
        self.log.info(sed_cmd1)
        sed_msg1 = self.dbuser_node.sh(sed_cmd1).result()
        self.log.info(sed_msg1)
        self.log.info('---------------检查是否修改成功---------------')
        cat_cmd1 = f'cat {self.items_path};'
        cat_msg1 = self.dbuser_node.sh(cat_cmd1).result()
        self.log.info(cat_msg1)
        self.assertIn('Threshold_Warning=500000', cat_msg1, '执行失败' + text)
        self.assertIn('进程数是否超过50万', cat_msg1, '执行失败' + text)

        text = '-------step2:检查修改后的单个检查项;expect:检查成功--------'
        self.log.info(text)
        check_cmd = f'''su - {self.dbuser_node.ssh_user} -c "
                   source {macro.DB_ENV_PATH};
                   expect -c \\\"set timeout -1
                   spawn gs_check -i CheckFilehandle
                   expect *]:
                   send {self.root_node.ssh_user}\\n
                   expect *]:
                   send {self.root_node.ssh_password}\\n
                   expect eof\\\""'''
        self.log.info(check_cmd)
        shell_res = os.popen(check_cmd)
        str_res = ''.join(shell_res.readlines())
        self.log.info(str_res)
        flag = (self.Constant.GS_CHECK_SUCCESS_MSG2[0] in str_res or
                self.Constant.GS_CHECK_SUCCESS_MSG2[1] in str_res) and \
               self.Constant.GS_CHECK_SUCCESS_MSG2[2] in str_res
        self.assertTrue(flag, '执行失败:' + text)

        text = '---------step3:恢复参数值;expect:恢复成功-----------'
        self.log.info(text)
        sed_cmd2 = f"sed -i 's/Threshold_Warning=500000/" \
            f"Threshold_Warning=800000/g' " \
            f"{self.items_path};" \
            f"sed -i 's/进程数是否超过50万/进程数是否超过80万/g' " \
            f"{self.items_path};"
        self.log.info(sed_cmd2)
        sed_msg2 = self.dbuser_node.sh(sed_cmd2).result()
        self.log.info(sed_msg2)
        self.log.info('---------------检查是否修改成功---------------')
        cat_cmd2 = f'cat {self.items_path};'
        cat_msg2 = self.dbuser_node.sh(cat_cmd2).result()
        self.log.info(cat_msg2)
        self.assertIn('Threshold_Warning=800000', cat_msg2, '执行失败' + text)
        self.assertIn('进程数是否超过80万', cat_msg2, '执行失败' + text)

    def tearDown(self):
        text = '----------清理环境----------'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.clear_path};'
        self.log.info(clear_cmd)
        clear_msg = self.root_node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status,
                        '执行失败:' + text)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0392_结束--')

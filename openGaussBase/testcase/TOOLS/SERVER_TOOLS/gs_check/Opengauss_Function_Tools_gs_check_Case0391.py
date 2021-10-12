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
Case Type   : 服务端工具
Case Name   : 修改单个检查项参数，以CheckCPU为例
Description :
     1.修改单个检查项参数，以CheckCPU为例
     2.检查修改后的单个检查项
     3.恢复参数值
Expect      :
     1.修改单个检查项参数成功
     2.检查修改后的单个检查项
     3.恢复参数值成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_check_Case0391start---')
        self.dbusernode = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        self.log.info('---步骤1：修改单个检查项参数，以CheckCPU为例---')
        sed_cmd1 = f"sed -i 's/StandardCPUIdle=30/StandardCPUIdle=10/g' " \
            f"{macro.DB_INSTANCE_PATH}/../tool/script/gspylib/inspection/" \
            f"config/items.xml;" \
            f"sed -i 's/StandardWIO=30/StandardWIO=10/g' " \
            f"{macro.DB_INSTANCE_PATH}/../tool/script/gspylib/inspection" \
            f"/config/items.xml;" \
            f"sed -i 's/如果idle 大于30%,或者 iowait 小于 30%/如果idle " \
            f"大于10%,或者 iowait 小于 10%/g' {macro.DB_INSTANCE_PATH}" \
            f"/../tool/script/gspylib/inspection/config/items.xml;"
        self.log.info(sed_cmd1)
        sed_msg1 = self.dbusernode.sh(sed_cmd1).result()
        self.log.info(sed_msg1)
        self.log.info('---------------检查是否修改成功---------------')
        cat_cmd1 = f'cat {macro.DB_INSTANCE_PATH}/../tool/script/gspylib/' \
            f'inspection/config/items.xml;'
        cat_msg1 = self.dbusernode.sh(cat_cmd1).result()
        self.log.info(cat_msg1)
        self.assertIn('StandardCPUIdle=10', cat_msg1)
        self.assertIn('StandardWIO=10', cat_msg1)
        self.assertIn('如果idle 大于10%,或者 iowait 小于 10%', cat_msg1)
        self.log.info('----------步骤2：检查修改后的单个检查项----------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_check -i CheckCPU;'
        self.log.info(check_cmd)
        check_msg = self.dbusernode.sh(check_cmd).result()
        self.log.info(check_msg)
        flag = (self.constant.GS_CHECK_SUCCESS_MSG2[0] in check_msg or
                self.constant.GS_CHECK_SUCCESS_MSG2[1] in check_msg) and \
                self.constant.GS_CHECK_SUCCESS_MSG2[2] in check_msg
        self.assertTrue(flag)
        self.log.info('---------------步骤3：恢复参数值成功---------------')
        sed_cmd2 = f"sed -i 's/StandardCPUIdle=10/StandardCPUIdle=30/g' " \
            f"{macro.DB_INSTANCE_PATH}/../tool/script/gspylib/inspection/" \
            f"config/items.xml;" \
            f"sed -i 's/StandardWIO=10/StandardWIO=30/g' " \
            f"{macro.DB_INSTANCE_PATH}/../tool/script/gspylib/inspection" \
            f"/config/items.xml;" \
            f"sed -i 's/如果idle 大于10%,或者 iowait 小于 10%/如果idle " \
            f"大于30%,或者 iowait 小于 30%/g' {macro.DB_INSTANCE_PATH}" \
            f"/../tool/script/gspylib/inspection/config/items.xml;"
        self.log.info(sed_cmd2)
        sed_msg2 = self.dbusernode.sh(sed_cmd2).result()
        self.log.info(sed_msg2)
        self.log.info('---------------检查是否修改成功---------------')
        cat_cmd2 = f'cat {macro.DB_INSTANCE_PATH}/../tool/script/gspylib/' \
            f'inspection/config/items.xml;'
        cat_msg2 = self.dbusernode.sh(cat_cmd2).result()
        self.log.info(cat_msg2)
        self.assertIn('StandardCPUIdle=30', cat_msg2)
        self.assertIn('StandardWIO=30', cat_msg2)
        self.assertIn('如果idle 大于30%,或者 iowait 小于 30%', cat_msg2)

    def tearDown(self):
        self.log.info('------清理环境-------')
        clear_cmd1 = f'rm -rf {macro.DB_INSTANCE_PATH}/../tool/script/' \
            f'gspylib/inspection/output/CheckReport*;'
        self.log.info(clear_cmd1)
        clear_msg1 = self.dbusernode.sh(clear_cmd1).result()
        self.log.info(clear_msg1)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0391finish--')

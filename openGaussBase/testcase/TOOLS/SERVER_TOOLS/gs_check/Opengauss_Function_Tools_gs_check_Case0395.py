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
Case Name   : 自定义场景safe的xml文件，但场景检查名称为scene_safe，检查失败
Description :
     1.自定义场景safe的xml文件，但场景检查名称为scene_safe，检查失败
     2.检查自定义场景 scene_safe
     3.删除自定义文件
Expect      :
     1.修改单个检查项参数成功
     2.检查自定义场景失败
     3.删除自定义文件成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_check_Case0394start---')
        self.dbusernode = Node('dbuser')
        self.rootnode = Node('default')

    def test_server_tools1(self):
        self.log.info('---步骤1：自定义场景的xml文件编写有误---')
        self.scene_path = f'{macro.DB_INSTANCE_PATH}/../tool/' \
            f'script/gspylib/inspection/config'
        sed_cmd1 = f''' echo '<?xml version="1.0" encoding="utf-8" ?>
            <scene name="safe" desc="check cluster parameters before safe.">
            <configuration/>
            <allowitems>
            <item name="CheckRouting"/>
            <item name="CheckPing"/>
            <item name="CheckEncoding"/>
            </allowitems>
            </scene>' > {self.scene_path}/scene_safe.xml;'''
        self.log.info(sed_cmd1)
        sed_msg1 = self.dbusernode.sh(sed_cmd1).result()
        self.log.info(sed_msg1)
        self.log.info('---------------检查是否修改成功---------------')
        ls_cmd1 = f'ls {macro.DB_INSTANCE_PATH}/../tool/script/gspylib/' \
            f'inspection/config;'
        ls_msg1 = self.dbusernode.sh(ls_cmd1).result()
        self.log.info(ls_msg1)
        self.assertIn('scene_safe.xml', ls_msg1)

        self.log.info('----------步骤2：检查自定义场景 scene_safe----------')
        result_msg = f'The scene scene_safe and its configuaration file ' \
            f'scene_scene_safe.xml were not found in config folder.'
        check_cmd = f'''source {macro.DB_ENV_PATH};
            gs_check -e scene_safe;
            '''
        self.log.info(check_cmd)
        check_msg = self.dbusernode.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertIn(f'{result_msg}', check_msg)

    def tearDown(self):
        self.log.info('------清理环境-------')
        self.log.info('-------------步骤3：删除自定义文件成功-------------')
        rm_cmd1 = f'rm -rf {self.scene_path}/scene_safe.xml;'
        self.log.info(rm_cmd1)
        rm_msg1 = self.dbusernode.sh(rm_cmd1).result()
        self.log.info(rm_msg1)
        clear_cmd1 = f'rm -rf {macro.DB_INSTANCE_PATH}/../tool/script/' \
            f'gspylib/inspection/output/CheckReport*;'
        self.log.info(clear_cmd1)
        clear_msg1 = self.dbusernode.sh(clear_cmd1).result()
        self.log.info(clear_msg1)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0395inish--')

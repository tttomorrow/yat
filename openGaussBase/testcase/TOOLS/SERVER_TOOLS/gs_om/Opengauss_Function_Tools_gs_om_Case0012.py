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
Case Name   : 生成静态配置文件
Description :
    1.查询数据库详细状态信息
    2.进行生成静态配置文件的操作
    3.查看生成的静态配置文件
    4.清理环境
Expect      :
    1.查询数据库状态正常
    2.生成静态配置文件
    3.静态配置文件存在
    4.清理成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Tools_gs_om_Case0012_开始----')
        self.dbuser = Node('dbuser')
        self.root = Node('default')
        self.constant = Constant()
        self.static_file_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'static_config_files')

    def test_tools_om(self):
        text = '-----step1.查询数据库详细状态信息;except:查询数据库状态正常-----'
        self.log.info(text)
        query_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t query; '
        self.log.info(query_cmd)
        query_msg = self.dbuser.sh(query_cmd).result()
        self.log.info(query_msg)
        self.assertTrue("Degraded" in query_msg or "Normal" in query_msg,
                        '执行失败' + text)

        text = '-----step2:生成静态配置文件;except:生成静态配置文件------'
        self.log.info(text)
        generateconf_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om' \
            f' -t generateconf' \
            f' -X {macro.DB_XML_PATH}' \
            f' --distribute;'
        self.log.info(generateconf_cmd)
        generateconf_msg = self.dbuser.sh(generateconf_cmd).result()
        self.log.info(generateconf_msg)
        self.assertIn('static_config_files', generateconf_msg, '执行失败' + text)

        text = '-----step3:检查生成的静态配置文件;expect:静态配置文件存在------'
        self.log.info(text)
        check_cmd = f'source {macro.DB_ENV_PATH};ls {self.static_file_path};'
        self.log.info(check_cmd)
        check_msg = self.dbuser.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertIn('cluster_static_config', check_msg, '执行失败' + text)

    def tearDown(self):
        text = '------step5:step4:清理环境;except:清理成功-----'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.static_file_path};'
        self.log.info(clear_cmd)
        clear_msg = self.root.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.log.info('--Opengauss_Function_Tools_gs_om_Case0012_结束--')

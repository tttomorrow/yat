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
Case Name   : 生成静态配置文件的同时生成日志文件
Description :
    1.查询数据库详细状态信息
    2.进行生成静态配置文件和日志的操作
    3.查看是否生成日志文件
    4.查看是否生成静态文件
    5.清理环境
Expect      :
    1.数据库状态正常
    2.生成静态配置文件和日志文件成功
    3.查看日志文件存在
    4.查看静态配置文件存在
    5.清理环境完成
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
        self.log.info('--Opengauss_Function_Tools_gs_om_Case0082_开始--')
        self.dbuser_node = Node('dbuser')
        self.root_node = Node('default')
        self.constant = Constant()
        self.static_file_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tool', 'script',
            'static_config_files')
        self.log_path = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                     'omlog')

    def test_tools_om(self):
        text = '-----step1.查询数据库详细状态信息;except:查询数据库状态正常-----'
        self.log.info(text)
        query_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t query; '
        self.log.info(query_cmd)
        query_msg = self.dbuser_node.sh(query_cmd).result()
        self.log.info(query_msg)
        self.assertTrue("Degraded" in query_msg or "Normal" in query_msg,
                        '执行失败' + text)

        text = '-----step2:执行生成静态配置文件和日志文件的操作;except:生成静态配置文件和日志文件------'
        self.log.info(text)
        generateconf_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om' \
            f' -t generateconf' \
            f' -X {macro.DB_XML_PATH}' \
            f' --distribute' \
            f' -l {self.log_path}/om.log;'
        self.log.info(generateconf_cmd)
        generateconf_msg = self.dbuser_node.sh(generateconf_cmd).result()
        self.log.info(generateconf_msg)
        self.assertIn('static_config_files', generateconf_msg, '执行失败' + text)

        text = '------step3:检查是否生成日志文件;except:查看日志文件存在-----'
        self.log.info(text)
        find_cmd = f'find {self.log_path} -name \'*.log\' -mmin -1;'
        self.log.info(find_cmd)
        find_msg = self.dbuser_node.sh(find_cmd).result()
        self.log.info(find_msg)
        self.assertIn('.log', find_msg, '执行失败' + text)

        text = '------step4:检查是否生成静态配置文件;expect:查看静态配置文件存在-----'
        self.log.info(text)
        ls_cmd = f'ls {self.static_file_path};'
        self.log.info(ls_cmd)
        ls_msg = self.dbuser_node.sh(ls_cmd).result()
        self.log.info(ls_msg)
        self.assertIn('cluster_static_config', ls_msg, '执行失败' + text)

    def tearDown(self):
        text = '------step5:清理环境;expect:清理环境成功-----'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.static_file_path};' \
            f'rm -rf {self.log_path};'
        self.log.info(clear_cmd)
        clear_msg = self.root_node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.log.info('--Opengauss_Function_Tools_gs_om_Case0082_结束--')

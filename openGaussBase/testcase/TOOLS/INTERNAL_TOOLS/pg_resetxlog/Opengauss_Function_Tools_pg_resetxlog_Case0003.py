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
Case Type   : tools
Case Name   : 指定不正确的数据库实例目录执行pg_resetxlog命令
Description :
    1.关闭数据库
    2.在对应目录下查看原有xlog列表
    3.指定不正确的数据库实例目录执行pg_resetxlog命令
    4.查看执行结果，是否有提示信息
    5.在对应目录下查看现有xlog列表，是否重置成功
Expect      :
    1.检查数据库状态成功
    2.在对应目录下查看xlog列表成功
    3.执行pg_resetxlog命令失败
    4.命令执行失败的提示信息为：could not change directory
    5.对应目录下查看xlog列表成功，日志重置失败
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf('Standby' not in Primary_SH.get_db_cluster_status('detail'),
                 '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.userNode = Node(node='PrimaryDbUser')
    
    def test_systools(self):
        text = '----step1:关闭数据库;expect:成功----'
        self.logger.info(text)
        Primary_SH.stop_db_cluster()
        text = '---step2:在对应目录下查看原有xlog列表;expect:成功---'
        self.logger.info(text)
        xlog_path = os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')
        excute_cmd1 = f'ls -t {xlog_path} | head -1'
        msg2 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg2)
        self.assertIn('000', msg2, text + '执行失败')
        
        text = '--step3-4:指定不正确的实例目录执行pg_resetxlog命令;expect:失败--'
        self.logger.info(text)
        error_path = os.path.join(macro.DB_INSTANCE_PATH, '..', 'dn5')
        excute_cmd3 = f'source {macro.DB_ENV_PATH};' \
            f'pg_resetxlog {error_path};'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertIn('pg_resetxlog: could not change directory to', msg3,
                      text + '执行失败')
        
        text = '----step5:在对应目录下查看现有xlog列表是否重置成功;expect:失败----'
        self.logger.info(text)
        excute_cmd5 = f'ls -t {xlog_path} | head -1'
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.assertEquals(msg5, msg2, text + '执行失败')
    
    def tearDown(self):
        text = '----恢复环境----'
        self.logger.info(text)
        start_msg = Primary_SH.start_db_instance(mode="primary")
        self.logger.info(start_msg)
        build_msg_list = Primary_SH.get_standby_and_build()
        self.logger.info(build_msg_list)
        rev_msg = Primary_SH.get_db_cluster_status(param='status')
        self.logger.info(rev_msg)
        self.assertTrue(rev_msg, text + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

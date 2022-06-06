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
Case Name   : set 方式设置认证参数：HOSTTYPE DATABASE USERNAME IPADDR-WITH-IPMASK
Description :
    1.设置认证参数
    2.重启数据库
    3.查看是否设置成功
    4.删除已经设置的客户端认证策略
    5.重启数据库
Expect      :
    1.设置完成
    2.重启成功
    3.设置成功
    4.删除成功
    5.重启成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Tools_gs_guc_Case0027开始执行--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools(self):
        text = "--step1:设置认证参数;expect:执行成功--"
        self.log.info(text)
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc set -N all -I all -h "hostssl  all all 127.0.0.1/32  sha256";
                        '''
        self.log.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        self.log.info(msg)
        self.assertIn('Success to perform gs_guc!', msg, '执行失败:' + text)

        text = "--step2:重启数据库;expect:重启成功--"
        self.log.info(text)
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status,
                        '执行失败:' + text)

        text = "--step3:查看是否设置成功;expect:设置成功--"
        self.log.info(text)
        check_cmd = f'''source {macro.DB_ENV_PATH};
        cat {macro.DB_INSTANCE_PATH}/pg_hba.conf | grep 'hostssl'| grep \ 
        '127.0.0.1/32  sha256';'''
        self.log.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        self.log.info(msg)
        self.assertIn('hostssl  all all 127.0.0.1/32  sha256', msg,
                      '执行失败:' + text)

    def tearDown(self):
        text = "--step4:注释已经设置的客户端认证策略;expect:注释成功--"
        self.log.info(text)
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc reload -N all -I all -h "hostssl  all all 127.0.0.1/32";'''
        self.log.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        self.log.info(msg)
        self.assertIn('Success to perform gs_guc!', msg, '执行失败:' + text)

        text = "--step5:重启数据库;expect:重启成功--"
        self.log.info(text)
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status,
                        '执行失败:' + text)
        self.log.info('--Opengauss_Function_Tools_gs_guc_Case0027执行结束--')

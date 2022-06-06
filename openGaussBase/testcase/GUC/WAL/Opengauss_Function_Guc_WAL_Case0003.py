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
Case Type   : guc参数
Case Name   : 分别修改参数wal_level为minimal、archive、hot_standby，并校验其预期结果
Description :
    1、查看wal_level默认值
    2、修改wal_level为minimal，archive, hot_standby,校验其预期结果
    gs_guc set -D {cluster/dn1} -c "wal_level=minimal";
    gs_guc set -D {cluster/dn1} -c "wal_level=archive;
    gs_guc set -D {cluster/dn1} -c "wal_level=hot_standby";
    3、恢复默认值
Expect      :
    1、查看wal_level默认值 期望：hot_standby
    2、参数设置成功(将导致数据库无法启动)
    3、默认值恢复成功
History     : 
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class Guc(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Guc_WAL_Case0003_开始----')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.dbuser = Node('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()

    def test_guc(self):
        text = '--step1.show参数默认值; expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("wal_level")
        self.log.info(self.default_value)

        text = '--step2.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        text = '--step2.1.1修改参数wal_level=minimal;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_level=minimal")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)
        text = '--step2.1.2.重启数据库;expect:启动失败--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Unavailable" in status, '执行失败:' + text)
        text = '--step2.2.1.修改参数wal_level=archive;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg2 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_level=archive")
        self.log.info(guc_msg2)
        self.assertTrue(guc_msg2, '执行失败:' + text)
        text = '--step2.2.2.重启数据库;expect:启动失败--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Unavailable" in status, '执行失败:' + text)
        text = '--step2.3.1.修改参数wal_level=hot_standby;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg3 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_level=hot_standby")
        self.log.info(guc_msg3)
        self.assertTrue(guc_msg3, '执行失败:' + text)
        text = '--step2.3.2.重启数据库;expect:重启失败--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)

    def tearDown(self):
        text = '--step3.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        self.recovery_value = self.sh_user.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'wal_level={self.default_value}')
        self.log.info(self.recovery_value)
        msg = self.sh_user.restart_db_cluster()
        self.log.info(msg)
        status = self.sh_user.get_db_cluster_status()
        self.log.info(status)
        self.default_value2 = self.com.show_param("wal_level")
        self.log.info(self.default_value2)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.default_value2, self.default_value,
                         '执行失败:' + text)
        self.log.info('----Opengauss_Function_Guc_WAL_Case0003_结束----')

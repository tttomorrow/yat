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
Case Name   : 修改参数wal_buffers，观察预期结果
Description :
    1、查询wal_buffers默认值
    show wal_buffers;
    2、修改wal_buffers为20MB，重启使其生效，并校验其预期结果
    gs_guc set -D /xxx/dn1 -c "wal_buffers=20MB"
    gs_om -t stop && gs_om -t start
    show wal_buffers;
    3、修改wal_buffers为-1，重启使其生效，查询shared_buffers值，校验wal_buffers修改后预期结果
    gs_guc set -D /xxx/dn1 -c "wal_buffers=-1"
    gs_om -t stop && gs_om -t start
    show shared_buffers;
    show wal_buffers;
    4、修改wal_buffers为3，重启使其生效，校验wal_buffers修改后预期结果
    gs_guc set -D /xxx/dn1 -c "wal_buffers=3"
    gs_om -t stop && gs_om -t start
    show wal_buffers;
    5、恢复默认值
Expect      :
    1、显示默认值
    2、参数修改成功，校验修改后系统参数值为20MB
    3、参数修改成功，修改后wal_buffers的大小随着参数shared_buffers自动调整，为shared_buffers的1/32
    4、参数修改成功，wal_buffers设置为小于4时，会被默认设置为4(32kB)
    5、恢复默认值成功
History     : 
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0036_开始---')
        self.userNode = Node('dbuser')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.xlog_path = os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')
        self.constant = Constant()
        self.com = Common()

    def test_guc(self):
        text = '--step1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("wal_buffers")
        self.log.info(self.default_value)

        text = '--step2.1.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_buffers=20")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)

        text = '--step2.2.重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)

        text = '--step3.1.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_buffers=-1")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)

        text = '--step3.2.重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)

        text = '--step4.1.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_buffers=3")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)

        text = '--step4.2.重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)

    def tearDown(self):
        text = '--step5.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_buffers="
                                              f"{self.default_value}")
        self.log.info(guc_msg1)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.com.show_param("wal_buffers")
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info('---Opengauss_Function_Guc_WAL_Case0036_结束---')
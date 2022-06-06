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
Case Name   : 修改参数wal_level为minimal，并校验其预期结果
Description :
    1、查看wal_level默认值
    2、单机环境下，修改wal_level为minimal，archive_mode设置为off, hot_standby设置为off，
    max_wal_senders参数设置为0，校验其预期结果
    gs_guc set -D {cluster/dn1} -c "wal_level=minimal";
    gs_guc set -D {cluster/dn1} -c "archive_mode=off";
    gs_guc set -D {cluster/dn1} -c "hot_standby=off";
    gs_guc set -D {cluster/dn1} -c "max_wal_senders=0";
    3、恢复默认值
Expect      :
    1、查看wal_level默认值 期望：hot_standby
    2、参数设置成功(需单机环境，否则将导致数据库无法启动)
    3、默认值恢复成功
History     : 
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class Guc(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Guc_WAL_Case0001_开始----')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.dbuser = Node('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()

    def test_guc(self):
        text = '--step1.show参数默认值; expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value1 = self.com.show_param("wal_level")
        self.log.info(self.default_value1)
        self.default_value2 = self.com.show_param("archive_mode")
        self.log.info(self.default_value2)
        self.default_value3 = self.com.show_param("hot_standby")
        self.log.info(self.default_value3)
        self.default_value4 = self.com.show_param("max_wal_senders")
        self.log.info(self.default_value4)

        text = '--step2.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        text = '--step2.1.修改参数wal_level;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_level=minimal")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)
        text = '--step2.2.修改参数archive_mode;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg2 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"archive_mode=off")
        self.log.info(guc_msg2)
        self.assertTrue(guc_msg2, '执行失败:' + text)
        text = '--step2.3.修改参数hot_standby;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg3 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"hot_standby=off")
        self.log.info(guc_msg3)
        self.assertTrue(guc_msg3, '执行失败:' + text)
        text = '--step2.4.修改max_wal_senders;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg4 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"max_wal_senders=0")
        self.log.info(guc_msg4)
        self.assertTrue(guc_msg4, '执行失败:' + text)
        text = '--step2.5.重启数据库;expect:单机成功,其他失败--'
        self.log.info(text)
        if 1 == self.sh_user.get_node_num():
            text = '---单机环境---'
            self.log.info(text)
            restart_msg = self.sh_user.restart_db_cluster()
            self.log.info(restart_msg)
            status = self.sh_user.get_db_cluster_status('detail')
            self.log.info(status)
            self.assertTrue("Degraded" in status or "Normal" in status
                            , '执行失败:' + text)
            text = '--step2.6.show参数值;expect:参数值修改成功--'
            self.log.info(text)
            sql_cmd = self.sh_user.execut_db_sql(f'show wal_level;')
            self.log.info(sql_cmd)
            self.assertIn('minimal', sql_cmd, '执行失败:' + text)
            sql_cmd = self.sh_user.execut_db_sql(f'show archive_mode;')
            self.log.info(sql_cmd)
            self.assertIn('off', sql_cmd, '执行失败:' + text)
            sql_cmd = self.sh_user.execut_db_sql(f'show hot_standby;')
            self.log.info(sql_cmd)
            self.assertIn('off', sql_cmd, '执行失败:' + text)
            sql_cmd = self.sh_user.execut_db_sql(f'show max_wal_senders;')
            self.log.info(sql_cmd)
            self.assertIn('0', sql_cmd, '执行失败:' + text)
        else:
            text = '---主备环境---'
            self.log.info(text)
            restart_msg = self.sh_user.restart_db_cluster()
            self.log.info(restart_msg)
            status = self.sh_user.get_db_cluster_status('detail')
            self.log.info(status)
            self.assertTrue("Unavailable" in status, '执行失败:' + text)

    def tearDown(self):
        text = '--step3.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        text = '--step3.1.恢复参数wal_level;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"wal_level="
                                              f"{self.default_value1}")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)
        text = '--step3.2.恢复参数archive_mode;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg2 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"archive_mode="
                                              f"{self.default_value2}")
        self.log.info(guc_msg2)
        self.assertTrue(guc_msg2, '执行失败:' + text)
        text = '--step3.3.恢复参数hot_standby;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg3 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"hot_standby="
                                              f"{self.default_value3}")
        self.log.info(guc_msg3)
        self.assertTrue(guc_msg3, '执行失败:' + text)
        text = '--step3.4.恢复max_wal_senders;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg4 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"max_wal_senders="
                                              f"{self.default_value4}")
        self.log.info(guc_msg4)
        self.assertTrue(guc_msg4, '执行失败:' + text)
        text = '--step3.5.重启数据库;expect:重启数据库成功--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value1 = self.com.show_param("wal_level")
        self.log.info(self.recovery_value1)
        self.recovery_value2 = self.com.show_param("archive_mode")
        self.log.info(self.recovery_value2)
        self.recovery_value3 = self.com.show_param("hot_standby")
        self.log.info(self.recovery_value3)
        self.recovery_value4 = self.com.show_param("max_wal_senders")
        self.log.info(self.recovery_value4)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)
        self.assertEqual(self.recovery_value1, self.default_value1,
                         '执行失败:' + text)
        self.assertEqual(self.recovery_value2, self.default_value2,
                         '执行失败:' + text)
        self.assertEqual(self.recovery_value3, self.default_value3,
                         '执行失败:' + text)
        self.assertEqual(self.recovery_value4, self.default_value4,
                         '执行失败:' + text)
        self.log.info('----Opengauss_Function_Guc_WAL_Case0001_结束----')

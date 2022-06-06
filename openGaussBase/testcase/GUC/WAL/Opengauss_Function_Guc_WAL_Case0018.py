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
Case Name   : 修改参数checkpoint_segments，并校验其预期结果
Description :
    1、查看checkpoint_segments默认值；进入xlog目录统计xlog数量
    2、修改checkpoint_segments为实际大于xlog数量值，在数据库内做switchxlog操作，校验其预期结果
    3、恢复默认值
Expect      :
    1、显示默认值
    2、参数修改成功，产生足够xlog后，实际xlog数量大于设置的checkpoint_segments值
    3、恢复默认值
History     : 
"""
import os
import time
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0018_开始---')
        self.userNode = Node('dbuser')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.xlog_path = os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')
        self.constant = Constant()
        self.com = Common()

    def test_guc(self):
        text = '--step1.1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("checkpoint_segments")
        self.log.info(self.default_value)

        text = '--step1.2.进入xlog目录统计xlog数量;expect:统计xlog数量--'
        self.log.info(text)
        cd_cmd = f'cd {self.xlog_path};ls -l|grep "^-"| wc -l'
        self.log.info(cd_cmd)
        num_result = int(self.userNode.sh(cd_cmd).result()) + int(5)
        self.log.info(num_result)

        text = '--step2.1.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                      self.constant.GSGUC_SUCCESS_MSG,
                                      f"checkpoint_segments={num_result}")
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

        text = '--step2.3.1.在数据库内做switchxlog操作;expect:生成xlog日志--'
        self.log.info(text)
        for i in range(1, 50):
            sql_cmd = self.sh_user.execut_db_sql(f'select pg_switch_xlog();')
            self.log.info(sql_cmd)
        text = '--step2.3.2.进入xlog目录统计xlog数量;expect:统计xlog数量--'
        self.log.info(text)
        cd_cmd = f'cd {self.xlog_path};ls -l|grep "^-"| wc -l'
        self.log.info(cd_cmd)
        num_result_new = int(self.userNode.sh(cd_cmd).result())
        self.log.info(num_result_new)
        self.assertLessEqual(5, num_result_new, '执行失败:' + text)
        time.sleep(3)

    def tearDown(self):
        text = '--step3.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"checkpoint_segments="
                                              f"{self.default_value}")
        self.log.info(guc_msg1)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.com.show_param("checkpoint_segments")
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info('---Opengauss_Function_Guc_WAL_Case0018_结束---')

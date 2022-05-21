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
Case Name   : 修改参数archive_command，并观察预期结果
Description :
    1、查看archive_command默认值
    2、修改archive_command为，校验其预期结果
    3、进行switchxlog操作
    4、恢复默认值
Expect      :
    1、显示默认值
    2、参数修改成功，
    3、switchxlog操作完成
    4、恢复默认值成功
History     : 
"""
import os
import time
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from yat.test import Node
from yat.test import macro


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0024_开始---')
        self.userNode = Node('dbuser')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        self.xlog_path = os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog',
                                      'archive_status')
        self.conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      'postgresql.conf')

    def test_guc(self):
        text = '--step1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("archive_command")
        self.log.info(self.default_value)

        text = '--step2.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"archive_command="
                                              f"'cp --remove-destination %p "
                                              f"{self.xlog_path}/%f'")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)
        time.sleep(30)

        text = '--step3.在数据库内做switchxlog操作;expect:switchxlog操作完成--'
        self.log.info(text)
        for i in range(1, 20):
            sql_cmd = self.sh_user.execut_db_sql(f'select pg_switch_xlog();')
            self.log.info(sql_cmd)
        cd_cmd = f'cd {self.xlog_path};ls -l|grep "^-"| wc -l'
        self.log.info(cd_cmd)
        num_result_new = int(self.userNode.sh(cd_cmd).result())
        self.log.info(num_result_new)
        self.assertLessEqual(0, num_result_new, '执行失败:' + text)

    def tearDown(self):
        text = '--step4.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        sed_cmd = f"sed -i 's/archive_command/#archive_command/g' " \
            f"{self.conf_path};"
        guc_msg2 = self.userNode.sh(sed_cmd).result()
        self.log.info(guc_msg2)
        self.log.info('-----重启集群并检查数据库状态-----')
        result = self.sh_user.restart_db_cluster()
        self.log.info(result)
        result = self.sh_user.get_db_cluster_status('detail')
        self.log.info(result)
        self.recovery_value = self.com.show_param("archive_command")
        self.log.info(self.recovery_value)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.assertTrue("Degraded" in result or "Normal" in result,
                        '执行失败' + text)
        self.log.info('---Opengauss_Function_Guc_WAL_Case0024_结束---')

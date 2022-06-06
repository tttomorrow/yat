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
Case Name   : 修改参数archive_mode，并观察预期结果
Description :
    1、查看archive_mode默认值
    2、修改archive_mode为on，校验其预期结果
    3、进行switchxlog操作
    4、恢复默认值
Expect      :
    1、显示默认值
    2、参数修改成功
    3、switchxlog后dn1/pg_xlog/archive_status生成待归档文件
    4、恢复默认值成功
History     : 
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0022_开始---')
        self.userNode = Node('dbuser')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        self.xlog_path = os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog',
                                      'archive_status')

    def test_guc(self):
        text = '--step1.1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("archive_mode")
        self.log.info(self.default_value)
        cd_cmd = f'cd {self.xlog_path};ls -l|grep "^-"| wc -l'
        self.log.info(cd_cmd)
        num_result = int(self.userNode.sh(cd_cmd).result())
        self.log.info(num_result)

        text = '--step2.1.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"archive_mode=on")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)

        text = '--step2.2.校验参数是否修改成功;expect:修改成功--'
        self.log.info(text)
        self.modify_value = self.com.show_param("archive_mode")
        self.assertIn('on', self.modify_value, '执行失败:' + text)

        text = '--step3.在数据库内做switchxlog操作;expect:生成待归档文件--'
        self.log.info(text)
        for i in range(1, 10):
            sql_cmd = self.sh_user.execut_db_sql(f'select pg_switch_xlog();')
            self.log.info(sql_cmd)
        cd_cmd = f'cd {self.xlog_path};ls -l|grep "^-"| wc -l'
        self.log.info(cd_cmd)
        num_result_new = int(self.userNode.sh(cd_cmd).result())
        self.log.info(num_result_new)
        self.assertLess(num_result, num_result_new, '执行失败:' + text)

    def tearDown(self):
        text = '--step4.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"archive_mode ="
                                              f"{self.default_value}")
        self.log.info(guc_msg1)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.com.show_param("archive_mode")
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info('---Opengauss_Function_Guc_WAL_Case0022_结束---')

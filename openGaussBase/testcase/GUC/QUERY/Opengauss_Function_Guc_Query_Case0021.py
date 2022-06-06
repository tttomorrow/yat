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
Case Type   : GUC
Case Name   : 使用gs_guc set设置track_stmt_session_slot为无效值
Description :
    1、查询track_stmt_session_slot默认值，show track_stmt_session_slot;
    2、使用gs_guc set方式修改为其他值-1
       gs_guc set -D {cluster/dn1} -c "track_stmt_session_slot=-1";
    3、使用gs_guc set方式修改为其他值2147483648
       gs_guc set -D {cluster/dn1} -c "track_stmt_session_slot=2147483648";
    4、使用gs_guc set方式修改为其他值99.99
       gs_guc set -D {cluster/dn1} -c "track_stmt_session_slot=99.99";
    5、清理环境，恢复默认值;
Expect      :
    1、显示默认值，1000;
    2、参数设置失败;
    3、参数设置失败;
    4、参数设置失败;
    5、清理环境、恢复默认值成功;
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("======Opengauss_Function_Guc_Query_Case0021开始执行======")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.config_param1 = 'show track_stmt_session_slot;'
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======步骤一：查询track_stmt_session_slot默认望，为1000======")
        show_cmd1 = self.comsh.execut_db_sql(self.config_param1)
        logger.info(show_cmd1)
        self.assertEqual('1000', show_cmd1.splitlines()[-2].strip())

        logger.info("======步骤二：设置track_stmt_session_slot为-1======")
        set_cmd1 = self.comsh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'track_stmt_session_slot = -1')
        logger.info(set_cmd1)
        self.assertFalse(set_cmd1)

        logger.info("======步骤三：设置track_stmt_session_slot为2147483648======")
        set_cmd2 = self.comsh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'track_stmt_session_slot = '
                                            '2147483648')
        logger.info(set_cmd2)
        self.assertFalse(set_cmd2)

        logger.info("======步骤四：设置track_stmt_session_slot为99.99======")
        set_cmd3 = self.comsh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'track_stmt_session_slot = 99.99')
        logger.info(set_cmd3)
        self.assertFalse(set_cmd3)

    def tearDown(self):
        logger.info("======清理环境，恢复默认值======")
        cmd = self.comsh.execut_db_sql(self.config_param1)
        logger.info(cmd)
        if '1000' != cmd.splitlines()[-2].strip():
            self.comsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'track_stmt_session_slot = 1000')
        logger.info("======Opengauss_Function_Guc_Query_Case0021执行结束======")

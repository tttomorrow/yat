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
Case Name   : 初始用户使用guc命令修改参数值synchronous_commit为2
Description :
    1.查看默认值
    show synchronous_commit;
    2.初始用户使用guc命令修改参数值为2,Total instances为1
    gs_guc set -D /xxx/dn1/ -c "synchronous_commit = 2"
    3.数据库未重启，查看参数值，依然是默认值on
    show synchronous_commit;
    4.重启数据库
    gs_om -t stop && gs_om -t start
    5.查看参数值（remote_apply）
    show synchronous_commit;
    6.恢复默认值
    gs_om -t stop && gs_om -t start
Expect      :
    1.显示默认值
    2.初始用户使用guc命令修改参数值为2，失败为0
    3.数据库未重启，查看参数值，依然是默认值on
    4.重启数据库成功；
    5.查看参数值，为remote_apply
    6.恢复参数默认值成功
History     : 
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class Guc(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0081_开始---')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()

    def test_guc(self):
        text = '--step1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("synchronous_commit")
        self.log.info(self.default_value)

        text = '--step2.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"synchronous_commit=2")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)

        text = '--step3.show参数值;expect:参数值是on(数据库未重启，参数修改不生效)--'
        self.log.info(text)
        self.modify_value = self.com.show_param("synchronous_commit")
        self.assertEqual(self.modify_value, self.default_value,
                         '执行失败:' + text)

        text = '--step4.重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)

        text = '--step5.show参数值;expect:参数值修改成功--'
        self.log.info(text)
        self.modify_value = self.com.show_param("synchronous_commit")
        self.assertIn('remote_apply', self.modify_value, '执行失败:' + text)

    def tearDown(self):
        text = '--step6.1.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"synchronous_commit="
                                              f"{self.default_value}")
        self.log.info(guc_msg1)
        text = '--step6.2.重启数据库;expect:重启数据库成功--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.com.show_param("synchronous_commit")
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info('---Opengauss_Function_Guc_WAL_Case0081_结束---')

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
Case Name   : 初始用户使用gs_guc reload 命令修改参数值synchronous_commit为2
Description :
    1.查看默认值
    show synchronous_commit;
    2.初始用户使用gs_guc reload 命令修改参数值为2
    gs_guc reload -D /xxx/dn1 -c "synchronous_commit = 2"
    3.连接数据库查看，参数值已生效（remote_apply）
    show synchronous_commit;
    4.恢复参数默认值
Expect      :
    1.显示默认值
    2.gs_guc reload 命令修改参数值成功
    3.查看参数值remote_apply
    4.默认值恢复成功
History     : 
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0082_开始---')
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
        guc_msg1 = self.sh_user.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"synchronous_commit=2")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)

        text = '--step3.show参数值;expect:参数值修改成功--'
        self.log.info(text)
        sql_cmd = self.sh_user.execut_db_sql(f'show synchronous_commit;')
        self.log.info(sql_cmd)
        self.assertIn('remote_apply', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step4.1.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"synchronous_commit="
                                              f"{self.default_value}")
        self.log.info(guc_msg1)
        text = '--step4.2.重启数据库;expect:重启数据库成功--'
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
        self.log.info('---Opengauss_Function_Guc_WAL_Case0082_结束---')
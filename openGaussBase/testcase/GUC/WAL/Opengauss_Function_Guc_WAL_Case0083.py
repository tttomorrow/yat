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
Case Name   : 手动修改postgresql.conf文件中的参数synchronous_commit为3，重启，合理报错
Description :
    1.查看默认值
     cat /xxx/dn1/postgresql.conf | grep synchronous_commit
    2.手动修改参数值为3并重启数据库，重启失败
    gs_om -t stop && gs_om -t start
    3.恢复参数默认值
Expect      :
    1.显示默认值
    2.gs_guc reload 命令修改参数值成功
    3.默认值恢复成功
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro
from yat.test import Node

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0083_开始---')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.dbuser = Node('dbuser')
        self.constant = Constant()
        self.com = Common()
        self.conf = os.path.join(macro.DB_INSTANCE_PATH, 'postgresql.conf')

    def test_guc(self):
        text = '--step1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("synchronous_commit")
        self.log.info(self.default_value)

        text = '--step2.1手动修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        sed_cmd = f"sed -i 's/synchronous_commit = {self.default_value}/" \
            f"synchronous_commit = 3/g' " \
            f"{self.conf};" \
            f"cat {self.conf};"
        self.log.info(sed_cmd)
        result = self.dbuser.sh(sed_cmd).result()
        self.log.info(result)
        self.assertIn(f'synchronous_commit = 3', result, '执行失败:' + text)

        text = '--step2.2.重启数据库;expect:重启数据库失败--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertFalse("Degraded" in status or "Normal" in status,
                         '执行失败' + text)

    def tearDown(self):
        text = '--step3.1.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        set_cmd = self.sh_user.execute_gsguc('set',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f"synchronous_commit="
                                             f"{self.default_value}")
        self.log.info(set_cmd)
        text = '--step3.2.重启数据库;expect:重启数据库成功--'
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
        self.log.info('---Opengauss_Function_Guc_WAL_Case0083_结束---')

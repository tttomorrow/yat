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
Case Type   : keep_sync_window
Case Name   :  通过postgresql.conf文件修改keep_sync_window参数
Description :
        1.通过postgresql.conf文件修改参数为10s并重启数据库
        2.通过postgresql.conf文件修改参数为空值并重启数据库
        3.注释参数并重启数据库
Expect      :
        1.修改成功且重启数据库成功
        2.重启数据库失败
        3.修改成功且重启数据库成功
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0004 start-')
        self.constant = Constant()
        self.common = Common()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_node = Node('PrimaryDbUser')
        self.pg_conf = os.path.join(macro.DB_INSTANCE_PATH,
                                    macro.DB_PG_CONFIG_NAME)

    def test_keep_sync_window(self):
        text = '--step1:通过postgresql.conf文件修改参数为10s并重启数据库;' \
               'expect:修改成功且重启数据库成功'
        self.log.info(text)
        set_cmd = f"sed -i '$a keep_sync_window=10' { self.pg_conf}"
        self.log.info(set_cmd)
        msg = self.pri_node.sh(set_cmd).result()
        self.log.info(msg)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        value1 = self.common.show_param('keep_sync_window')
        self.assertEqual('10s', value1, '执行失败:' + text)

        text = '--step2:通过postgresql.conf文件修改参数为空值并重启数据库;' \
               'expect:重启数据库失败'
        self.log.info(text)
        cat_cmd = f"sed -i \"s/keep_sync_window=10/keep_sync_window" \
                  f"= ''/g\" {self.pg_conf}"
        self.log.info(cat_cmd)
        msg = self.pri_node.sh(cat_cmd).result()
        self.log.info(msg)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        self.assertFalse(restart_msg)

        text = '--step3:注释参数并重启数据库;' \
               'expect:修改成功且重启数据库成功'
        self.log.info(text)
        sed_cmd = f"sed -i 's/keep_sync_window/#keep_sync_window/g' " \
                  f"{self.pg_conf};"
        self.log.info(sed_cmd)
        msg = self.pri_node.sh(sed_cmd).result()
        self.log.info(msg)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        self.assertTrue(restart_msg)
        value2 = self.common.show_param('keep_sync_window')
        self.assertEqual('0', value2, '执行失败:' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:无须清理环境--'
        self.log.info(text)
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0004 finish-')

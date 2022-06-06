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
Case Type   : GUC参数
Case Name   : 使用gs_guc set方法设置参数explain_dna_file绝对路径,观察预期结果
Description :
    1.show参数默认值
    2.创建csv路径
    3.修改参数默认值为指定路径
    4.show参数值
    5.恢复参数默认值
    6.show参数值
    7.清理环境
Expect      :
    1.参数默认值为空
    2.创建成功
    3.修改成功
    4.参数值修改成功
    5.恢复参数默认值成功
    6.参数值为空
    7.清理环境完成
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DeveloperOptions_Case0023开始')
        self.dbuser = Node('PrimaryDbUser')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_guc_developeroptions(self):
        text = '--step1:show参数默认值;expect:参数值为空--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show explain_dna_file;')
        self.log.info(sql_cmd)
        default_value = sql_cmd.splitlines()[2].strip()
        self.log.info(default_value)

        text = '--step2.创建csv路径;expect:创建成功--'
        self.log.info(text)
        gsql_cmd = f'touch {macro.DB_INSTANCE_PATH}/explain_test.csv;'
        self.log.info(gsql_cmd)
        find_msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(find_msg)

        text = '--step3:修改参数默认值为指定路径;expect:修改成功--'
        self.log.info(text)
        mod_msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"explain_dna_file ="
                                              f"'{macro.DB_INSTANCE_PATH}"
                                              f"/explain_test.csv'")
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step4:show参数值;expect:参数值修改成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show explain_dna_file;')
        self.log.info(sql_cmd)
        self.assertIn(f'{macro.DB_INSTANCE_PATH}/explain_test.csv', sql_cmd,
                      '执行失败:' + text)

        text = '--step5.恢复参数默认值;expect:恢复成功--'
        self.log.info(text)
        gsql_cmd = f"sed -i '/explain_dna_file/d' " \
                   f"{macro.DB_INSTANCE_PATH}/postgresql.conf"
        self.log.info(gsql_cmd)
        find_msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(find_msg)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step6:show参数值;expect:参数值为空--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'show explain_dna_file;')
        self.log.info(sql_cmd)
        self.assertIn(default_value, sql_cmd,  '执行失败:' + text)

    def tearDown(self):
        text = '-step7:清理环境;expect:清理环境完成--'
        self.log.info(text)
        gsql_cmd = f'rm -rf {macro.DB_INSTANCE_PATH}/explain_test.csv;'
        self.log.info(gsql_cmd)
        find_msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(find_msg)
        self.log.info('Opengauss_Function_DeveloperOptions_Case0023结束')

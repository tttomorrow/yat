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
Case Name   : local_bind_address参数使用gs_guc reload 设置为空值
Description :
        1.查询local_bind_address默认值
        2.修改参数值为空
        3.查询
        4.清理环境
Expect      :
        1.数据库实例安装好后，根据XML配置文件中不同实例的IP地址配置不同默认值
        2.gs_guc reload命令执行成功
        3.参数值不变
        4.清理环境完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0036start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.primary_node = Node('PrimaryDbUser')

    def test_local_bind_address(self):
        text = '---step1:查询默认值;expect:数据库实例安装好后，' \
               '根据XML配置文件中不同实例的IP地址配置不同默认值---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show local_bind_address;')
        self.log.info(sql_cmd)
        self.assertEqual(f'{self.primary_node.db_host}',
                         sql_cmd.splitlines()[-2].strip(), '执行失败:' + text)

        text = '--step2:修改参数值为空值;expect:gs_guc reload命令执行成功--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('reload',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"local_bind_address=''")
        self.assertTrue(result, '执行失败:' + text)

        text = '---step3:查询;expect:参数值不变---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show local_bind_address;')
        self.log.info(sql_cmd)
        self.assertEqual(f'{self.primary_node.db_host}',
                         sql_cmd.splitlines()[-2].strip(), '执行失败:' + text)

    def tearDown(self):
        text = '---step4:清理环境;expect:清理环境完成---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('''show local_bind_address;''')
        self.log.info(sql_cmd)
        if f'{self.primary_node.db_host}' != sql_cmd.split('\n')[2].strip():
            msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"local_bind_address"
                                            f"='{self.primary_node.db_host}'",
                                            single=True)
            self.log.info(msg)
            msg = self.pri_sh.restart_db_cluster()
            self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0036finish-')

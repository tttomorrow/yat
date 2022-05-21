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
Case Name   : 使用gs_guc set方法设置参数standard_conforming_strings值为off，
              backslash_quote为off，查询反斜杠，合理报错
Description :
        1.查询standard_conforming_strings默认值
        2.执行语句select '\';
        3.修改参数值为off并重启数据库
        4.查询修改后的参数值
        5.设置参数backslash_quote为off并查询select '\';';
        6.恢复参数默认值
Expect      :
        1.显示默认值为on
        2.语句执行成功，显示反斜杠本身\
        3.修改成功
        4.显示off
        5.合理报错
        6.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '---Opengauss_Function_Guc_VPC_Case0003start---')
        self.constant = Constant()

    def test_standard_conforming_strings(self):
        LOG.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show
            standard_conforming_strings;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('---步骤2:默认值为on时，查询\符号，\会被作为普通的字符串---')
        sql_cmd = commonsh.execut_db_sql('''select '\\';''')
        LOG.info(sql_cmd)
        self.assertIn('\\', sql_cmd)
        LOG.info('---步骤3:修改参数值为off---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'standard_conforming_strings = off')
        LOG.info(msg)
        self.assertTrue(msg)
        LOG.info('---步骤4:重启数据库---')
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('---步骤5:查询修改后的参数值---')
        sql_cmd = commonsh.execut_db_sql('''show 
            standard_conforming_strings;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('---步骤6:修改backslash_quote为off，\不会作为普通的字符串---')
        sql_cmd = commonsh.execut_db_sql('''set backslash_quote to off;
                                                 select '\\';';''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd)
        self.assertIn('ERROR', sql_cmd)

    def tearDown(self):
        LOG.info('---步骤7:清理环境---')
        sql_cmd = commonsh.execut_db_sql('''set backslash_quote to
            safe_encoding;''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('''show 
            standard_conforming_strings;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'standard_conforming_strings'
                                         f'={self.res}')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show 
                   standard_conforming_strings;''')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_Guc_VPC_Case0003finish---')

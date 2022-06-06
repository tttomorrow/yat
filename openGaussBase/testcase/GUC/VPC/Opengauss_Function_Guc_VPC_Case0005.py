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
Case Name   : 使用gs_guc set方法设置参数escape_string_warning值为off,
              测试是否有告警输出
Description :
        1.查询escape_string_warning默认值
        2.设置参数standard_conforming_strings为off
        3.执行select '\';';
        4.修改escape_string_warning参数为off并查询
        5.执行select '\';';
        6.恢复参数默认值
Expect      :
        1.显示默认值为on
        2.设置成功
        3.有告警输出
        4.修改成功显示off
        5.无告警输出，显示';
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
            '---Opengauss_Function_Guc_VPC_Case0005start---')
        self.constant = Constant()

    def test_escape_string_warning(self):
        LOG.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show 
            escape_string_warning;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('---步骤2:设置参数standard_conforming_strings为off---')
        msg = commonsh.execute_gsguc('reload',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'standard_conforming_strings =off')
        LOG.info(msg)
        self.assertTrue(msg)
        LOG.info('---步骤3:测试反斜扛当转义符并且有警告输出---')
        sql_cmd = commonsh.execut_db_sql('''select '\\';';''')
        LOG.info(sql_cmd)
        self.assertIn('WARNING', sql_cmd)
        LOG.info('---步骤4:修改参数值escape_string_warning为off---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'escape_string_warning=off')
        LOG.info(msg)
        self.assertTrue(msg)
        LOG.info('---步骤5:重启数据库---')
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('---步骤6:查询修改后的参数值---')
        sql_cmd = commonsh.execut_db_sql('''show escape_string_warning;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('---步骤7:反斜扛当转义符并且无警告输出---')
        sql_cmd = commonsh.execut_db_sql('''select '\\';';''')
        LOG.info(sql_cmd)
        self.assertIn("';", sql_cmd)

    def tearDown(self):
        LOG.info('---步骤8:清理环境---')
        sql_cmd = commonsh.execut_db_sql('''show 
            escape_string_warning;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'escape_string_warning'
                                         f'={self.res}')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show 
                    escape_string_warning;''')
        LOG.info(sql_cmd)
        msg = commonsh.execute_gsguc('reload',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'standard_conforming_strings = on')
        LOG.info(msg)
        self.assertTrue(msg)
        sql_cmd = commonsh.execut_db_sql('''show 
            standard_conforming_strings;''')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_Guc_VPC_Case0005finish---')

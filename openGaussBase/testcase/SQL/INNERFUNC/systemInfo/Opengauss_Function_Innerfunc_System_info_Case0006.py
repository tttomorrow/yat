"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : 系统管理函数
Case Name   : pg_conf_load_time() 返回最后加载服务器配置文件的时间戳
Description :
    1. pg_conf_load_time返回最后加载服务器配置文件的时间戳
Expect      :
    1.返回成功
History     :
"""
import unittest
import time
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0006开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.pg_conf_load_time返回最后加载服务器配置文件的时间戳-')
        restrt = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t restart'
        LOG.info(restrt)
        check_msg = self.dbuser_node.sh(restrt).result()
        LOG.info(check_msg)
        date1 = time.strftime("%Y-%m-%d %H", time.localtime())
        LOG.info(date1)
        sql_cmd = self.commonsh.execut_db_sql(f'select pg_conf_load_time();')
        LOG.info(sql_cmd)
        self.assertIn(f'{date1}', sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0006结束-')

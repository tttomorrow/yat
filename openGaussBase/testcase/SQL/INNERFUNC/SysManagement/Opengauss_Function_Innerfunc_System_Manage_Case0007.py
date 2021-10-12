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
Case Type   : 系统管理函数-其他函数
Case Name   :  使用函数textlen()查询text的逻辑长度
Description :
    1.查询text的逻辑长度
Expect      :
    1.查询text的逻辑长度成功
History     : 
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0007开始-')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info(f'---步骤1.查询text的逻辑长度---')
        text = f' <?xml version="1.0" encoding="UTF-8"?>' \
            f'-<ROOT>-<CLUSTER> <PARAM value="gauss_openv1" ' \
            f'name="clusterName"/><PARAM value="ctupopenga00019" ' \
            f'name="nodeNames"/><PARAM value="' \
            f'/data/opengauss_hsl_0310/cluster/app" '
        sql_cmd = self.commonsh.execut_db_sql(f'select textlen(\'{text}\');')
        LOG.info(sql_cmd)
        self.assertIn('192', sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0007结束-')

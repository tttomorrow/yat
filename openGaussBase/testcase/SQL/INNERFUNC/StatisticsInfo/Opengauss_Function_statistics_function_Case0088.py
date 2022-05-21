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
Case Type   : 统计信息函数
Case Name   : gs_wlm_get_resource_pool_info(int),获取所有用户的资源使用统计信息
Description :
    1.获取所有用户的资源使用统计信息
Expect      :
    1.获取所有用户的资源使用统计信息成功
History     : 
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0088开始')
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_built_in_func(self):
        self.log.info('-----步骤1.获取所有用户的资源使用统计信息--')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select gs_wlm_get_resource_pool_info(1);')
        self.log.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)
        str1 = sql_cmd.split('\n')[-2]
        self.log.info(f'str1 = {str1}')
        num = len(str1.split(','))
        self.log.info(f'list1 = {num}')
        if num == 7:
            self.log.info('获取所有用户的资源使用统计信息成功')
        else:
            raise Exception('函数执行异常，请检查')

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0088结束')

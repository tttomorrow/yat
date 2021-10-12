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
Case Type   : 功能测试
Case Name   : 使用random()函数生成0.0到1.0之间的随机数。
Description :
    1.多次执行select random();语句
    2.执行select random(1,3);语句
    3.执行select random('a');语句
Expect      :
    1.随机数生成成功
    2.合理报错
    3.合理报错
History     :
"""

import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        logger.info("----------Opengauss_Function_Innerfunc_Random_Case0001开始执行------------")
        self.commonsh = CommonSH('dbuser')

    def test_random(self):
        logger.info("-----------------正常获取-------------------")

        res = set()
        for n in range(5):
            cmd1 = f'''select random();'''
            msg1 = self.commonsh.execut_db_sql(cmd1)
            logger.info(msg1)
            res.add(float('0' + msg1.splitlines()[2].strip()))  # 值放入集合

        self.assertTrue(len(res) == 5)  # 验证获取的值随机不等
        for i in res:
            if not 0.0 < i < 1.0:
                raise ValueError('返回值错误')  # 验证函数返回值范围正确

        logger.info("-----------------异常校验-------------------")
        cmd2 = f'''select random(1,3);
                   select random('a');'''
        msg2 = self.commonsh.execut_db_sql(cmd2)
        logger.info(msg2)
        self.assertTrue(msg2.count('ERROR') == 2)

    def tearDown(self):
        logger.info('----------Opengauss_Function_Innerfunc_Random_Case0001执行结束------------')

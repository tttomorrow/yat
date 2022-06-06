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
Case Type   : set
Case Name   : set命令设置时区为无效值，合理报错
Description :
    1.设置时区值为中文
    2.设置时区不合法
    3.设置时区不合法
Expect      :
    1.合理报错
    2.合理报错
    3.合理报错
History     :
    修改sql脚本为py
"""
import sys
import unittest
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class SETTIMEZONE(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0015开始执行-----------------------------')

    def test_set_timezone(self):
        sql_cmd1 = commonsh.execut_db_sql('''set time zone '欧洲罗马';
                                           set time zone PST;
                                           set time zone KST;''')
        logger.info(sql_cmd1)
        self.assertIn('ERROR:  invalid value for parameter "TimeZone":', sql_cmd1)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DML_Set_Case0015执行结束--------------------------')

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
Case Type   : 用户-权限测试
Case Name   : 初始用户修改目录对象属主为普通用户，成功
Description :
    1.初始用户创建目录对象
    2.创建普通用户
    3.初始用户修改directory属主为普通用户
    4.删除用户和目录
Expect      :
    1.创建成功
    2.用户创建成功
    3.修改成功
    4.删除成功
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Directory(unittest.TestCase):
    def setUp(self):
        logger.info(f'-----{os.path.basename(__file__)} 开始执行-----')

    def test_common_user_permission(self):
        text = '-----step1:初始用户创建目录对象;expect:成功'
        logger.info(text)
        sql_cmd1 = "drop directory if exists test_dir;" \
                   "create directory test_dir as '/tmp/';"
        logger.info(sql_cmd1)
        msg1 = commonsh.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(constant.CREATE_DIRECTORY_SUCCESS_MSG, msg1,
                      '执行失败' + text)

        text = '-----step2:创建普通用户;expect:成功'
        logger.info(text)
        sql_cmd2 = commonsh.execut_db_sql(f"drop user if exists "
                                          f"test_com cascade;"
                                          f"create user test_com password "
                                          f"'{macro.COMMON_PASSWD}';")
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2,
                      '执行失败' + text)

        text = '-----step3:修改directory属主为普通用户;expect:合理报错'
        logger.info(text)
        sql_cmd3 = commonsh.execut_db_sql('''
        alter directory test_dir owner to test_com;''')
        logger.info(sql_cmd3)
        self.assertIn('ALTER DIRECTORY', sql_cmd3, '执行失败' + text)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        text = '-----step3:删除用户和目录;expect:成功'
        logger.info(text)
        sql_cmd4 = commonsh.execut_db_sql('drop directory test_dir;'
                                          'drop user test_com cascade;')
        logger.info(sql_cmd4)
        self.assertIn(constant.DROP_DIRECTORY_SUCCESS_MSG, sql_cmd4,
                      '执行失败' + text)
        self.assertIn(constant.DROP_ROLE_SUCCESS_MSG, sql_cmd4, '执行失败' + text)
        logger.info(f'-----{os.path.basename(__file__)} 执行结束-----')

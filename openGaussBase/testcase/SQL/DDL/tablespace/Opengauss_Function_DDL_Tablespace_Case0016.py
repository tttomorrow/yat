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
Case Type   : 功能测试-表空间
Case Name   : 表空间创建指定相对路径RELATIVE
Description :
    1、创建tablespace指定相对路径为空
    2、创建tablespace指定相对路径为三层
    3、创建tablespace指定相对路径为绝对路径格式
    4、创建tablespace指定相对路径包含$>
    5、创建tablespace指定相对路径为两层
    6、创建tablespace指定相对路径与已存在表空间路径存在嵌套
    7、创建tablespace指定相对路径下不为空
Expect      :
    1、创建tablespace指定相对路径为空，创建失败
    2、创建tablespace指定相对路径为三层，创建失败
    3、创建tablespace指定相对路径为绝对路径格式，创建失败
    4、创建tablespace指定相对路径包含$>，创建失败
    5、创建tablespace指定相对路径为两层，创建成功
    6、创建tablespace指定相对路径与已存在表空间路径存在嵌套，创建失败
    7、创建tablespace指定相对路径下不为空，创建成功
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tablespace(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_dbuser = Node(node='PrimaryDbUser')

        self.constant = Constant()
        self.tbspc_name1 = 'tsp_tbspc0016_1'
        self.tbspc_name2 = 'tsp_tbspc0016_2'
        self.tbspc_location1 = 'dir1/dir2/dir3'
        self.tbspc_location2 = '/dir1/dir2'
        self.tbspc_location3 = 'dir1$/dir2>'
        self.tbspc_location4 = 'tbspc0016_dir1/dir2'
        self.tbspc_location5 = 'tbspc0016_existsfiledir'
        self.location5 = os.path.join(macro.DB_INSTANCE_PATH,
                                      'pg_location', self.tbspc_location5)
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0016'
        self.connect_info = f'-U {self.sys_user} -W {self.pwd}'
        self.err_flag1 = 'ERROR:  The relative location can not be null'
        self.err_flag2 = "ERROR:  relative location can only be formed of " \
                         "'a~z', 'A~Z', '0~9', '-', '_' and " \
                         "two level directory at most"
        self.err_flag3 = 'ERROR:  find conflict linkpath'

    def test_main(self):
        step_txt = '----step0:创建系统管理员用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2}; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step1:创建tablespace指定相对路径为空; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertEqual(self.err_flag1, create_result, "执行失败" + step_txt)

        step_txt = '----step2:创建tablespace指定相对路径为三层; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertEqual(self.err_flag2, create_result, "执行失败" + step_txt)

        step_txt = '----step3:创建tablespace指定相对路径为绝对路径格式; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location2}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertEqual(self.err_flag2, create_result, "执行失败" + step_txt)

        step_txt = '----step4:创建tablespace指定相对路径包含$>; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location3}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertEqual(self.err_flag2, create_result, "执行失败" + step_txt)

        step_txt = '----step5:创建tablespace指定相对路径为两层; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location4}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result)
        self.log.info('--检查relative标志是否正确--')
        check_sql = f"select relative from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        check_result = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(check_result)
        self.assertIn('t', check_result, "执行失败" + step_txt)

        step_txt = '----step6:创建tablespace指定相对路径与已存在表空间路径存在嵌套; expect:失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name2} relative " \
            f"location '{os.path.dirname(self.tbspc_location4)}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag3, create_result, "执行失败" + step_txt)

        step_txt = '----step7:创建tablespace指定相对路径下不为空; expect:创建成功----'
        self.log.info(step_txt)
        self.log.info('--创建非空目录及文件--')
        create_cmd = f'rm -rf {self.location5};mkdir {self.location5};' \
            f'cd {self.location5};' \
            f'touch existsfile.txt;' \
            f'ls -lt {self.location5}'
        self.log.info(create_cmd)
        create_result = self.pri_dbuser.sh(create_cmd).result()
        self.log.info(create_result)
        self.assertIn('existsfile.txt', create_result, "执行失败" + step_txt)
        self.log.info('--创建表空间，指定相对路径不为空--')
        create_sql = f"create tablespace {self.tbspc_name2} " \
            f"relative location '{self.tbspc_location5}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2}; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')

        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(1, drop_user, "执行失败" + step_txt)
        self.assertEqual(2, drop_tbspc, "执行失败" + step_txt)

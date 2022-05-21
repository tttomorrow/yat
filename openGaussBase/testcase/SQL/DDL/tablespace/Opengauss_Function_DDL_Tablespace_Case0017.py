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
Case Name   : 表空间创建指定绝对路径LOCATION
Description :
    1、创建tablespace指定绝对路径为空
    2、创建tablespace指定绝对路径为相对路径格式
    3、创建tablespace指定绝对路径包含$>
    4、创建tablespace指定绝对路径为数据库数据目录下
    5、创建tablespace指定绝对路径正确
    6、创建tablespace指定绝对路径与已存在表空间路径存在嵌套
    7、创建tablespace指定绝对路径与数据库应用不同磁盘
    8、创建tablespace指定绝对路径下不为空
Expect      :
    1、创建tablespace指定绝对路径为空，创建失败
    2、创建tablespace指定绝对路径为相对路径格式，创建失败
    3、创建tablespace指定绝对路径包含$>，创建失败
    4、创建tablespace指定绝对路径为数据库数据目录下，创建失败
    5、创建tablespace指定绝对路径正确，创建成功
    6、创建tablespace指定绝对路径与已存在表空间路径存在嵌套，创建失败
    7、创建tablespace指定绝对路径与数据库应用不同磁盘，创建成功
    8、创建tablespace指定绝对路径下不为空，创建成功
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

pri_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != pri_sh.get_node_num(), '非1+2环境不执行')
class Tablespace(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.sta1_dbuser = Node(node='Standby1DbUser')
        self.sta2_dbuser = Node(node='Standby2DbUser')
        self.constant = Constant()
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0017'
        self.connect_info = f'-U {self.sys_user} -W {self.pwd}'
        self.tbspc_name1 = 'tsp_tbspc0017_1'
        self.tbspc_name2 = 'tsp_tbspc0017_2'
        self.tbspc_name3 = 'tsp_tbspc0017_3'
        self.parent_dir = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tbspc0017')

        self.tbspc_location1 = 'dir1/dir2'
        self.tbspc_location2 = os.path.join(self.parent_dir,
                                            'dir1$/dir2>')
        self.tbspc_location3 = os.path.join(macro.DB_INSTANCE_PATH, 'dir1')
        self.tbspc_location4 = os.path.join(self.parent_dir,
                                            'tbspc0017_dir1/dir2')
        self.tbspc_location5 = os.path.join(self.parent_dir,
                                            'tbspc0017_dir1/dir2/dir3')
        self.tbspc_location6 = os.path.join(macro.DB_BACKUP_PATH,
                                            'tbspc0017_dir1')
        self.tbspc_location7 = os.path.join(self.parent_dir,
                                            'tbspc0017_dir1', 'existsfiledir')

        self.err_flag1 = "ERROR:  tablespace location must " \
                         "be an absolute path"
        self.err_flag2 = "ERROR:  tablespace cannot be " \
                         "created under data directory"
        self.err_flag3 = "ERROR:  tablespace location can only " \
                         "be formed of 'a~z', 'A~Z', '0~9', '-', '_'"
        self.err_flag4 = "ERROR:  find conflict linkpath"

    def test_main(self):
        step_txt = '----step0:创建系统管理员用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step1:创建tablespace指定绝对路径为空; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"location '';"
        create_result = pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag1, create_result, "执行失败" + step_txt)

        step_txt = '----step2:创建tablespace指定绝对路径为相对路径格式; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"location '{self.tbspc_location1}';"
        create_result = pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag1, create_result, "执行失败" + step_txt)

        step_txt = '----step3:创建tablespace指定绝对路径包含$; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"location '{self.tbspc_location2}';"
        create_result = pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag3, create_result, "执行失败" + step_txt)

        step_txt = '----step4:创建tablespace指定绝对路径为数据库数据目录下; expect:创建失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"location '{self.tbspc_location3}';"
        create_result = pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag2, create_result, "执行失败" + step_txt)

        step_txt = '----step5:创建tablespace指定绝对路径正确; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"location '{self.tbspc_location4}';"
        create_result = pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--检查relative标志是否正确--')
        check_sql = f"select relative from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        check_result = pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(check_result)
        self.assertEqual('f', check_result.strip(), "执行失败" + step_txt)
        self.log.info('--检查路径是否设置正确--')
        loc_sql = f"select pg_tablespace_location(" \
            f"(select oid from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}'));"
        loc_info = pri_sh.execut_db_sql(loc_sql).splitlines()[-2].strip()
        self.log.info(loc_info)
        self.assertEqual(self.tbspc_location4, loc_info, "执行失败" + step_txt)

        step_txt = '----step6:创建tablespace指定绝对路径与已存在表空间路径存在嵌套; expect:失败----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name2} " \
            f"location '{self.tbspc_location5}';"
        create_result = pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag4, create_result, "执行失败" + step_txt)

        step_txt = '----step7:创建tablespace指定绝对路径与数据库应用不同磁盘; expect:成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name2} " \
            f"location '{self.tbspc_location6}';"
        create_result = pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--检查relative标志是否正确--')
        check_sql = f"select relative from pg_tablespace where " \
            f"spcname = '{self.tbspc_name2}';"
        check_result = pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(check_result)
        self.assertEqual('f', check_result.strip(), "执行失败" + step_txt)
        self.log.info('--检查路径是否设置正确--')
        loc_sql = f"select pg_tablespace_location(" \
            f"(select oid from pg_tablespace where " \
            f"spcname = '{self.tbspc_name2}'));"
        loc_info = pri_sh.execut_db_sql(loc_sql).splitlines()[-2].strip()
        self.log.info(loc_info)
        self.assertEqual(self.tbspc_location6, loc_info, "执行失败" + step_txt)

        step_txt = '----step8:创建tablespace指定绝对路径下不为空; expect:成功----'
        self.log.info(step_txt)
        self.log.info('--创建非空目录及文件--')
        create_cmd = f'mkdir {self.tbspc_location7};' \
            f'cd {self.tbspc_location7};' \
            f'touch existsfile.txt;' \
            f'ls -lt {self.tbspc_location7}'
        self.log.info(create_cmd)
        create_result = self.pri_dbuser.sh(create_cmd).result()
        self.log.info(create_result)
        self.assertIn('existsfile.txt', create_result, "执行失败" + step_txt)
        self.log.info('--创建表空间，指定绝对路径不为空--')
        create_sql = f"create tablespace {self.tbspc_name3} " \
            f"location '{self.tbspc_location7}';"
        create_result = pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2}; " \
            f"drop tablespace if exists {self.tbspc_name3}; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        step2_txt = '----删除表空间路径; expect:成功----'
        self.log.info(step2_txt)
        del_cmd = f"rm -rf {self.parent_dir}; " \
            f"rm -rf {self.tbspc_location6};" \
            f"if [ -d {self.parent_dir} ]; then echo 'exists'; " \
            f"else echo 'not exists'; fi;" \
            f"if [ -d {self.tbspc_location6} ]; then echo 'exists'; " \
            f"else echo 'not exists'; fi;"
        self.log.info(del_cmd)
        del_result1 = self.pri_dbuser.sh(del_cmd).result()
        del_result2 = self.sta1_dbuser.sh(del_cmd).result()
        del_result3 = self.sta2_dbuser.sh(del_cmd).result()
        self.log.info(del_result1)
        self.log.info(del_result2)
        self.log.info(del_result3)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')

        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(1, drop_user, "执行失败" + step1_txt)
        self.assertEqual(3, drop_tbspc, "执行失败" + step1_txt)
        self.assertEqual(2, del_result1.count('not exists'),
                         "执行失败" + step1_txt)
        self.assertEqual(2, del_result2.count('not exists'),
                         "执行失败" + step1_txt)
        self.assertEqual(2, del_result3.count('not exists'),
                         "执行失败" + step1_txt)

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
Case Name   : 表空间创建限额
Description :
    2、创建tablespace设置限额大于8388607TB
    3、创建tablespace设置限额含小数2.5TB
    4、创建tablespace设置限额不带单位
    5、创建tablespace设置限额单位为G
    6、创建tablespace设置限额单位为M
Expect      :
    2、创建tablespace设置限额大于8388607TB，创建失败
    3、创建tablespace设置限额含小数2.5TB，创建失败
    4、创建tablespace设置限额不带单位，创建失败
    5、创建tablespace设置限额单位为G，创建成功
    6、创建tablespace设置限额单位为M，创建成功
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro


class Tablespace(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.tbspc_name1 = 'tsp_tbspc0018_1'
        self.tbspc_name2 = 'tsp_tbspc0018_2'
        self.tblspace_location1 = 'tbspc0018_1'
        self.tblspace_location2 = 'tbspc0018_2'
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0018'
        self.connect_info = f'-U {self.sys_user} -W {self.pwd}'

        self.err_flag1 = 'HINT:  Value exceeds max size ' \
        self.err_flag2 = 'HINT:  Value exceeds max size 8388607 with unit TB'
        self.err_flag3 = 'HINT:  Valid units are "k/K", "m/M", "g/G", ' \
                         '"t/T", and "p/P".'
        self.err_flag4 = 'HINT:  lost valid unit'
        self.maxsize = 500

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

        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tblspace_location1}' " \
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag1, create_result, "执行失败" + step_txt)

        step_txt = '----step2:创建tablespace设置限额大于8388607TB;expect:成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tblspace_location1}' " \
            f"maxsize '8388608T';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag2, create_result, "执行失败" + step_txt)

        step_txt = '----step3:创建tablespace设置限额含小数2.5TB;expect:成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tblspace_location1}' " \
            f"maxsize '2.5T';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag3, create_result, "执行失败" + step_txt)

        step_txt = '----step4:创建tablespace设置限额不带单位;expect:成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tblspace_location1}' " \
            f"maxsize '500';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.err_flag4, create_result, "执行失败" + step_txt)

        step_txt = '----step5:创建tablespace设置限额单位为G;expect:成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tblspace_location1}' " \
            f"maxsize '{self.maxsize}G';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('----检查tablespace设置限额大小----')
        check_sql = f"select spcmaxsize from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(size)
        self.assertIn(str(self.maxsize * pow(1024, 2)), size,
                      "执行失败" + step_txt)

        step_txt = '----step6:创建tablespace设置限额单位为M;expect:成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name2} " \
            f"relative location '{self.tblspace_location2}' " \
            f"maxsize '{self.maxsize}M';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_info)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('----检查tablespace设置限额大小----')
        check_sql = f"select spcmaxsize from pg_tablespace where " \
            f"spcname = '{self.tbspc_name2}';"
        size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(size)
        self.assertIn(str(self.maxsize * 1024), size, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2}; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(1, drop_user, "执行失败" + step1_txt)
        self.assertEqual(2, drop_tbspc, "执行失败" + step1_txt)

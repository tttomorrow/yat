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
Case Name   : 修改空间限额-基础验证
Description :
    2、修改空间限额，修改限额大于8388607TB
    3、修改空间限额，修改值为小数+单位
    4、修改空间限额，修改值不带单位
    5、修改空间限额，修改限额单位为G，与初始值不一致
    6、修改空间限额，修改限额单位为M，与初始值一致
    7、普通用户非表空间所有者修改空间限额，与初始值一致
Expect      :
    2、修改空间限额，修改限额大于8388607TB，修改失败
    3、修改空间限额，修改值为小数+单位，修改失败
    4、修改空间限额，修改值不带单位，修改失败
    5、修改空间限额，修改限额单位为G，与初始值不一致，修改成功
    6、修改空间限额，修改限额单位为M，与初始值一致，修改成功
    7、普通用户非表空间所有者修改空间限额，与初始值一致，修改失败
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
        self.tbspc_name1 = 'tsp_tbspc0029'
        self.tbspc_location1 = 'tbspc0029'
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0029_sys'
        self.com_user = 'u_tbspc0029_com'
        self.connect_sys = f'-U {self.sys_user} -W {self.pwd}'
        self.connect_com = f'-U {self.com_user} -W {self.pwd}'

        self.err_flag1 = 'HINT:  Value exceeds max size ' \
        self.err_flag2 = 'HINT:  Value exceeds max size 8388607 with unit TB'
        self.err_flag3 = 'HINT:  Valid units are "k/K", "m/M", "g/G", ' \
                         '"t/T", and "p/P".'
        self.err_flag4 = 'HINT:  lost valid unit'
        self.err_flag5 = 'ERROR:  permission denied for tablespace'
        self.maxsize = 500

    def test_main(self):
        step_txt = '----step0:创建系统管理员/普通用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.com_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.com_user} password '{self.pwd}';" \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step0:初始创建tablespace设置限额单位为M; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}' " \
            f"maxsize '{self.maxsize}M';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('检查tablespace设置限额大小----')
        check_sql = f"select spcmaxsize from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(size)
        self.assertIn(str(self.maxsize * 1024), size, "执行失败" + step_txt)

        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag1, alter_result, "执行失败" + step_txt)

        step_txt = '----step2:修改空间限额，修改限额大于8388607TB; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"resize maxsize '8388608T';"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag2, alter_result, "执行失败" + step_txt)

        step_txt = '----step3:修改空间限额，修改值为小数+单位; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"resize maxsize '2.5T';"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag3, alter_result, "执行失败" + step_txt)

        step_txt = '----step4:修改空间限额，修改值不带单位; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"resize maxsize '500';"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag4, alter_result, "执行失败" + step_txt)

        step_txt = '----step5:修改空间限额，修改限额单位为G，与初始值不一致; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"resize maxsize '{self.maxsize}G';"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('检查tablespace设置限额大小----')
        size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(size)
        self.assertIn(str(self.maxsize * pow(1024, 2)), size,
                      "执行失败" + step_txt)

        step_txt = '----step6:修改空间限额，修改限额单位为M，与初始值一致; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"resize maxsize '{self.maxsize}M';"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('检查tablespace设置限额大小----')
        size = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(size)
        self.assertIn(str(self.maxsize * 1024), size, "执行失败" + step_txt)

        step_txt = '----step7:普通用户非表空间所有者修改空间限额，与初始值一致; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"resize maxsize '{self.maxsize}M';"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_com)
        self.log.info(alter_result)
        self.assertIn(self.err_flag5, alter_result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.com_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(2, drop_user, "执行失败" + step1_txt)
        self.assertEqual(1, drop_tbspc, "执行失败" + step1_txt)

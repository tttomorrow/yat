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
Case Name   : 重置表空间属性-random_page_cost、seq_page_cost
Description :
    0、创建系统管理员; 
    0、指定seq_page_cost、random_page_cost属性创建表空间;
    1、单独重置random_page_cost属性;
    2.1、同时修改表空间seq_page_cost、random_page_cost设定值为正浮点数;
    2.2、单独重置seq_page_cost属性;
    3.1、同时修改表空间seq_page_cost、random_page_cost设定值为正浮点数;
    3.2、同时重置seq_page_cost、random_page_cost属性;
    4、未设置seq_page_cost、random_page_cost设定值场景下重置参数;
Expect      :
    0、创建系统管理员; 创建成功
    0、指定seq_page_cost、random_page_cost属性创建表空间; 创建成功
    1、单独重置random_page_cost属性; 修改成功
    2.1、同时修改表空间seq_page_cost、random_page_cost设定值为正浮点数; 修改成功
    2.2、单独重置seq_page_cost属性; 修改成功
    3.1、同时修改表空间seq_page_cost、random_page_cost设定值为正浮点数; 修改成功
    3.2、同时重置seq_page_cost、random_page_cost属性; 修改成功
    4、未设置seq_page_cost、random_page_cost设定值场景下重置参数; 修改失败
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
        self.tbspc_name1 = 'tsp_tbspc0028'
        self.tbspc_location1 = 'tbspc0028'
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0028_sys'
        self.connect_sys = f'-U {self.sys_user} -W {self.pwd}'
        self.err_flag = 'ERROR:  RESET must not include values for parameters'

    def test_main(self):
        step_txt = '----step0:创建系统管理员; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step0:指定seq_page_cost、random_page_cost属性创建表空间; ' \
                   'expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location \'{self.tbspc_location1}\' " \
            f"with (seq_page_cost=9.333,random_page_cost=9.33333);"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        check_sql = f"select spcoptions from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertIn('seq_page_cost=9.333,random_page_cost=9.33333',
                      spcoptions, "执行失败" + step_txt)

        step_txt = '----step1:单独重置random_page_cost属性; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"reset (random_page_cost);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertNotIn('random_page_cost', spcoptions, "执行失败" + step_txt)
        self.assertIn('seq_page_cost=9.333', spcoptions, "执行失败" + step_txt)

        step_txt = '----step2.1:同时修改表空间seq_page_cost、random_page_cost设定值' \
                   '为正浮点数; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"set (seq_page_cost=9.333,random_page_cost =9.33333);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertIn('seq_page_cost=9.333,random_page_cost=9.33333',
                      spcoptions, "执行失败" + step_txt)

        step_txt = '----step2.2:单独重置seq_page_cost属性; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"reset (seq_page_cost);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertNotIn('seq_page_cost', spcoptions, "执行失败" + step_txt)
        self.assertIn('random_page_cost=9.33333', spcoptions,
                      "执行失败" + step_txt)

        step_txt = '----step3.1:同时修改表空间seq_page_cost、random_page_cost设定值' \
                   '为正浮点数; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"set (seq_page_cost=9.333,random_page_cost =9.33333);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertIn('seq_page_cost=9.333,random_page_cost=9.33333',
                      spcoptions, "执行失败" + step_txt)

        step_txt = '----step3.2:同时重置seq_page_cost、random_page_cost属性; ' \
                   'expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"reset (seq_page_cost,random_page_cost);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertEqual(' ', spcoptions, "执行失败" + step_txt)

        step_txt = '----step4：未设置seq_page_cost、random_page_cost设定值场景下重置参数; ' \
                   'expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"reset (seq_page_cost=9.333,random_page_cost =9.33333);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag, alter_result, "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertEqual(' ', spcoptions, "执行失败" + step_txt)

        self.log.info('----4、重置属性不存在----')
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"reset (seq_page_,random_page_);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertEqual(' ', spcoptions, "执行失败" + step_txt)

    def tearDown(self):
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(1, drop_user, "执行失败" + step1_txt)
        self.assertEqual(1, drop_tbspc, "执行失败" + step1_txt)

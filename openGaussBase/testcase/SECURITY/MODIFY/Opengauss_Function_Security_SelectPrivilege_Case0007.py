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
Case Type   : 防篡改
Case Name   : 三权分立打开时验证普通用户对于public模式下的表没有select权限，赋予select权限之后可以查询表
Description :
    1.设置参数并重启数据库enableSeparationOfDuty=on
    2.创建两个普通用户
    3.授予普通用户1在public下创建对象的权限
    4.切换普通用户1创建表并插入数据
    5.切换普通用户2对表进行select操作
    6.切换普通用户1对授权给普通用户2
    7.切换普通用户2对表进行select操作
    8.清理环境
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.permission denied
    6.成功
    7.成功
    8.成功
History     :
"""


import os
import unittest
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.table_name = 't_security_selectprivilege_0007'
        self.user_name1 = 'u_security_selectprivilege_0007_01'
        self.user_name2 = 'u_security_selectprivilege_0007_02'
        self.default_value = self.common.show_param('enableSeparationOfDuty')

    def test_security(self):
        text = '-----step1：设置参数并重启数据库enableSeparationOfDuty=on; ' \
               'expect:成功-----'
        self.log.info(text)
        mod_msg = \
            self.primary_sh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'enableSeparationOfDuty=on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        restart_msg = self.primary_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '-----step2：创建两个普通用户 expect:成功-----'
        self.log.info(text)
        create_cmd = f"drop user if exists {self.user_name1} cascade;" \
            f"drop user if exists {self.user_name2} cascade; " \
            f"create user {self.user_name1} password " \
            f"'{macro.PASSWD_REPLACE}';" \
            f"create user {self.user_name2} password " \
            f"'{macro.PASSWD_REPLACE}';"
        msg = self.primary_sh.execut_db_sql(create_cmd)
        self.log.info(msg)
        self.assertTrue(msg.count(self.constant.CREATE_ROLE_SUCCESS_MSG) == 2,
                        '执行失败:' + text)

        text = '-----step3：授予普通用户1在public下创建对象的权限 ' \
               'expect:成功-----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(
            f"grant create on schema public to {self.user_name1};")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '----step4:切换普通用户1创建表并插入数据; expect:成功----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            set role {self.user_name1} password '{macro.PASSWD_REPLACE}';
            create  table public.{self.table_name}
            (id int,name varchar(100));
            insert into public.{self.table_name}  
            values(1,'beijing'),(2,'shanghai');''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step5:切换普通用户2对表进行select操作; ' \
               'expect:权限拒绝 permission denied----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            set role {self.user_name2} password '{macro.PASSWD_REPLACE}';
            select * from public.{self.table_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.constant.PERMISSION_DENIED,
                      sql_cmd, "执行失败:" + text)

        text = '----step6:切换普通用户1对授权给普通用户2; expect:成功----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            set role {self.user_name1} password '{macro.PASSWD_REPLACE}';
            grant select on table public.{self.table_name} to {self.user_name2};
            ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step7:切换普通用户2对表进行select操作; expect:成功----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            set role {self.user_name2} password '{macro.PASSWD_REPLACE}';
            select * from public.{self.table_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn('2 rows', sql_cmd, "执行失败:" + text)

    def tearDown(self):
        text = '----step8:清理环境 expect:成功----'
        self.log.info(text)
        self.log.info('恢复参数默认值')
        mod_msg1 = \
            self.primary_sh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f'enableSeparationOfDuty='
                                          f'{self.default_value}')
        self.log.info(mod_msg1)
        self.assertTrue(mod_msg1, '执行失败:' + text)
        restart_msg = self.primary_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.primary_sh.get_db_cluster_status()
        self.log.info('删除用户')
        sql_cmd = self.primary_sh.execut_db_sql(
            f"drop user {self.user_name1} cascade;"
            f"drop user {self.user_name2} cascade;")
        self.log.info(sql_cmd)
        self.assertTrue(sql_cmd.count
                        (self.constant.DROP_ROLE_SUCCESS_MSG) == 2,
                        '执行失败:' + text)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

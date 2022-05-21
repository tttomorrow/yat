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
Case Name   : 验证会提前提示修改口令
Description :
    1.查询参数
    2.设置口令有效期为1天
    3.创建用户
    4.新用户登录数据库
    5.清理环境
Expect      :
    1.显示默认值90、7
    2.成功
    3.成功
    4.数据库登录成功会提前提示修改口令
    5.成功
History     : 
"""



import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.common = Common()
        self.user_name = 'u_security_mgt_manamegent_0005'
        self.default_value1 = self.common.show_param('password_effect_time')
        self.default_value2 = self.common.show_param('password_notify_time')

    def test_security(self):
        text = '----step1:查询参数值; expect:默认值90、7、60----'
        self.logger.info(text)
        show_para1 = self.default_value1
        show_para2 = self.default_value2
        self.logger.info(show_para1)
        self.logger.info(show_para2)
        self.assertTrue('90' in show_para1 and
                        '7' in show_para2, "执行失败:" + text)

        text = '----step2:设置参数有效期1天;  expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            alter system set password_effect_time to 1;
            alter system set password_notify_time to 1;
            select pg_sleep(4);
            show password_effect_time;
            show password_notify_time;''')
        self.logger.info(sql_cmd)
        self.assertEqual("1", sql_cmd.split("\n")[-2].strip(),
                         "执行失败:" + text)
        self.assertEqual("1", sql_cmd.split("\n")[-7].strip(),
                         "执行失败:" + text)

        text = '----step3:创建用户 expect:成功----'
        self.logger.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            create user {self.user_name} password '{macro.PASSWD_REPLACE}';''')
        self.logger.info(sql_cmd)
        self.assertTrue(
            sql_cmd.count(self.Constant.CREATE_ROLE_SUCCESS_MSG) == 1,
            "执行失败:" + text)

        text = '----step4:新用户登录数据库 ' \
               'expect:数据库登录成功会提前提示修改口令----'
        self.logger.info(text)
        connect_sql = f'gsql -d {self.dbuserNode.db_name} ' \
            f'-p {self.dbuserNode.db_port} -U {self.user_name} ' \
            f'-W {macro.PASSWD_REPLACE}'
        execute_cmd = f'''source {macro.DB_ENV_PATH}
              expect <<EOF
              set timeout 10
              spawn {connect_sql}
              expect "{self.dbuserNode.db_name}=#"
              expect eof\n''' + '''EOF'''
        self.logger.info(execute_cmd)
        msg = self.dbuserNode.sh(execute_cmd).result()
        self.logger.info(msg)
        self.assertIn('1 days left before password expired, '
                      'please change the password', msg, '执行失败:' + text)

    def tearDown(self):
        text = '----step5:清理环境 expect:成功----'
        self.logger.info(text)
        self.logger.info('删除用户')
        sql_cmd1 = self.primary_sh.execut_db_sql(f'''
                drop user {self.user_name} cascade;''')
        self.logger.info(sql_cmd1)
        self.logger.info('恢复默认值')
        sql_cmd2 = self.primary_sh.execut_db_sql(f'''
            alter system set password_effect_time to {self.default_value1};
            alter system set password_notify_time to {self.default_value2};
            select pg_sleep(4);
            show password_effect_time;
            show password_notify_time;''')
        self.logger.info(sql_cmd2)
        self.assertEqual("7", sql_cmd2.split("\n")[-2].strip(),
                         "执行失败:" + text)
        self.assertEqual("90", sql_cmd2.split("\n")[-7].strip(),
                         "执行失败:" + text)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd1,
                      '执行失败:' + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

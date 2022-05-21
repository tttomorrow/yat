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
Case Type   : security_masking
Case Name   : 使用regexpmasking方式脱敏，同一张表中增加、修改、移除脱敏策略
Description :
    1.poladmin用户创建表，并赋予表的所有操作权限给用户1
    2.poladmin用户将敏感字段加到资源标签
    3.poladmin用户设置脱敏策略regexpmasking,过滤用户1
    4.用户1连接数据库查看表string字段是否脱敏
    5.增加一个maskall策略,用户1连接数据库查看person表新增脱敏策略是否生效
    6.修改脱敏策略1为creditcardmasking,查看是否修改生效
    7.删除脱敏策略creditcardmasking,查看是否删除生效
Expect      :
    1.创表成功，赋权成功
    2.资源标签创建成功：CREATE RESOURCE LABEL
    3.脱敏策略添加成功
    4.查询到string字段的信息脱敏，第四位到第十位数字脱敏，脱敏数据被指定字母代替
    5.新增脱敏策略成功，脱敏策略生效
    6.修改脱敏策略成功，脱敏策略生效
    7.删除脱敏策略成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.userNode = Node(node='PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.poladmin = 'pol_security_masking_0080'
        self.user = 'u_security_masking_0080'
        self.table = f'{self.poladmin}.table_security_masking_0080'
        self.res_label1 = 'rl01_security_masking_0080'
        self.res_label2 = 'rl02_security_masking_0080'
        self.masking_policy = 'mp1_security_masking_0080'
        self.common = Common()
        self.constant = Constant()
        self.default_policy = self.common.show_param('enable_security_policy')
    
    def test_masking(self):
        text = '-----pre1:创建安全策略管理员、普通用户;expect:成功-----'
        self.logger.info(text)
        create_cmd = f'drop user if exists {self.poladmin};' \
            f'drop user if exists {self.user};' \
            f'create user {self.poladmin} with POLADMIN password \'' \
            f'{macro.COMMON_PASSWD}\';create user {self.user} with ' \
            f'password \'{macro.COMMON_PASSWD}\';' \
            f'grant all privileges to {self.user};'
        create_msg = self.sh_primy.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertTrue(
            create_msg.count(self.constant.CREATE_ROLE_SUCCESS_MSG) == 2,
            '执行失败' + text)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, create_msg,
                      '执行失败' + text)
        
        text = '-----pre2:开启安全策略开关;expect:成功-----'
        self.logger.info(text)
        result = self.sh_primy.execute_gsguc('reload',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f'enable_security_policy=on')
        self.assertEqual(True, result, '执行失败' + text)
        check_msg = self.common.show_param('enable_security_policy')
        self.logger.info(check_msg)
        self.assertEqual('on', check_msg, '执行失败' + text)
        
        text = '-----step1:poladmin用户创建表;expect:成功-----'
        self.logger.info(text)
        sql_cmd1 = f'drop table if exists {self.table};' \
            f'create table {self.table}(id int,name char(10),string ' \
            f'text,address varchar(60));' \
            f'insert into {self.table} values(1,\'张三\',' \
            f'\'6402-3372-0368-5477-5801\',\'Shanxi,Xian,yuhuazhai\'),' \
            f'(2,\'李四\',\'1354-7676-6854-8988-1232\',\'Fujian\');'
        content1 = f'-U {self.user} -W {macro.COMMON_PASSWD}'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type=f'{content1}')
        self.logger.info(msg1)
        self.assertIn((self.constant.CREATE_TABLE_SUCCESS), msg1,
                      '执行失败' + text)
        self.assertIn((self.constant.INSERT_SUCCESS_MSG), msg1,
                      '执行失败' + text)
        
        text = '-----step2:poladmin用户将敏感字段加到资源标签;expect:成功-----'
        self.logger.info(text)
        sql_cmd2 = f'drop resource label if exists {self.res_label1};' \
            f'create resource label {self.res_label1} ' \
            f'add column({self.table}.string);' \
            f'drop resource label if exists {self.res_label2};' \
            f'create resource label {self.res_label2} ' \
            f'add column({self.table}.address);'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2, sql_type=f'{content1}')
        self.logger.info(msg2)
        self.assertIn(self.constant.resource_label_create_success_msg, msg2,
                      '执行失败' + text)
        
        text = '-----step3:poladmin用户设置脱敏策略regexpmasking,过滤用户1;' \
               'expect:成功-----'
        self.logger.info(text)
        sql_cmd3 = f'drop masking policy if exists {self.masking_policy};' \
            f'create masking policy {self.masking_policy} ' \
            f'regexpmasking(\'[\d+]\',\'x\',2,10) on ' \
            f'label({self.res_label1}) filter on ' \
            f'roles({self.user});'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3, sql_type=f'{content1}')
        self.logger.info(msg3)
        self.assertIn(self.constant.masking_policy_create_success_msg, msg3,
                      '执行失败' + text)
        
        text = '-----step4:用户1连接数据库查看表string字段是否脱敏;' \
               'expect:成功-----'
        self.logger.info(text)
        sql_cmd4 = f'select string from {self.table};'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4, sql_type=f'{content1}')
        self.logger.info(msg4)
        self.assertIn('13xx-xxxx-xx54-8988-1232', msg4, '执行失败' + text)
        self.assertIn('64xx-xxxx-xx68-5477-5801', msg4, '执行失败' + text)
        
        text = '-----step5:增加一个maskall策略,用户1连接数据库查看person表新增脱敏' \
               '策略是否生效;expect:成功-----'
        self.logger.info(text)
        add_masking_sql = f'alter masking policy {self.masking_policy} ' \
            f'add maskall on label({self.res_label2});'
        add_masking_msg = self.sh_primy.execut_db_sql(add_masking_sql)
        self.logger.info(add_masking_msg)
        self.assertEqual(self.constant.alter_masking_policy_success,
                         add_masking_msg, '执行失败' + text)
        sql_cmd5 = f'select address from {self.table};'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5, sql_type=f'{content1}')
        self.logger.info(msg5)
        self.assertIn('xxxxxxxxxxxxxxxxxxxxx', msg5, '执行失败' + text)
        self.assertIn('xxxxxx', msg5, '执行失败' + text)
        
        text = '-----step6:修改脱敏策略1为creditcardmasking,查看是否修改生效;' \
               'expect:成功-----'
        self.logger.info(text)
        add_masking_sql = f'alter masking policy {self.masking_policy} ' \
            f'modify creditcardmasking on label({self.res_label1});'
        add_masking_msg = self.sh_primy.execut_db_sql(add_masking_sql)
        self.logger.info(add_masking_msg)
        self.assertEqual(self.constant.alter_masking_policy_success,
                         add_masking_msg, '执行失败' + text)
        sql_cmd6 = f'select string from {self.table};'
        msg6 = self.sh_primy.execut_db_sql(sql_cmd6, sql_type=f'{content1}')
        self.logger.info(msg6)
        self.assertIn('xxxx-xxxx-xxxx-xxxx-5801', msg6, '执行失败' + text)
        self.assertIn('xxxx-xxxx-xxxx-xxxx-1232', msg6, '执行失败' + text)
        
        text = '-----step7:删除脱敏策略creditcardmasking,查看是否删除生效;' \
               'expect:成功-----'
        self.logger.info(text)
        add_masking_sql = f'alter masking policy {self.masking_policy} ' \
            f'remove creditcardmasking on label({self.res_label1});'
        add_masking_msg = self.sh_primy.execut_db_sql(add_masking_sql)
        self.logger.info(add_masking_msg)
        self.assertEqual(self.constant.alter_masking_policy_success,
                         add_masking_msg, '执行失败' + text)
        sql_cmd7 = f'select string from {self.table};'
        msg7 = self.sh_primy.execut_db_sql(sql_cmd7, sql_type=f'{content1}')
        self.logger.info(msg7)
        self.assertIn('6402-3372-0368-5477-5801', msg7, '执行失败' + text)
        self.assertIn('1354-7676-6854-8988-1232', msg7, '执行失败' + text)
    
    def tearDown(self):
        text = '-----恢复参数配置-----'
        self.logger.info(text)
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                            f'enable_security_policy={self.default_policy}')
        check_msg = self.common.show_param('enable_security_policy')
        self.logger.info(check_msg)
        
        text = '-----清理表对象-----'
        self.logger.info(text)
        drop_cmd = f'drop masking policy if exists {self.masking_policy};' \
            f'drop resource label if exists {self.res_label1};' \
            f'drop resource label if exists {self.res_label2};' \
            f'drop table {self.table};'
        content2 = f'-U {self.poladmin} -W {macro.COMMON_PASSWD}'
        drop_msg = self.sh_primy.execut_db_sql(drop_cmd,
                                               sql_type=f'{content2}')
        self.logger.info(drop_msg)
        
        text = '-----清理用户-----'
        self.logger.info(text)
        drop_user_cmd = f'drop user {self.user} cascade;' \
            f'drop user {self.poladmin} cascade;'
        drop_user_msg = self.sh_primy.execut_db_sql(drop_user_cmd)
        self.logger.info(drop_user_msg)
        self.assertEqual(self.default_policy, check_msg, '执行失败' + text)
        self.assertIn(self.constant.drop_masking_policy_success, drop_msg,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_resource_label_success, drop_msg,
                      '执行失败' + text)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_msg,
                      '执行失败' + text)
        self.assertTrue(
            drop_user_msg.count(self.constant.DROP_ROLE_SUCCESS_MSG) == 2,
            '执行失败' + text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

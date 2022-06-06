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
Case Name   : 最多支持创建98个动态数据脱敏策略
Description :
    1.poladmin用户创建表，并赋予表的所有操作权限给用户user001
    2.poladmin用户将敏感字段加到资源标签
    3.poladmin用户创建脱敏策略99个
    4.清理资源:删除资源标签，删除脱敏策略,删除表，删除用户,关闭安全策略开关
Expect      :
    1.创表成功，赋权成功
    2.资源标签创建成功：CREATE RESOURCE LABEL
    3.第98个脱敏策略创建成功，第99个创建失败
    4.清理资源成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        text = '---Opengauss_Function_Security_Masking_Case0062 start---'
        self.logger.info(text)
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.poladmin = 'poladmin_security_masking_0062'
        self.com_user = 'com_security_masking_0062'
        self.resource_label = 'rl_security_masking_0062'
        self.masking_policy = 'mp_security_masking_0062'
        self.table = 'table_security_masking_0062'

        self.logger.info(
            '-----检查参数，修改配置:enable_security_policy=on-----')
        self.config_item = 'enable_security_policy'
        self.sql_cmd = f'show {self.config_item};'
        check_res = self.sh_primy.execut_db_sql(self.sql_cmd)
        self.logger.info(check_res)
        self.check_default = check_res.splitlines()[-2].strip()
        if 'on' != self.check_default:
            result = self.sh_primy.execute_gsguc('reload',
                        self.constant.GSGUC_SUCCESS_MSG,
                        f'{self.config_item}=on')
            self.assertTrue(result, '参数修改失败')
        msg = self.sh_primy.execut_db_sql(self.sql_cmd)
        self.logger.info(msg)
        self.common.equal_sql_mdg(msg, f'{self.config_item}', 'on',
                                  '(1 row)', flag='1')

    def test_masking(self):
        text = '---step1.1：创建poladmin及普通用户 expect:创建成功，权限赋予成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop owned by {self.poladmin} cascade;' \
                   f'drop user if exists {self.poladmin};' \
                   f'drop user if exists {self.com_user};' \
                   f'create user {self.poladmin} with POLADMIN ' \
                   f'password \'{macro.COMMON_PASSWD}\';' \
                   f'create user {self.com_user} with password ' \
                   f'\'{macro.COMMON_PASSWD}\';' \
                   f'grant all privileges to {self.com_user};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        assert_1 = msg1.count(self.constant.CREATE_ROLE_SUCCESS_MSG) == 2
        assert_2 = self.constant.ALTER_ROLE_SUCCESS_MSG in msg1
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)

        for i in range(99):
            text = '---step1.2：poladmin用户创建表 expect:创表成功---'
            self.logger.info(text)
            table = '_'.join([self.table, str(i)])
            sql_cmd4 = f'''drop table if exists {table};
                create table {table}(id int,name char(10),
                creditcard varchar(25),address varchar(60)) 
                with (orientation =column); 
                insert into {table} values
                (1,'张三','3214-5260-0070-1456-226',
                'Shanxi,Xian,yuhuazhai'),
                (2,'李四','5677-5260-7655-1456-776',
                'Shanxi,hanzhong,yangxian');'''
            excute_cmd4 = f'source {macro.DB_ENV_PATH};' \
                          f'gsql -d {self.userNode.db_name} ' \
                          f'-p {self.userNode.db_port} ' \
                          f'-U {self.poladmin} ' \
                          f'-W {macro.COMMON_PASSWD} ' \
                          f'-c "{sql_cmd4}"'
            self.logger.info(excute_cmd4)
            msg4 = self.userNode.sh(excute_cmd4).result()
            self.logger.info(msg4)
            assert_3 = self.constant.CREATE_TABLE_SUCCESS in msg4
            assert_4 = self.constant.INSERT_SUCCESS_MSG in msg4
            self.assertTrue(assert_3 and assert_4, '执行失败:' + text)

            text = '---step2: poladmin用户将敏感字段加到资源标签，' \
                   'except: 资源标签创建成功---'
            self.logger.info(text)
            resource_label = '_'.join([self.resource_label, str(i)])
            sql_cmd5 = f'drop resource label if exists {resource_label};' \
                       f'create resource label {resource_label} ' \
                       f'add column({table}.creditcard);'
            excute_cmd5 = f'source {macro.DB_ENV_PATH};' \
                          f'gsql -d {self.userNode.db_name} ' \
                          f'-p {self.userNode.db_port} ' \
                          f'-U {self.poladmin} ' \
                          f'-W {macro.COMMON_PASSWD} ' \
                          f'-c "{sql_cmd5}"'
            self.logger.info(excute_cmd5)
            msg5 = self.userNode.sh(excute_cmd5).result()
            self.logger.info(msg5)
            assert_5 = self.constant.resource_label_create_success_msg in msg5
            self.assertTrue(assert_5, '执行失败:' + text)

            text = '---step3：poladmin用户创建脱敏策略99个，' \
                   'except: 前98个脱敏策略创建成功，第99个创建失败---'
            self.logger.info(text)
            masking_policy = '_'.join([self.masking_policy, str(i)])
            sql_cmd6 = f'drop masking policy if exists {masking_policy};' \
                       f'create masking policy {masking_policy} ' \
                       f'maskall on label({resource_label}) ' \
                       f'filter on roles({self.com_user});'
            excute_cmd6 = f'source {macro.DB_ENV_PATH};' \
                          f'gsql -d {self.userNode.db_name} ' \
                          f'-p {self.userNode.db_port} ' \
                          f'-U {self.poladmin} ' \
                          f'-W {macro.COMMON_PASSWD} ' \
                          f'-c "{sql_cmd6}"'
            self.logger.info(excute_cmd6)
            msg6 = self.userNode.sh(excute_cmd6).result()
            self.logger.info(msg6)
            if i < 98:
                assert_6 = self.constant.masking_policy_create_success_msg \
                           in msg6
            else:
                assert_6 = 'Too many policies, adding new policiy is ' \
                           'restricted' in msg6
            self.assertTrue(assert_6, '执行失败：' + text)

    def tearDown(self):
        self.logger.info('-------step4: 清理资源 expect:清理资源成功-------')
        for i in range(99):
            resource_label = '_'.join([self.resource_label, str(i)])
            masking_policy = '_'.join([self.masking_policy, str(i)])
            sql_cmd1 = f'drop masking policy {masking_policy};' \
                       f'drop resource label {resource_label};'
            excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
                          f'gsql -d {self.userNode.db_name} ' \
                          f'-p {self.userNode.db_port} ' \
                          f'-U {self.poladmin} ' \
                          f'-W {macro.COMMON_PASSWD} ' \
                          f'-c "{sql_cmd1}"'
            self.logger.info(excute_cmd1)
            msg1 = self.userNode.sh(excute_cmd1).result()
            self.logger.info(msg1)
        sql_cmd2 = f'select * from GS_MASKING_POLICY_ACTIONS ' \
                   f'where actlabelname like \'{self.resource_label}%\';' \
                   f'select * from gs_policy_label where labelname ' \
                   f'like \'{self.resource_label}%\';'
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} ' \
                      f'-p {self.userNode.db_port} ' \
                      f'-U {self.poladmin} ' \
                      f'-W {macro.COMMON_PASSWD} ' \
                      f'-c "{sql_cmd2}"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        sql_cmd3 = f'drop owned by {self.poladmin} cascade;' \
                   f'drop user {self.com_user};' \
                   f'drop user {self.poladmin};'
        self.logger.info(sql_cmd3)
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.logger.info(
            '----检查参数，恢复默认配置:enable_security_policy----')
        check_res = self.sh_primy.execut_db_sql(self.sql_cmd)
        self.logger.info(check_res)
        current = check_res.splitlines()[-2].strip()
        if self.check_default != current:
            result = self.sh_primy.execute_gsguc('reload',
                        self.constant.GSGUC_SUCCESS_MSG,
                        f'{self.config_item}={self.check_default}')
            self.assertTrue(result, '参数恢复失败')
        msg4 = self.sh_primy.execut_db_sql(self.sql_cmd)
        self.logger.info(msg4)
        self.assertTrue(msg2.count('(0 rows)') == 2)
        self.assertIn(self.constant.DROP_OWNED_SUCCESS,
                      msg3.splitlines()[0].strip())
        self.assertTrue(msg3.count(self.constant.DROP_ROLE_SUCCESS_MSG) == 2)
        self.common.equal_sql_mdg(msg4, f'{self.config_item}',
                    f'{self.check_default}', '(1 row)', flag='1')
        self.logger.info(
            '---Opengauss_Function_Security_Masking_Case0062 finish---')
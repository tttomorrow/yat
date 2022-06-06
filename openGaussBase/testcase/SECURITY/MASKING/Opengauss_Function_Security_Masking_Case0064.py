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
Case Name   : 脱敏后的数据为查询条件，更新数据
Description :
    1.管理员用户创建表，并赋予表的所有操作权限给用户user004
    2.poladmin用户将敏感字段加到资源标签
    3.poladmin用户设置脱敏策略creditcardmasking
    4.user004用户连接数据库查看表creditcard字段是否脱敏
    5.以脱敏后的数据为条件，更新数据
    6.清理资源：删除资源标签，删除脱敏策略,删除表，删除用户,关闭安全策略开关
Expect      :
    1.创表成功，赋权成功
    2.资源标签创建成功：CREATE RESOURCE LABEL
    3.脱敏策略添加成功：CREATE MASKING POLICY
    4.creditcard字段的信息，后四位之前的数字已脱敏
    5.更新原数据失败
    6.清理资源成功
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
        text = '---Opengauss_Function_Security_Masking_Case0064 start---'
        self.logger.info(text)
        self.userNode = Node('PrimaryDbuser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.poladmin = 'poladmin_security_masking_0064'
        self.com_user = 'com_security_masking_0064'
        self.resource_label = 'rl_security_masking_0064'
        self.masking_policy = 'mp_security_masking_0064'
        self.table = 'public.table_security_masking_0064'

        self.logger.info(
            '------检查参数，修改配置:enable_security_policy=on------')
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
        text = '---step1.1：创建poladmin及普通用户，' \
               'expect:创建成功，权限赋予成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop user if exists {self.poladmin};' \
                   f'drop user if exists {self.com_user};' \
                   f'create user {self.poladmin} with POLADMIN ' \
                   f'password \'{macro.COMMON_PASSWD}\';' \
                   f'create user {self.com_user} with password \'' \
                   f'{macro.COMMON_PASSWD}\';' \
                   f'grant all privileges to {self.com_user};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        assert_1 = msg1.count(self.constant.CREATE_ROLE_SUCCESS_MSG) == 2
        assert_2 = self.constant.ALTER_ROLE_SUCCESS_MSG in msg1
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)

        text = '---step1.2：管理员用户创建表 expect:创表成功---'
        self.logger.info(text)
        sql_cmd4 = f'''drop table if exists {self.table};
                    create table {self.table}(id int,name char(10),
                    creditcard varchar(25),address varchar(60));
                    insert into {self.table} values
                    (1,'张三','6236-0044-7120-1432-645',
                    'Shanxi,Xian,yuhuazhai'),
                    (2,'李四','5432-1502-0666-3215-663',
                    'Fujian,Xiamen');'''
        self.logger.info(sql_cmd4)
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        assert_3 = self.constant.CREATE_TABLE_SUCCESS in msg4
        assert_4 = self.constant.INSERT_SUCCESS_MSG in msg4
        self.assertTrue(assert_3 and assert_4, '执行失败:' + text)

        text = '---step2.poladmin用户将敏感字段加到资源标签,' \
               'expect:资源标签创建成功---'
        self.logger.info(text)
        sql_cmd5 = f'drop resource label if exists {self.resource_label};' \
                   f'create resource label {self.resource_label} ' \
                   f'add column({self.table}.creditcard);'
        excute_cmd5 = f'source {macro.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U {self.poladmin} -W ' \
                      f'{macro.COMMON_PASSWD} -c "{sql_cmd5}"'
        self.logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        assert_5 = self.constant.resource_label_create_success_msg in msg5
        self.assertTrue(assert_5, '执行失败：' + text)

        text = '---step3: poladmin用户设置脱敏策略creditcardmasking,' \
               'except:脱敏策略添加成功---'
        self.logger.info(text)
        sql_cmd6 = f'drop masking policy if exists {self.masking_policy};' \
                   f'create masking policy {self.masking_policy} ' \
                   f'creditcardmasking on label({self.resource_label}) ' \
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
        assert_6 = self.constant.masking_policy_create_success_msg in msg6
        self.assertTrue(assert_6, '执行失败：' + text)

        text = '---step4: user004用户连接数据库查看表creditcard字段' \
               '是否脱敏,except:creditcard字段的信息，后四位之前的数字已脱敏---'
        self.logger.info(text)
        sql_cmd7 = f'select creditcard from {self.table};'
        excute_cmd7 = f'source {macro.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} ' \
                      f'-p {self.userNode.db_port} ' \
                      f'-U {self.com_user} ' \
                      f'-W {macro.COMMON_PASSWD} ' \
                      f'-c "{sql_cmd7}"'
        self.logger.info(excute_cmd7)
        msg7 = self.userNode.sh(excute_cmd7).result()
        self.logger.info(msg7)
        assert_7 = 'xxxx-xxxx-xxxx-xxxx-645' and \
                   'xxxx-xxxx-xxxx-xxxx-663' in msg7
        self.assertTrue(assert_7, '执行失败:' + text)

        text = '---step5: 以脱敏后的数据为条件，更新数据,except：更新原数据失败---'
        self.logger.info(text)
        sql_cmd8 = f'update {self.table} set address = ' \
                   f'\'guangdong,shengzhen\' where creditcard = ' \
                   f'\'xxxx-xxxx-xxxx-xxxx-645\';'
        excute_cmd8 = f'source {macro.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} ' \
                      f'-p {self.userNode.db_port} -U {self.com_user} ' \
                      f'-W {macro.COMMON_PASSWD} -c "{sql_cmd8}"'
        self.logger.info(excute_cmd8)
        msg8 = self.userNode.sh(excute_cmd8).result()
        self.logger.info(msg8)
        self.assertEqual(msg8, 'UPDATE 0')

    def tearDown(self):
        self.logger.info('-------step6: 清理资源 expect:清理资源成功------')
        sql_cmd1 = f'drop masking policy {self.masking_policy};' \
                   f'drop resource label {self.resource_label};'
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p' \
                      f'{self.userNode.db_port} -U {self.poladmin} ' \
                      f'-W {macro.COMMON_PASSWD} -c "{sql_cmd1}"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = f'drop table {self.table};' \
                   f'drop user {self.com_user};' \
                   f'drop user {self.poladmin};'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.logger.info(
            '-------检查参数，恢复默认配置:enable_security_policy-------')
        check_res = self.sh_primy.execut_db_sql(self.sql_cmd)
        self.logger.info(check_res)
        current = check_res.splitlines()[-2].strip()
        if self.check_default != current:
            result = self.sh_primy.execute_gsguc('reload',
                     self.constant.GSGUC_SUCCESS_MSG,
                     f'{self.config_item}= {self.check_default}')
            self.assertTrue(result, '参数恢复失败')
        msg3 = self.sh_primy.execut_db_sql(self.sql_cmd)
        self.logger.info(msg3)
        self.common.equal_sql_mdg(msg3, f'{self.config_item}',
                f'{self.check_default}', '(1 row)', flag='1')
        self.assertIn(self.constant.drop_masking_policy_success,
                      msg1.splitlines()[0].strip())
        self.assertIn(self.constant.drop_resource_label_success,
                      msg1.splitlines()[1].strip())
        self.assertIn(self.constant.TABLE_DROP_SUCCESS,
                      msg2.splitlines()[0].strip())
        self.assertTrue(msg2.count(self.constant.DROP_ROLE_SUCCESS_MSG) == 2)
        self.logger.info(
            '---Opengauss_Function_Security_Masking_Case0064 finish---')
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
Case Name   : 使用maskall方式脱密，存量数据和新增数据均被脱敏处理
Description :
    1.poladmin用户创建表，并赋予表的所有操作权限给用户1
    2.poladmin用户将敏感字段加到资源标签
    3.poladmin用户设置脱敏策略maskall,过滤用户1
    4.用户1连接数据库查看表的string字段是否脱敏
    5.表中插入新的的数据，查看存量数据和新增数据是否脱敏
Expect      :
    1.创表成功，赋权成功
    2.资源标签创建成功：CREATE RESOURCE LABEL
    3.脱敏策略添加成功
    4.查询到string字段的信息脱敏，所有的字符脱敏显示X
    5.查询到string字段的存量数据和新增数据均脱敏处理，所有的字符脱敏显示X
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        text = '---Opengauss_Function_Security_Masking_Case0055 start---'
        logger.info(text)
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.poladmin = 'poladmin_security_masking_0055'
        self.com_user = 'com_security_masking_0055'
        self.resource_label = 'rl_security_masking_0055'
        self.masking_policy = 'mp_security_masking_0055'
        self.table = f'{self.poladmin}.table_security_masking_0055'
    
    def test_masking(self):
        text = '---step1.1：创建poladmin及普通用户 expect:创建成功，权限赋予成功---'
        logger.info(text)
        sql_cmd1 = f'drop user if exists {self.poladmin};' \
            f'drop user if exists {self.com_user};' \
            f'create user {self.poladmin} with POLADMIN password \'' \
            f'{macro.COMMON_PASSWD}\';' \
            f'create user {self.com_user} with password \'' \
            f'{macro.COMMON_PASSWD}\';' \
            f'grant all privileges to {self.com_user};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"enable_security_policy=on"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        assert_1 = self.constant.CREATE_ROLE_SUCCESS_MSG in msg1
        assert_2 = self.constant.ALTER_ROLE_SUCCESS_MSG in msg1
        sql_cmd3 = f'show enable_security_policy;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'enable_security_policy', 'on',
                                  '(1 row)', flag='1')
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)
        text = '---step1.2：poladmin用户创建表 expect:创建表成功---'
        logger.info(text)
        sql_cmd4 = f'''drop table if exists {self.table};
                create table {self.table}(id int,name char(10),string
                varchar2(25),address varchar(60));
                insert into {self.table} values(1,'张三','22337203685477580',
                'Shanxi,Xian,yuhuazhai'),(2,'李四','13547676685489881',
                'Fujian');'''
        excute_cmd4 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.poladmin} -W' \
            f' {macro.COMMON_PASSWD} -c "{sql_cmd4}"'
        logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        logger.info(msg4)
        assert_1 = self.constant.CREATE_TABLE_SUCCESS in msg4
        assert_2 = self.constant.INSERT_SUCCESS_MSG in msg4
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)
        text = '---step2：poladmin用户将敏感字段加到资源标签,设置脱敏策略' \
               'maskall,过滤用户1 expect:添加成功，脱敏策略设置成功---'
        logger.info(text)
        sql_cmd5 = f'drop resource label if exists {self.resource_label};' \
            f'create resource label {self.resource_label} add column(' \
            f'{self.table}.string);' \
            f'drop masking policy if exists {self.masking_policy};' \
            f'create masking policy {self.masking_policy} ' \
            f'maskall on label({self.resource_label}) ' \
            f'filter on roles({self.com_user});'
        excute_cmd5 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.poladmin} -W' \
            f' {macro.COMMON_PASSWD} -c "{sql_cmd5}"'
        logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        logger.info(msg5)
        assert_1 = self.constant.resource_label_create_success_msg in msg5
        assert_2 = self.constant.masking_policy_create_success_msg in msg5
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)
        text = '---step3：登录用户1查看表的string字段脱敏 expect:脱敏成功---'
        logger.info(text)
        sql_cmd6 = f'select string from {self.table};'
        excute_cmd6 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.com_user} -W \'' \
            f'{macro.COMMON_PASSWD}\' -c "{sql_cmd6}"'
        logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        logger.info(msg6)
        msg6_list = msg6.splitlines()
        assert_1 = msg6_list[2].strip() == 'xxxxxxxxxxxxxxxxx' and \
                   msg6_list[3].strip() == 'xxxxxxxxxxxxxxxxx'
        self.assertTrue(assert_1, '执行失败:' + text)
        text = '---step4：表中插入新的的数据，查看存量数据和新增数据是否脱敏 ' \
               'expect:脱敏成功---'
        logger.info(text)
        sql_cmd7 = f'''insert into {self.table} values(1,'张三',
                '22337203685476680','Shanxi,Xian,yuhuazhai'),
                (2,'李四','21237123685476680','Fujian');'''
        msg7 = self.sh_primy.execut_db_sql(sql_cmd7)
        logger.info(msg7)
        logger.info(text)
        sql_cmd8 = f'select string from {self.table};'
        excute_cmd8 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.com_user} -W \'' \
            f'{macro.COMMON_PASSWD}\' -c "{sql_cmd8}"'
        logger.info(excute_cmd8)
        msg8 = self.userNode.sh(excute_cmd8).result()
        logger.info(msg8)
        msg8_list = msg8.splitlines()
        assert_1 = msg8_list[2].strip() == 'xxxxxxxxxxxxxxxxx' and \
                   msg8_list[3].strip() == 'xxxxxxxxxxxxxxxxx' and \
                   msg8_list[4].strip() == 'xxxxxxxxxxxxxxxxx' and \
                   msg8_list[5].strip() == 'xxxxxxxxxxxxxxxxx'
        self.assertTrue(assert_1, '执行失败:' + text)
    
    def tearDown(self):
        logger.info('-------清理资源------')
        sql_cmd1 = f'drop masking policy if exists {self.masking_policy};' \
            f'drop resource label if exists {self.resource_label};' \
            f'drop table if exists {self.table};'
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -c "{sql_cmd1}"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"enable_security_policy=off"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        sql_cmd3 = f'show enable_security_policy;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        sql_cmd4 = f'drop user {self.com_user};' \
            f'drop user {self.poladmin};'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        logger.info(
            '---Opengauss_Function_Security_Masking_Case0055 finish---')

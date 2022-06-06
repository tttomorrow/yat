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
Case Name   : 过滤条件为IP，查看数据脱敏成功
Description :
    1.poladmin用户创建表
    2.poladmin用户将敏感字段加到资源标签
    3.poladmin用户设置脱敏策略maskall,过率ip
    4.用户1连接数据库查看表的string字段是否脱敏
Expect      :
    1.创表成功
    2.资源标签创建成功：CREATE RESOURCE LABEL
    3.脱敏策略添加成功
    4.用户1查询到string字段的信息脱敏
History     :
"""
import os
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
        text = '---Opengauss_Function_Security_Masking_Case0059 start---'
        self.logger.info(text)
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.poladmin = 'poladmin_security_masking_0059'
        self.com_user = 'com_security_masking_0059'
        self.resource_label = 'rl_security_masking_0059'
        self.masking_policy = 'mp_security_masking_0059'
        self.table = f'{self.poladmin}.table_security_masking_0059'
        self.config = os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')
        self.confignew = os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba02.conf')
        self.logger.info('--------备份白名单文件---------')
        cp_cmd = f"cp {self.config} {self.confignew}"
        self.userNode.sh(cp_cmd).result()
    
    def test_masking(self):
        text = '---step1.1：创建poladmin及普通用户 expect:创建成功，权限赋予成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop user if exists {self.poladmin};' \
            f'drop user if exists {self.com_user};' \
            f'create user {self.poladmin} with POLADMIN password \'' \
            f'{macro.COMMON_PASSWD}\';' \
            f'create user {self.com_user} with password \'' \
            f'{macro.COMMON_PASSWD}\';' \
            f'grant all privileges to {self.com_user};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"enable_security_policy=on"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        assert_1 = self.constant.CREATE_ROLE_SUCCESS_MSG in msg1
        assert_2 = self.constant.ALTER_ROLE_SUCCESS_MSG in msg1
        sql_cmd3 = f'show enable_security_policy;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'enable_security_policy', 'on',
                                  '(1 row)', flag='1')
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)
        
        text = '---step1.2：poladmin用户创建表 expect:创表成功---'
        self.logger.info(text)
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
        self.logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        assert_1 = self.constant.CREATE_TABLE_SUCCESS in msg4
        assert_2 = self.constant.INSERT_SUCCESS_MSG in msg4
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)
        text = '---step1.3：修改白名单认证方式为sha256 expect:修改成功---'
        self.logger.info(text)
        sql_encryption = 'show password_encryption_type;'
        msg_encryption = self.sh_primy.execut_db_sql(sql_encryption)
        self.logger.info(msg_encryption)
        content_encryption = msg_encryption.splitlines()
        self.logger.info(content_encryption)
        exc_mag = ''
        if content_encryption[-2].strip() == '3':
            exc_mag = 'sm3'
        elif content_encryption[-2].strip() == '2':
            exc_mag = 'sha256'
        elif content_encryption[-2].strip() == '1':
            exc_mag = 'md5'
        guc_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -h ' \
            f'"host {self.userNode.db_name} {self.com_user} ' \
            f'{self.userNode.db_host}/32 {exc_mag}"'
        guc_msg = self.userNode.sh(guc_cmd).result()
        self.logger.info(guc_msg)
        text = '---step2-3：poladmin用户将敏感字段加到资源标签，设置脱敏策略' \
               'maskall，过滤IP expect:添加成功，脱敏策略设置成功---'
        self.logger.info(text)
        sql_cmd5 = f'drop resource label if exists {self.resource_label};' \
            f'create resource label {self.resource_label} add column(' \
            f'{self.table}.string);' \
            f'drop masking policy if exists {self.masking_policy};' \
            f'create masking policy {self.masking_policy} ' \
            f'maskall on label({self.resource_label}) ' \
            f'filter on IP(\'{self.userNode.db_host}\');'
        excute_cmd5 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.poladmin} -W' \
            f' {macro.COMMON_PASSWD} -c "{sql_cmd5}"'
        self.logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        assert_1 = self.constant.resource_label_create_success_msg in msg5
        assert_2 = self.constant.masking_policy_create_success_msg in msg5
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)
        text = '---step4：用户1-h连接数据库查看表的string字段脱敏 expect:脱敏成功---'
        self.logger.info(text)
        sql_cmd6 = f'select string from {self.table};'
        excute_cmd6 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.com_user} -W \'' \
            f'{macro.COMMON_PASSWD}\' -h {self.userNode.db_host} ' \
            f'-c "{sql_cmd6}"'
        self.logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        self.logger.info(msg6)
        msg6_list = msg6.splitlines()
        assert_1 = msg6_list[2].strip() == 'xxxxxxxxxxxxxxxxx' and \
                   msg6_list[3].strip() == 'xxxxxxxxxxxxxxxxx'
        self.assertTrue(assert_1, '执行失败:' + text)
    
    def tearDown(self):
        self.logger.info('-------恢复配置文件------')
        check_cmd = f'if [ -f {self.config} ];then mv {self.confignew} ' \
            f'{self.config};fi'
        self.logger.info(check_cmd)
        self.userNode.sh(check_cmd).result()
        restart_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary'
        restart_msg = self.userNode.sh(restart_cmd).result()
        self.logger.info(restart_msg)
        self.logger.info('-------清理资源------')
        sql_cmd1 = f'drop masking policy if exists {self.masking_policy};' \
            f'drop resource label if exists {self.resource_label};' \
            f'drop table if exists {self.table};'
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -c "{sql_cmd1}"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        excute_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"enable_security_policy=off"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        sql_cmd3 = f'show enable_security_policy;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        sql_cmd4 = f'drop user {self.com_user};' \
            f'drop user {self.poladmin};'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.logger.info(
            '---Opengauss_Function_Security_Masking_Case0059 finish---')

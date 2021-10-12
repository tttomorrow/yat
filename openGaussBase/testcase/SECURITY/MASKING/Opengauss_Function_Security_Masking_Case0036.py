"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : 对使用alldigitsmasking方式脱密的数据还原，查看数据还原成功
Description :
    1.poladmin用户创建表，并赋予表的所有操作权限给用户user001
    2.poladmin用户将敏感字段加到资源标签
    3.poladmin用户设置脱敏策略alldigitsmasking,过滤user001
    4.user001用户连接数据库查看person表email字段是否脱敏
    5.还原脱敏字段
    6.查看字段还原成功，查询出来的内容是否显示完整
Expect      :
    1.创表成功，赋权成功
    2.资源标签创建成功：CREATE RESOURCE LABEL
    3.脱敏策略设置失败
    4.email字段的信息已做脱敏处理
    5.person.email字段移除脱敏策略成功
    6.email字段还原成功，查询出来的内容显示完整
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_Masking_Case0036 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_masking(self):
        logger.info('--------创建用户--------')
        sql_cmd1 = f'create user poladmin with POLADMIN password \'' \
                   f'{macro.COMMON_PASSWD}\';' \
                   f'create user user001 with password \'' \
                   f'{macro.COMMON_PASSWD}\';grant all privileges to user001;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('--------开启安全策略开关--------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                      f'"enable_security_policy=on"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        sql_cmd3 = f'show enable_security_policy;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'enable_security_policy', 'on',
                                  '(1 row)', flag='1')
        logger.info('------创建表、资源标签、脱敏策略------')
        sql_cmd4 = '''create table public.person(id int,name char(10),email 
                varchar(25),address varchar(60));
                insert into person values(1,'张三','qaz9176@qq.com',
                'Shanxi,Xian,yuhuazhai'),(2,'李四','edc7896@qq.com',
                'Fujian');'''
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd4}"'
        logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        logger.info(msg4)
        self.assertTrue('CREATE TABLE' in msg4)
        sql_cmd5 = 'create resource label email_lable add column(' \
                   'public.person.email);' \
                   'create masking policy mask_card_pol alldigitsmasking ' \
                   'on label(email_lable) filter on roles(user001);'
        excute_cmd5 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U poladmin -W' \
                      f' {macro.COMMON_PASSWD} -c "{sql_cmd5}"'
        logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        logger.info(msg5)
        logger.info('------user001查看person表email字段脱敏------')
        sql_cmd6 = 'select email from public.person;'
        excute_cmd6 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user001 -W \'' \
                      f'{macro.COMMON_PASSWD}\' -c "{sql_cmd6}"'
        logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        logger.info(msg6)
        msg6_list = msg6.splitlines()
        self.assertTrue(msg6_list[2].strip() == 'qaz0000@qq.com' and
                        msg6_list[3].strip() == 'edc0000@qq.com')
        logger.info('---------还原脱敏字段----------')
        sql_cmd7 = 'drop masking policy mask_card_pol;'
        excute_cmd7 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U poladmin -W \'' \
                      f'{macro.COMMON_PASSWD}\' -c "{sql_cmd7}"'
        logger.info(excute_cmd7)
        msg7 = self.userNode.sh(excute_cmd7).result()
        logger.info(msg7)
        sql_cmd8 = 'select email from public.person;;'
        excute_cmd8 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user001 -W \'' \
                      f'{macro.COMMON_PASSWD}\' -c "{sql_cmd8}"'
        logger.info(excute_cmd8)
        msg8 = self.userNode.sh(excute_cmd8).result()
        logger.info(msg8)
        msg8_list = msg8.splitlines()
        self.assertTrue(msg8_list[2].strip() == 'qaz9176@qq.com' and
                        msg8_list[3].strip() == 'edc7896@qq.com')

    def tearDown(self):
        logger.info('-------清理资源------')
        sql_cmd1 = 'drop resource label email_lable;' \
                   'drop table person;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd1}"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertTrue(msg1.find('DROP TABLE') > -1)
        self.assertTrue(msg1.find('DROP RESOURCE LABEL') > -1)
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                      f'"enable_security_policy=off"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        sql_cmd3 = f'show enable_security_policy;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'enable_security_policy', 'off',
                                  '(1 row)', flag='1')
        sql_cmd4 = f'drop user user001;drop user poladmin;'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        self.assertTrue(msg4.count('DROP ROLE') == 2)
        logger.info(
            '---Opengauss_Function_Security_Masking_Case0036 finish---')
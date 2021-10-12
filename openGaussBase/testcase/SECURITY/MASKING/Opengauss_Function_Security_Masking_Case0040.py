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
Case Name   : 使用shufflemasking脱密策略，对邮箱格式的数据类型进行脱敏
Description :
    1.poladmin用户创建表，并赋予表的所有操作权限给用户user001
    2.poladmin用户将敏感字段加到资源标签
    3.poladmin用户设置脱敏策略shufflemasking,过滤user001
    4.user001用户查看数据是否脱敏
Expect      :
    1.创表成功，赋权成功
    2.资源标签创建成功：CREATE RESOURCE LABEL
    3.脱敏策略设置失败成功
    4.查看到string字段的文本内容均脱敏处理，原来的字符位置打乱顺序
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
        logger.info('---Opengauss_Function_Security_Masking_Case0040 start---')
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
                   f'{macro.COMMON_PASSWD}\';' \
                   f'grant all privileges to user001;'
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
        sql_cmd4 = '''create table public.person(id int,name char(10),string 
                varchar(25),address varchar(60));
                insert into person values(1,'张三','5855457@qq.com',
                'Shanxi,Xian,yuhuazhai'),(2,'李四','qazw345@163.com',
                'Fujian');'''
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd4}"'
        logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        logger.info(msg4)
        self.assertTrue('CREATE TABLE' in msg4)
        sql_cmd5 = 'create resource label string_lable add column(' \
                   'public.person.string);' \
                   'create masking policy mask_card_pol shufflemasking ' \
                   'on label(string_lable) filter on roles(user001);'
        excute_cmd5 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U poladmin -W' \
                      f' {macro.COMMON_PASSWD} -c "{sql_cmd5}"'
        logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        logger.info(msg5)
        logger.info('------user001查看person表string字段脱敏------')
        sql_cmd6 = 'select string from public.person;'
        excute_cmd6 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user001 -W \'' \
                      f'{macro.COMMON_PASSWD}\' -c "{sql_cmd6}"'
        logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        logger.info(msg6)
        msg6_list = msg6.splitlines()
        logger.info(msg6_list[2].count('-'))
        self.assertTrue(msg6_list[2].strip() != '5855457@qq.com' and
                        "@" in msg6_list[2])
        self.assertTrue(msg6_list[3].strip() != 'qazw345@163.com' and
                        "@" in msg6_list[2])

    def tearDown(self):
        logger.info('-------清理资源------')
        sql_cmd1 = 'drop masking policy mask_card_pol;' \
                   'drop resource label string_lable;' \
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
            '---Opengauss_Function_Security_Masking_Case0040 finish---')

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
Case Type   : security-auditing
Case Name   : 关闭数据库对象RESOURCE POOL的CREATE、DROP、ALTER操作审计功能
Description :
    1.设置参数"audit_system_object=511"；
    2.登录数据库，创建RESOURCE POOL对象;
    3.修改RESOURCE POOL对象；
    4.删除RESOURCE POOL对象;
    5.登录数据库，查看审计日志，时间设在最接近登录数据库的时间
Expect      :
    1.设置成功
    2.创建成功
    3.修改成功
    4.删除成功
    5.未查询到创建、修改、删除RESOURCE POOL的信息
History     :
"""
import re
import unittest
from time import sleep
from yat.test import Node
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '------Opengauss_Function_Security_Auditing_Case0052 start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.respol = 'respol_security_audit_0052'
        self.default_param = self.common.show_param('audit_system_object')
    
    def test_security(self):
        text = '---step1:设置参数audit_system_object=511;expect:成功---'
        self.logger.info(text)
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                                    f'audit_system_object=511')
        self.logger.info('------获取起始时间点-----')
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        self.logger.info(start_time)
        sleep(5)
        text = '---step2-4:创建、修改、删除RESOURCE POOL对象;expect:成功---'
        self.logger.info(text)
        exc_cmd1 = f'CREATE RESOURCE POOL {self.respol};' \
            f'ALTER RESOURCE POOL {self.respol} WITH ' \
            f'(CONTROL_GROUP=\'High\');' \
            f'DROP RESOURCE POOL {self.respol};'
        msg1 = self.sh_primy.execut_db_sql(exc_cmd1)
        self.logger.info(msg1)
        assert1 = re.search(
            r".*CREATE RESOURCE POOL.*ALTER RESOURCE POOL.*"
            r"DROP RESOURCE POOL.*",
            msg1, re.S)
        self.assertTrue(assert1, '执行失败:' + text)
        self.logger.info('------获取终止时间点-----')
        sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd2 = f'select * from pg_query_audit(\'{start_time}\',\
                   \'{end_time}\');'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        assert2 = re.search(
            r".*CREATE RESOURCE POOL.*ALTER RESOURCE POOL.*"
            r"DROP RESOURCE POOL.*",
            msg2, re.S)
        self.assertFalse(assert2, '执行失败:' + text)
    
    def tearDown(self):
        self.logger.info('----恢复配置----')
        rev_msg = self.sh_primy.execute_gsguc('reload',
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f'audit_system_object={self.default_param}')
        self.logger.info(rev_msg)
        check_msg = self.sh_primy.execut_db_sql('show audit_system_object;')
        self.logger.info(check_msg)
        self.common.equal_sql_mdg(check_msg, 'audit_system_object',
                                  f'{self.default_param}', '(1 row)', flag='1')
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0052 end-----')

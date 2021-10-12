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
Case Type   : GUC_ErrorLog
Case Name   : 参数client_min_messages的值设置设为2min，24h
Description :
    1.修改参数client_min_messages的值为error：gs_guc reload -N all -I all -c
    "client_min_messages=error"
    2.查看修改后的参数：show client_min_messages;
    3.执行正确语句：drop table if exists table001;
Expect      :
    1.修改成功
    2.返回值：error
    3.返回信息：DROP TABLE,无返回notice信息
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Errorlog(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0057 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_errorlog(self):
        self.logger.info('----------查看client_min_messages默认值----------')
        sql_cmd0 = 'show client_min_messages;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'client_min_messages', 'notice',
                                '(1 row)', flag='1')
        self.logger.info('--------设置参数client_min_messages值为error-------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"client_min_messages=error"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('----------查看client_min_messages修改后的值----------')
        sql_cmd2 = 'show client_min_messages;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'client_min_messages', 'error',
                                '(1 row)', flag='1')
        sql_cmd3 = 'drop table if exists table001;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue("NOTICE:" not in msg3 and "DROP TABLE" in msg3)

    def tearDown(self):
        self.logger.info('--------------恢复配置----------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -N all -I all -c ' \
                      f'"client_min_messages=notice"'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-------查看 client_min_messages修改后的值--------')
        sql_cmd2 = 'show client_min_messages;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'client_min_messages', 'notice',
                                '(1 row)', flag='1')
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0057 finish--')

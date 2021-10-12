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
Case Name   : 查看参数client_min_messages的默认值为notice
Description :
    1.查看参数client_min_messages默认值：show client_min_messages;
    2.连接数据库，输入错误语句：drop table if exist table001;
Expect      :
    1.返回值：notice
    2.返回报错信息：ERROR:  syntax error at or near "exist"
History     :
"""
import os
import unittest
from time import sleep

from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        Logger.info('----Opengauss_Function_Guc_ErrorLog_Case0053 start----')
        self.userNode = Node('PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')

    def test_errorlog(self):
        Logger.info('------查看client_min_messages默认值------')
        sql_cmd1 = 'show client_min_messages;'
        sql_msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        Logger.info(sql_msg1)
        self.common.equal_sql_mdg(sql_msg1, 'client_min_messages', 'notice',
                                  '(1 row)', flag='1')
        Logger.info('------查看执行sql语句，查看客户端返回日志是否notice------')
        sql_cmd2 = 'drop table if exists table001;'
        sql_msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        Logger.info(sql_msg2)
        self.assertTrue('NOTICE:  table "table001" does not exist, skipping'
                        in sql_msg2)

    def tearDown(self):
        Logger.info('--Opengauss_Function_Guc_ErrorLog_Case0053 finish--')

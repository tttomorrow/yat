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
Case Type   : GUC
Case Name   : 使用alter database方法设置参数TimeZone为Australia/South,
              观察预期结果
Description :
        1.查询TimeZone默认值
        2.创建数据库
        3.修改参数值为Australia/South并查询当前时间
        4.删除数据库
Expect      :
        1.显示默认值PRC
        2.数据库创建成功
        3.设置成功当前时间为北京时间
        4.删除成功
"""
import time
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0126start------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')

    def test_TimeZone(self):
        self.log.info('查询默认值')
        sql_cmd = self.commonsh.execut_db_sql('''show TimeZone;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('创建数据库')
        sql_cmd = self.commonsh.execut_db_sql('''drop database if exists 
            test_spdb132;
            create database test_spdb132;''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        self.log.info('修改数据库级别参数')
        sql_cmd = self.commonsh.execut_db_sql('''alter database 
            test_spdb132 set TimeZone to 'Australia/South';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd)
        time.sleep(3)
        self.log.info('连接数据库查询')
        sql_cmd = '''show TimeZone;
                     select now();'''
        excute_cmd = f'''
                        source {macro.DB_ENV_PATH};
                        gsql -d test_spdb132 -p {self.userNode.db_port} \
                        -c "{sql_cmd}"'''
        self.log.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.log.info(msg)
        self.assertIn('Australia/South', msg)
        self.assertIn('+09:30', msg)

    def tearDown(self):
        self.log.info('----------------恢复默认值----------------------')
        sql_cmd = self.commonsh.execut_db_sql('''drop database if exists 
            test_spdb132;''')
        self.log.info(sql_cmd)
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0126执行完成---')

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
Case Type   : GUC
Case Name   : 使用alter database方法设置参数TimeZone为Australia/South,
              观察预期结果
Description :
        1.查询TimeZone默认值
        2.创建数据库
        3.修改参数值为Australia/South
        4.查询当前时间
        5.清理环境
Expect      :
        1.显示默认值PRC
        2.数据库创建成功
        3.设置成功
        4.时区修改成功，和系统表pg_timezone_names相对于UTC的偏移量一致
        5.清理环境完成
             故Australia/South时区的偏移量会变化
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
            '----Opengauss_Function_Guc_ClientConnection_Case0132start------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.db_name = "db_guc_clientconnection_case0132"

    def test_TimeZone(self):
        text = '--步骤1:查看默认值;expect:默认值为PRC--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql('''show TimeZone;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        text = '--步骤2:创建数据库;expect:创建成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists 
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        text = '--步骤3:修改数据库级别参数;expect:修改成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'''alter database 
            {self.db_name} set TimeZone to 'Australia/South';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.ALTER_DATABASE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        time.sleep(3)
        text = '--步骤4:连接数据库查询;expect:时区修改成功，和系统表' \
               'pg_timezone_names相对于UTC的偏移量一致--'
        self.log.info(text)
        sql_cmd = '''show TimeZone;'''
        self.log.info(sql_cmd)
        result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                             dbname=f'{self.db_name}')
        self.log.info(result)
        self.assertIn('Australia/South', result, '执行失败:' + text)
        sql_cmd = '''select now();'''
        self.log.info(sql_cmd)
        result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                             dbname=f'{self.db_name}')
        self.log.info(result)
        msg1 = result.splitlines()[-2].strip()
        self.log.info(msg1)
        res1 = msg1.split('+')[-1]
        self.log.info(res1)
        sql_cmd = f'''select * from  \
            pg_timezone_names where name= 'Australia/South';'''
        result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                             dbname=f'{self.db_name}')
        self.log.info(result)
        msg2 = result.splitlines()[-2].strip()
        self.log.info(msg2)
        res2 = msg2.split('|')[-2].strip().replace(':00', '')
        self.log.info(res2)
        self.assertEqual(res1, res2, '执行失败:' + text)

    def tearDown(self):
        text = '--步骤5:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists 
            {self.db_name};''')
        self.log.info(sql_cmd)
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0132执行完成---')

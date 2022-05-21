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
Case Name   : 使用alter database方法设置参数temp_tablespaces为不存在的表空间
              名称,合理报错
Description :
        1.查询temp_tablespaces默认值
        2.创建数据库
        3.修改参数值为不存在名称
        4.删除数据库
Expect      :
        1.显示默认值为空
        2.数据库创建成功
        3.合理报错
        4.删除成功
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0040start--')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.db_name = "db_guc_clientconnection_case0040"

    def test_temp_tablespaces(self):
        text = '--step1:查看默认值;expect:默认值为空--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'''show temp_tablespaces;''')
        self.log.info(sql_cmd)
        self.assertEqual('', sql_cmd.splitlines()[-2].strip(),
                         '执行失败:' + text)
        text = '--step2:创建数据库;expect:创建成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists \
            {self.db_name} ;
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        text = 'step3:使用alter database设置temp_tablespaces为' \
               '不存在的t_temp_tablespaces040;expect:设置成功'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'''alter database \
            {self.db_name} set temp_tablespaces to 't_temp_tablespaces040';''')
        self.log.info(sql_cmd)
        self.assertIn(
            'NOTICE:  tablespace "t_temp_tablespaces040" does not exist',
            sql_cmd)
        sql_cmd = '''show temp_tablespaces;'''
        result = self.commonsh.execut_db_sql(sql=sql_cmd,
                                             dbname=f'{self.db_name}')
        self.log.info(result)
        self.assertIn('t_temp_tablespaces040', result, '执行失败:' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'''drop database if exists \
            {self.db_name};''')
        self.log.info(sql_cmd)
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0040执行完成--')

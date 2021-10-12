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
Case Name   : 设置temp_tablespaces为多个表空间名称，事务中，连续创建临时对象
Description :
        1.查询temp_tablespaces默认值
        2.创建表空间
        3.开启事务并创建临时表
        4.查询临时表的表空间后结束事务
        5.恢复参数值为空并删除表和表空间
Expect      :
        1.显示默认值为空
        2.创建成功
        3.开启事务成功且创建临时表成功
        4.临时表的表空间在列表里连续的表空间中
        5.恢复默认值成功，删除成功
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-----------Opengauss_Function_Guc_ClientConnection_Case0045start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_temp_tablespaces(self):

        # 查询默认值
        sql_cmd = self.commonsh.execut_db_sql(f'''show temp_tablespaces;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 创建表空间
        sql_cmd = self.commonsh.execut_db_sql('''drop tablespace if exists t_tablespace045;
        create tablespace t_tablespace045 relative location 'tablespace/tablespace_15';
        drop tablespace if exists t_tablespace045_bak;
        create tablespace t_tablespace045_bak relative location 'tablespace/tablespace_16';''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.TABLESPCE_CREATE_SUCCESS, sql_cmd)
        # 开启事务;创建临时表并查询表空间(列表里连续的表空间中))
        sql_cmd = self.commonsh.execut_db_sql('''set temp_tablespaces to t_tablespace045,t_tablespace045_bak;
        start transaction;
        drop table if exists test_search_path045;
        create temp table test_search_path045(i int);
        drop table if exists test_search_path045_bak;
        create temp table test_search_path045_bak(i int);
        select tablename ,tablespace from pg_tables where tablename = 'test_search_path045';
        select tablename ,tablespace from pg_tables where tablename = 'test_search_path045_bak';
        end;''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.SET_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn('t_tablespace045', sql_cmd)
        self.assertIn(self.Constant.COMMIT_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        self.log.info('----------------清理环境-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''set default_tablespace to '';
        drop table if exists test_search_path045;
        drop table if exists test_search_path045_bak;
        drop tablespace if exists t_tablespace045;
        drop tablespace if exists t_tablespace045_bak;''')
        self.log.info(sql_cmd)
        self.log.info('--------------Opengauss_Function_Guc_ClientConnection_Case0045执行完成---------------')

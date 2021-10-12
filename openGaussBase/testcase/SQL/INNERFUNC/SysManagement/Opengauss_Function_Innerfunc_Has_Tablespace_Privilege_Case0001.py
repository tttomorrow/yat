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
Case Type   : 功能测试
Case Name   : has_tablespace_privilege(tablespace, privilege)当前用户是否有访问表空间的权限
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除用户和表空间防止新建失败，新建用户和表并对该表空间进行赋权限
    步骤 3.切换到新建的用户执行SELECT has_tablespace_privilege(tablespace, privilege);判断新建用户是否有表空间的权限
Expect      :
    步骤 1：数据库状态正常
    步骤 2：环境清理成功，赋权成功
    步骤 3：返回结果正确
History     :
"""

import unittest
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH


logger = Logger()
common = Common()
commonsh = CommonSH('dbuser')

class Has_table_privilege(unittest.TestCase):


    def setUp(self):
        logger.info("-----------Opengauss_Function_Innerfunc_Has_Tablespace_Privilege_Case0001开始执行---------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()
    def test_has_table_privilege(self):
        sql_cmd = f'''drop user if exists joe CASCADE;
                    drop TABLESPACE if exists tpcds_tbspc;
                    CREATE TABLESPACE tpcds_tbspc RELATIVE LOCATION 'tablespace/tablespace_1';
                    CREATE USER joe password '{macro.COMMON_PASSWD}';
                    GRANT CREATE  ON TABLESPACE tpcds_tbspc TO joe;
            '''
        SqlMdg = commonsh.execut_db_sql(sql_cmd)
        logger.info(SqlMdg)

        endowed_SqlMdg = commonsh.execut_db_sql(
            "SELECT has_tablespace_privilege('joe','tpcds_tbspc', 'CREATE');")
        logger.info(endowed_SqlMdg)
        common.equal_sql_mdg(endowed_SqlMdg, 'has_tablespace_privilege', 't', '(1 row)', flag='1')

        SqlMdg = commonsh.execut_db_sql('REVOKE ALL PRIVILEGES ON TABLESPACE tpcds_tbspc FROM joe;')
        logger.info(SqlMdg)

        unowed_SqlMdg = commonsh.execut_db_sql(
            "SELECT has_tablespace_privilege('joe','tpcds_tbspc','CREATE');")
        logger.info(unowed_SqlMdg)
        common.equal_sql_mdg(unowed_SqlMdg, 'has_tablespace_privilege', 'f', '(1 row)', flag='1')

    def tearDown(self):
        clear_sql = 'DROP USER IF EXISTS joe CASCADE;drop TABLESPACE if exists tpcds_tbspc;'
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info('----------Opengauss_Function_Innerfunc_Has_Tablespace_Privilege_Case0001执行结束------------')
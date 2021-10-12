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
Case Name   : has_database_privilege(db, privilege)当前用户是否有访问数据库的权限
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除用户和数据库防止新建失败，新建用户和数据库并对该数据库进行赋权限
    步骤 3.切换到新建的用户执行SELECT has_database_privilege(db, privilege);privilege权限存在和不存在时返回值校验
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
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()
common = Common()
commonsh = CommonSH('dbuser')
constant = Constant()


class Has_database_privilege(unittest.TestCase):

    def setUp(self):
        logger.info("----------Opengauss_Function_Innerfunc_Has_Database_Privilege_Case0001开始执行-------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_has_database_privilege(self):
        sql_cmd = f'''drop user if exists joe CASCADE;
                    CREATE USER joe password '{macro.COMMON_PASSWD}';
                    DROP database IF EXISTS dbtest_001;
                    create database dbtest_001; 
                    GRANT connect on database dbtest_001 TO joe ;
            '''
        SqlMdg = commonsh.execut_db_sql(sql_cmd)
        logger.info(SqlMdg)

        endowed_SqlMdg = commonsh.execut_db_sql(
            "SELECT has_database_privilege('joe','dbtest_001' ,'connect');")
        logger.info(endowed_SqlMdg)
        common.equal_sql_mdg(endowed_SqlMdg, 'has_database_privilege', 't', '(1 row)', flag='1')

        endowed_SqlMdg = commonsh.execut_db_sql(
            "SELECT has_database_privilege('joe','dbtest_001' ,'create');")
        logger.info(endowed_SqlMdg)
        common.equal_sql_mdg(endowed_SqlMdg, 'has_database_privilege', 'f', '(1 row)', flag='1')


    def tearDown(self):
        clear_sql = 'DROP USER IF EXISTS joe CASCADE;DROP database IF EXISTS dbtest_001;'
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info('--------Opengauss_Function_Innerfunc_Has_Database_Privilege_Case0001执行结束------------')

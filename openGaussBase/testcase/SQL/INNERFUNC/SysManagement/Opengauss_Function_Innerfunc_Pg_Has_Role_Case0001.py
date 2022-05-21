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
Case Type   : 功能测试
Case Name   : pg_has_role(role, privilege)当前用户是否具有角色权限
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除用户和角色防止新建失败，新建用户和角色并对把该角色赋予用户
    步骤 3.切换到新建的用户执行SELECT pg_has_role(role, privilege);判断用户是否具有该角色权限
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


class Pg_has_role(unittest.TestCase):

    def setUp(self):
        logger.info("---------------Opengauss_Function_Innerfunc_Pg_Has_Role_Case0001开始执行-------------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_pg_has_role(self):
        sql_cmd = f'''drop user if exists senior_manager CASCADE;
                    DROP ROLE IF EXISTS manager;
                    CREATE ROLE manager IDENTIFIED BY 'Bigdata@123';
                    CREATE USER senior_manager password '{macro.COMMON_PASSWD}';
                    GRANT manager TO senior_manager;
                    select pg_has_role('senior_manager', 'manager', 'USAGE');
            '''
        SqlMdg = commonsh.execut_db_sql(sql_cmd)

        endowed_SqlMdg = commonsh.execut_db_sql("select pg_has_role('manager', 'USAGE');", f"-U senior_manager -W '{macro.COMMON_PASSWD}'")
        logger.info(endowed_SqlMdg)
        common.equal_sql_mdg(endowed_SqlMdg, 'pg_has_role', '-------------', 't', '(1 row)')

        SqlMdg = commonsh.execut_db_sql('REVOKE manager FROM senior_manager;')

        unowed_SqlMdg = commonsh.execut_db_sql("select pg_has_role('manager', 'USAGE');", f"-U senior_manager -W '{macro.COMMON_PASSWD}'")
        logger.info(unowed_SqlMdg)
        common.equal_sql_mdg(unowed_SqlMdg, 'pg_has_role', '-------------', 'f', '(1 row)')

    def tearDown(self):
        clear_sql = 'DROP ROLE IF EXISTS manager;DROP USER IF EXISTS senior_manager CASCADE;'
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info('----------Opengauss_Function_Innerfunc_Pg_Has_Role_Case0001执行结束--------------------------')

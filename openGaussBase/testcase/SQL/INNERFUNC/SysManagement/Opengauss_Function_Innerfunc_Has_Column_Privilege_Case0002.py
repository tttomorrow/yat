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
Case Name   : has_column_privilege(userid,table, privilege)函数查询用户参数为oid时是否有访问表中特定行的权限
Description : ceiling(dp or numeric)描述：不小于参数的最小整数（ceil的别名）。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除用户和表防止新建失败，新建用户和表并对该表进行赋权限
    步骤 3.重启数据库执行SELECT has_column_privilege(table, privilege);判断新建用户是否有表中特定行权限
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


class Has_column_privilege_002(unittest.TestCase):

    def setUp(self):
        logger.info("---------Opengauss_Function_Innerfunc_Has_Column_Privilege_Case0002开始执行------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_has_column_privilege(self):
        sql_cmd = f'''drop user if exists joe CASCADE;
                    CREATE USER joe password '{macro.COMMON_PASSWD}';
                    DROP table IF EXISTS table_test001;
                    create table table_test001(c int,d int); 
                    GRANT select (c),update (d) ON table_test001 TO joe;
                    SELECT has_column_privilege('joe', 'table_test001','c' ,'select');
            '''
        SqlMdg = commonsh.execut_db_sql(sql_cmd)

        restartMsg = commonsh.restart_db_cluster('success')

        endowed_SqlMdg = commonsh.execut_db_sql(
            "SELECT has_column_privilege(userid, 'table_test001','c' ,'select') from GS_WLM_USER_INFO where username = 'joe';")
        logger.info(endowed_SqlMdg)
        common.equal_sql_mdg(endowed_SqlMdg, 'has_column_privilege', '----------------------', 't', '(1 row)')

        unowed_SqlMdg = commonsh.execut_db_sql(
            "SELECT has_column_privilege(userid,'table_test001','c' ,'insert') from GS_WLM_USER_INFO where username = 'joe';")
        logger.info(unowed_SqlMdg)
        common.equal_sql_mdg(unowed_SqlMdg, 'has_column_privilege', '----------------------', 'f', '(1 row)')

    def tearDown(self):
        clear_sql = 'DROP USER IF EXISTS joe CASCADE;DROP table IF EXISTS table_test001;'
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info('------------Opengauss_Function_Innerfunc_Has_Column_Privilege_Case0002执行结束------------')

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
Case Name   : has_schema_privilege(userid,schema, privilege)函数，在用户参数为用户oid时有权限和无权限返回值校验
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除用户和模式防止新建失败，新建用户和表并对该模式进行赋权限
    步骤 3.重启数据库执行SELECT has_schema_privilege(userid,schema, privilege);判断新建用户是否有模式的权限
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


class Has_schema_privilege_002(unittest.TestCase):

    def setUp(self):
        logger.info("-----------Opengauss_Function_Innerfunc_Has_Schema_Privilege_Case0002开始执行-----------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_has_schema_privilege_002(self):
        sql_cmd = f'''drop user if exists joe CASCADE;
                    CREATE USER joe password '{macro.COMMON_PASSWD}';
                    DROP SCHEMA IF EXISTS schema_test001;
                    create SCHEMA schema_test001; 
                    GRANT USAGE ON SCHEMA schema_test001 TO joe;
                    SELECT has_schema_privilege('joe', 'schema_test001','USAGE');
            '''
        SqlMdg = commonsh.execut_db_sql(sql_cmd)
        restartMsg = commonsh.restart_db_cluster('success')

        endowed_SqlMdg = commonsh.execut_db_sql(
            "SELECT has_schema_privilege(userid,'schema_test001','USAGE') from GS_WLM_USER_INFO where username = 'joe';")
        logger.info(endowed_SqlMdg)
        common.equal_sql_mdg(endowed_SqlMdg, 'has_schema_privilege', '----------------------', 't', '(1 row)')

        unowed_SqlMdg = commonsh.execut_db_sql(
            "SELECT has_schema_privilege(userid,'schema_test001','CREATE')from GS_WLM_USER_INFO where username = 'joe';")
        logger.info(unowed_SqlMdg)
        common.equal_sql_mdg(unowed_SqlMdg, 'has_schema_privilege', '----------------------', 'f', '(1 row)')

    def tearDown(self):
        clear_sql = 'DROP USER IF EXISTS joe CASCADE;drop DROP SCHEMA IF EXISTS schema_test001;'
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info('---------Opengauss_Function_Innerfunc_Has_Schema_Privilege_Case0002执行结束----------------')

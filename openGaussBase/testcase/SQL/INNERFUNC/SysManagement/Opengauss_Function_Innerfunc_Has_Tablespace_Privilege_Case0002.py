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
Case Name   : has_tablespace_privilege(userid,tablespace, privilege)用户参数为用户oid时有权限和无权限时返回参数值校验
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境删除用户和表空间防止新建失败，新建用户和表并对该表空间进行赋权限
    步骤 3.重启执行SELECT has_tablespace_privilege(userid,tablespace, privilege);判断新建用户是否有表空间的权限
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


class Has_table_privilege_002(unittest.TestCase):

    def setUp(self):
        logger.info("----------Opengauss_Function_Innerfunc_Has_Tablespace_Privilege_Case0002开始执行----------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh = CommonSH('dbuser')
        self.common = Common()
        self.commonsh.ensure_dbstatus_normal()

    def test_has_table_privilege_002(self):
        sql_cmd = f'''drop user if exists joe CASCADE;
                    drop TABLESPACE if exists tpcds_tbspc;
                    CREATE TABLESPACE tpcds_tbspc RELATIVE LOCATION 'tablespace/tablespace_1';
                    CREATE USER joe password '{macro.COMMON_PASSWD}';
                    GRANT CREATE  ON TABLESPACE tpcds_tbspc TO joe;
                    select has_tablespace_privilege ('joe', 'tpcds_tbspc', 'CREATE');
            '''
        self.commonsh.execut_db_sql(sql_cmd)
        self.commonsh.restart_db_cluster('success')

        endowed_SqlMdg = self.commonsh.execut_db_sql(
            "select has_tablespace_privilege(userid,'tpcds_tbspc', 'CREATE') from GS_WLM_USER_INFO where username = 'joe';")
        logger.info(endowed_SqlMdg)
        self.common.equal_sql_mdg(endowed_SqlMdg, 'has_tablespace_privilege', '--------------------------', 't', '(1 row)')

        SqlMdg = self.commonsh.execut_db_sql('REVOKE ALL PRIVILEGES ON TABLESPACE tpcds_tbspc FROM joe;')
        logger.info(SqlMdg)

        unowed_SqlMdg = self.commonsh.execut_db_sql(
            "select has_tablespace_privilege(userid,'tpcds_tbspc', 'CREATE') from GS_WLM_USER_INFO where username = 'joe';")
        logger.info(unowed_SqlMdg)
        self.common.equal_sql_mdg(unowed_SqlMdg, 'has_tablespace_privilege', '--------------------------', 'f', '(1 row)')

    def tearDown(self):
        clear_sql = 'DROP USER IF EXISTS joe CASCADE;drop TABLESPACE if exists tpcds_tbspc;'
        self.commonsh.execut_db_sql(clear_sql)
        logger.info('-------Opengauss_Function_Innerfunc_Has_Tablespace_Privilege_Case0002执行结束------------')

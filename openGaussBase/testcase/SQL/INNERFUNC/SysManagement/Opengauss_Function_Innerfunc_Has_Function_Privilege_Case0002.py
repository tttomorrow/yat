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
Case Name   : has_function_privilege(userid,oid, privilege)用户oid 方法oid 查询是否有访问一个方法的权限
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.切换到新建的用户执行SELECT has_function_privilege(userid,oid, privilege);查看当前用户是否具有该权限
Expect      :
    步骤 1：数据库状态正常
    步骤 2：返回结果正确
History     :
"""

from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
import unittest
import sys

sys.path.append(sys.path[0] + "/../")

commonsh = CommonSH('dbuser')
common = Common()
logger = Logger()


class Has_function_privilege_002(unittest.TestCase):

    def setUp(self):
        logger.info(
            "-----Opengauss_Function_Innerfunc_Has_Function_Privilege_Case0002开始执行-------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_has_function_privilege_002(self):
        SqlMdg_oid = commonsh.execut_db_sql(
            "select oid from PG_PROC where  proname = 'age';").splitlines()[2].strip()
        logger.info(SqlMdg_oid)

        SqlMsg_userid = commonsh.execut_db_sql(
            f"select userid from GS_WLM_USER_INFO where username = '{commonsh.node.db_user}';").splitlines()[2].strip()
        logger.info(SqlMsg_userid)

        endowed_SqlMdg = commonsh.execut_db_sql(
            f"select has_function_privilege({SqlMsg_userid},{SqlMdg_oid} ,'EXECUTE');")

        logger.info(endowed_SqlMdg)
        common.equal_sql_mdg(endowed_SqlMdg, 'has_function_privilege',
                           '------------------------', 't', '(1 row)')

    def tearDown(self):
        logger.info(
            '----------Opengauss_Function_Innerfunc_Has_Function_Privilege_Case0002执行结束-----------')

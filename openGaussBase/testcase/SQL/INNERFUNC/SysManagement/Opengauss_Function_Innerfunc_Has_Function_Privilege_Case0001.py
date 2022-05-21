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
Case Name   : has_function_privilege(function, privilege)当前用户是否有访问一个方法的权限
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.清理环境自定义方法防止新建失败，新建用户和表并对该表进行赋权限
    步骤 3.切换到新建的用户执行SELECT has_function_privilege(function, privilege);查看当前用户是否具有该权限
Expect      :
    步骤 1：数据库状态正常
    步骤 2：环境清理成功，赋权成功
    步骤 3：返回结果正确
History     :
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

commonsh = CommonSH('dbuser')
common = Common()
logger = Logger()


class Has_function_privilege(unittest.TestCase):

    def setUp(self):
        logger.info("-----------Opengauss_Function_Innerfunc_Has_Function_Privilege_Case0001开始执行---------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_has_function_privilege(self):
        func_sql = '''
                    DROP FUNCTION IF EXISTS func_add_sql2;
                    CREATE FUNCTION func_add_sql2(num1 integer, num2 integer) RETURN integer
                    AS
                    BEGIN 
                    RETURN num1 + num2;
                    END;
                    '''
        SqlMdg = commonsh.execut_db_sql(func_sql)
        logger.info(SqlMdg)
        self.assertIn('CREATE FUNCTION', SqlMdg)

        endowed_SqlMdg = commonsh.execut_db_sql(
            "select has_function_privilege('func_add_sql2(integer, integer)','EXECUTE');")
        logger.info(endowed_SqlMdg)
        common.equal_sql_mdg(endowed_SqlMdg, 'has_function_privilege', '------------------------', 't', '(1 row)')

    def tearDown(self):
        clear_sql = 'DROP FUNCTION IF EXISTS func_add_sql2;'
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info('----------Opengauss_Function_Innerfunc_Has_Function_Privilege_Case0001执行结束--------------')

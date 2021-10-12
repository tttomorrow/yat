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
Case Name   : 系统管理员使用alter user命令设置synchronous_commit参数值为-2,合理报错
Description :
        1.查询synchronous_commit默认值
        2.创建用户
        3.系统管理员使用alter user命令修改参数为-2
        4.删除用户
Expect      :
        1.显示默认值为off
        2.创建成功
        3.合理报错
        4.删除成功
History     :
"""
import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class GUC_SC(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------------------------Opengauss_Function_Guc_Synchronous_Commit_Case0008开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_synchronous_commit(self):
        # 查看参数默认值(off)且创建系统管理员
        sql_cmd1 = commonsh.execut_db_sql(f'''show synchronous_commit;
                                       drop user if exists test1_sys008 cascade;
                                       create user test1_sys008 with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.res = sql_cmd1.splitlines()[-2].strip()
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        # 系统管理员使用alter user命令修改参数为-2；
        sql_cmd2 = ('''alter user test1_sys008 set synchronous_commit to -2;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test1_sys008 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  invalid value for parameter "synchronous_commit": "-2"', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除用户
        sql_cmd3 = commonsh.execut_db_sql('''drop user test1_sys008 cascade;''')
        logger.info(sql_cmd3)
        logger.info(
            '------------------------Opengauss_Function_Guc_Synchronous_Commit_Case0008执行结束--------------------------')

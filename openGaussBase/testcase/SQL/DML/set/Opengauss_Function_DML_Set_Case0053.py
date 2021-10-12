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
Case Type   : 系统操作
Case Name   : checkpoint权限测试,普通用户执行checkpoint，合理报错
Description :
        1.创建系统管理员
        2.调用checkpoint
        3.创建普通用户
        4.调用checkpoint
        5.清理环境
Expect      :
        1.创建系统管理员成功
        2.执行成功
        3.创建普通用户成功
        4.合理报错
        5.清理环境完成
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0053开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_checkpoint(self):
        # 创建系统管理员
        sql_cmd1 = commonsh.execut_db_sql(f'''drop user if exists t_sys cascade;
        create user t_sys with sysadmin password '{macro.COMMON_PASSWD}'; ''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        # 调用checkpoint
        sql_cmd2 = '''checkpoint;'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U t_sys -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.CHECKPOINT_SUCCESS_MSG, msg1)
        # 创建普通用户
        sql_cmd3 = commonsh.execut_db_sql(f'''drop user if exists test1_common cascade;
        create user test1_common password '{macro.COMMON_PASSWD}'; ''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd3)
        # 调用checkpoint
        sql_cmd4 = '''checkpoint;'''
        excute_cmd1 = f'''
                                    source {self.DB_ENV_PATH};
                                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test1_common -W '{macro.COMMON_PASSWD}' -c "{sql_cmd4}"
                                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  must be system admin to do CHECKPOINT', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除用户
        sql_cmd5 = commonsh.execut_db_sql(f'''drop user if exists t_sys cascade;
        drop user if exists test1_common cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0053执行结束--------------------------')

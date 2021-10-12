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
Case Type   : 用户-权限测试
Case Name   : 初始用户创建目录对象
Description :
    1.初始用户创建目录对象
    2.通过系统表查看目录信息
    3.删除目录
Expect      :
    1.创建成功
    2.查看成功
    3.删除成功
History     :
"""
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info(
            '---Opengauss_Function_DDL_Create_Directory_Case0001开始执行----')
        self.user_node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('dbuser')

    def test_common_user_permission(self):
        # 初始用户创建目录对象
        sql_cmd1 = '''DROP DIRECTORY if exists test_dir;
                    create DIRECTORY test_dir as '/tmp/';'''
        excute_cmd1 = f'''
               source {self.DB_ENV_PATH};
               gsql -d {self.user_node.db_name} -p {self.user_node.db_port} \
-U {self.user_node.ssh_user} -c "{sql_cmd1}"
            '''
        logger.info(excute_cmd1)
        msg1 = self.user_node.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.CREATE_DIRECTORY_SUCCESS_MSG, msg1)
        # 通过系统表查看目录信息
        sql_cmd2 = commonsh.execut_db_sql('''
        select dirname,dirpath from PG_DIRECTORY where dirname = 'test_dir';
        ''')
        logger.info(sql_cmd2)
        self.assertIn('test_dir', sql_cmd2)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''DROP DIRECTORY test_dir;''')
        logger.info(sql_cmd3)
        logger.info(
            '--Opengauss_Function_DDL_Create_Directory_Case0001执行结束----')

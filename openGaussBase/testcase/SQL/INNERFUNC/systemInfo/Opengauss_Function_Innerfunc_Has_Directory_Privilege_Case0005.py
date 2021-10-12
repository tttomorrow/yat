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
Case Name   : 创建路径赋权限之后切换用户查询权限
Description :
    1. 创建用户，赋予权限
    2. 切换到用户，使用has_directory_privilege函数查询被赋予以及未赋予的权限
    3. 删除用户及路径
Expect      :
    1. 创建成功，赋权成功
    2. 切换成功，只具有被赋予过的权限
    3. 删除成功
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')
        self.pwd = macro.COMMON_PASSWD
        self.env = macro.DB_ENV_PATH
        self.log.info('''---
        Opengauss_Function_Innerfunc_Has_Directory_Privilege_Case0005开始---''')

    def test_privilege(self):
        self.log.info('''----------------创建用户及目录------------------''')
        cmd0 = f"""drop user if exists hong;
                   drop directory if exists dir;
                   create user hong password '{self.pwd}';
                   create or replace directory dir as '/tmp/';"""
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('CREATE ROLE') > -1)
        self.assertTrue(msg0.find('CREATE DIRECTORY') > -1)

        self.log.info('''-----------将directory对象的读权限赋予用户-----------''')
        cmd1 = """grant read on directory dir to hong;"""
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue('GRANT' in msg1)

        priv = ['read', 'write']
        res = ['t', 'f']
        self.log.info('''-------切换到上述用户并查询其对directory的权限-------''')
        for i in range(2):
            cmd2 = f'''source {self.env}
                       gsql -d {self.user.db_name} -U hong -W {self.pwd} \
                       -p {self.user.db_port} -c \
                       "select has_directory_privilege('dir','{priv[i]}');"'''
            msg2 = self.user.sh(cmd2).result()
            self.log.info(msg2)
            result = msg2.splitlines()[-2].strip()
            self.assertTrue(result == res[i])

    def tearDown(self):
        cmd = f"""drop user if exists hong cascade;
                  drop directory if exists dir;"""
        self.commonsh.execut_db_sql(cmd)
        self.log.info('''---
        Opengauss_Function_Innerfunc_Has_Directory_Privilege_Case0005结束---''')

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
Case Name   : has_directory_privilege函数，查询当前用户是否有新建目录的权限
Description :
    1. 创建目录
    2. 省略参数1，即对当前用户进行查询
    3. 删除路径
Expect      :
    1. 创建成功，赋权成功
    2. 具有所有权限
    3. 删除成功
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('''---
        Opengauss_Function_Innerfunc_Has_Directory_Privilege_Case0004开始---''')

    def test_privilege(self):
        self.log.info('''----------------创建目录------------------''')
        cmd0 = f'''drop directory if exists dir;
           create or replace directory dir as '/tmp/';
            '''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('CREATE DIRECTORY') > -1)

        self.log.info('''---省略参数1，查询当前用户---''')
        cmd1 = '''select has_directory_privilege('dir','read');
            select has_directory_privilege('dir','write');
            '''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        res = msg1.splitlines()
        self.assertTrue(res.count(' t') == 2)

    def tearDown(self):
        cmd = f'''drop directory if exists dir;'''
        self.commonsh.execut_db_sql(cmd)
        self.log.info('''---
        Opengauss_Function_Innerfunc_Has_Directory_Privilege_Case0004结束---''')

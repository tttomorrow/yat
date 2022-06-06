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
Case Name   : analyze检测当前库的数据文件
Description :
    1. 创建sql文件
    2. 指定检测模式是FAST
    3. 指定检测模式是COMPLETE
Expect      :
    1. 创建成功
    2. 结果保存成功且结果显示分析表信息以及总时长
    3. 结果保存成功且结果显示分析表信息以及总时长
History     : 
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.user = Node('dbuser')
        self.env = macro.DB_ENV_PATH
        self.path = macro.DB_INSTANCE_PATH
        self.log.info('''---Opengauss_Function_DML_Set_Case0101开始---''')

    def test_analyse(self):
        cmd = ['ANALYZE VERIFY FAST;',
               'ANALYZE VERIFY COMPLETE;']
        self.verify = os.path.join(self.path, 'verify.sql')
        self.redirect = os.path.join(self.path, 'verify_redirect.txt')
        self.log.info(self.verify)
        self.log.info(self.redirect)
        for i in range(2):
            # 将analyse verify命令放入sql文件
            cmd0 = f'''echo "{cmd[i]}" > {self.verify};
                cat {self.verify}'''
            self.log.info(cmd0)
            msg0 = self.user.sh(cmd0).result()
            self.log.info(msg0)

            cmd1 = f'''source {self.env};\
            gsql -d {self.user.db_name}\
            -p {self.user.db_port}\
             -f "{self.verify}"> {self.redirect} 2>&1'''
            self.log.info(cmd1)
            self.user.sh(cmd1).result()

            # 结果保存成功且结果显示分析表信息以及总时长
            cmd2 = f'''cat {self.redirect}'''
            msg2 = self.user.sh(cmd2).result()
            self.log.info(msg2)
            self.assertTrue('ANALYZE VERIFY' in msg2)
            cost = msg2.splitlines()[-1]
            self.assertTrue(cost.split(':')[0] == 'total time')
            self.assertTrue(int(cost.split()[2]) > 0)

            cmd3 = f''' rm -rf {self.redirect};
                        rm -rf {self.verify}'''
            self.user.sh(cmd3).result()

    def tearDown(self):
        self.log.info('''---Opengauss_Function_DML_Set_Case0101结束---''')

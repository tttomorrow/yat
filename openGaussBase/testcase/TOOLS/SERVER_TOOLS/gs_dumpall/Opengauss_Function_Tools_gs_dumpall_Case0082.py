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
Case Type   : 服务端工具
Case Name   : 对导出的数据进行加密设置并将结果输出到指定的文件
Description :
    1.创建数据数
    2.对导出的数据进行加密设置并将结果输出到指定的文件
    3.清理环境
Expect      :
    1.数据创建成功
    2.导出成功
    3.清理环境成功
History     :
    modified：2022/1/10 by 5318639 优化用例适配新代码
"""

import os
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Tools_gs_dumpall_Case0082_start----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.dumpall_path = os.path.join(macro.DB_INSTANCE_PATH, 'dumpall_qm')
        self.key = f'12345678@qaz'
        self.t_name = 't_dump_0082'
        self.r_name = 'r_dump_0082'

    def test_server_tools(self):
        text = '----step1:创建测试数据;expect:构造成功----'
        self.log.info(text)
        sql_cmd1 = f'''drop table if exists {self.t_name}; 
            create table {self.t_name} (id int ,name char(10));
            insert into {self.t_name} values (1,'aa'),(2,'bb');
            drop role if exists {self.r_name}; 
            create role {self.r_name} identified by '{macro.COMMON_PASSWD}';
            '''
        gsql_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd1}"'
        self.log.info(gsql_cmd1)
        sql_msg1 = self.dbuser_node.sh(gsql_cmd1).result()
        self.log.info(sql_msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_msg1,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_msg1,
                      '执行失败:' + text)

        text = '----step2:导出的数据进行加密设置并将结果输出到指定的文件;expect:导出成功----'
        self.log.info(text)
        dumpall_cmd = f'source {macro.DB_ENV_PATH} ;' \
            f'gs_dumpall ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'--with-encryption=AES128 ' \
            f'--with-key={self.key} ' \
            f'-f {self.dumpall_path};'
        self.log.info(dumpall_cmd)
        dumpall_msg = self.dbuser_node.sh(dumpall_cmd).result()
        self.log.info(dumpall_msg)
        du_cmd = f'du -h {self.dumpall_path};'
        self.log.info(du_cmd)
        du_msg = self.dbuser_node.sh(du_cmd).result()
        self.log.info(du_msg)
        du_msg_list = du_msg.split()[0]
        self.assertTrue(float(du_msg_list[:-1]) > 0, '执行失败:' + text)
        self.assertIn(self.constant.gs_dumpall_success_msg, dumpall_msg,
                      '执行失败:' + text)

    def tearDown(self):
        text = '----step3:清理环境;expect:清理成功----'
        self.log.info(text)
        sql_cmd2 = f'''drop table if exists {self.t_name}; 
            drop role if exists {self.r_name};
            '''
        clear_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} ' \
            f'-c "{sql_cmd2}";'
        self.log.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        excute_cmd3 = f'rm -rf {self.dumpall_path};'
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, clear_msg,
                      '执行失败:' + text)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, clear_msg,
                      '执行失败:' + text)
        self.assertEqual('', msg3, '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_gs_dumpall_Case0082_finish----')

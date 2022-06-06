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
Case Type   : python驱动pyog
Case Name   : openGauss模式连接数据库，copy
Description :
    1.配置pg_hba入口
    2.配置enable_copy_server_files参数值为on，允许使用copy to/from
    3.连接数据库
    4.copy-to拷贝表数据到文件，copy-from拷贝文件到表
    5.断开连接
    6.还原enable_copy_server_files参数值
Expect      :
    1.执行成功
    2.执行成功
    3.连接成功，db.state返回'idle'
    4.执行成功
    5.执行成功，db.state返回'closed'
    6.执行成功
History     :
"""
import os
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython22(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.t_name = 't_py_copy22'
        text = '----Opengauss_Function_Connect_Python_Case0022 start----'
        self.LOG.info(text)

    def test_conn(self):
        text = '----step1: 配置pg_hba入口 expect: 成功----'
        self.LOG.info(text)
        host_cmd = "ifconfig -a|grep inet6 -a2|" \
                   "grep broadcast|awk '{print $2}'"
        self.host = os.popen(host_cmd).readlines()[0].strip()
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.pri_user.db_name} {self.pri_user.db_user} ' \
            f'{self.host}/32 sha256"'
        self.LOG.info(guc_cmd)
        guc_res = self.pri_user.sh(guc_cmd).result()
        self.LOG.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG,
                      guc_res,
                      f'执行失败: {text}')

        text = '----step2: 配置enable_copy_server_files参数值为on，' \
               '允许使用copy to/from expect: 成功----'
        self.LOG.info(text)
        befor_val = self.pri_sh.execute_gsguc('check', '',
                                              'enable_copy_server_files',
                                              get_detail=True)
        self.LOG.info(befor_val)
        guc_res = self.pri_sh.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'enable_copy_server_files=on')
        self.assertTrue(guc_res)

        text = '----step3: 连接数据库 expect: 成功----'
        self.LOG.info(text)
        conn_info = f'opengauss://{self.pri_user.db_user}:' \
            f'{self.pri_user.db_password}@{self.pri_user.db_host}:' \
            f'{self.pri_user.db_port}/{self.pri_user.db_name}'
        self.LOG.info(conn_info)
        db = py_opengauss.open(conn_info)
        self.assertEqual('idle', db.state, f'执行失败: {text}')

        text = '----step4: copy-to拷贝表数据到文件，copy-from拷贝文件到表 expect: 成功----'
        self.LOG.info(text)

        cmd = f'drop table if exists {self.t_name};'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.TABLE_DROP_SUCCESS,
                                 None), f'执行失败: {text}')

        cmd = f'create table {self.t_name} (a int,b int,c text);'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS,
                                 None), f'执行失败: {text}')

        cmd = f"insert into {self.t_name} values(generate_series(1,100000)," \
            f"generate_series(1,5),'c-'||generate_series(1,10));"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('INSERT', 100000), f'执行失败: {text}')

        self.copy_path = os.path.join('/home', self.pri_user.ssh_user,
                                      'copy.dat')

        cmd = f"copy {self.t_name} to '{self.copy_path}';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('COPY', 100000), f'执行失败: {text}')

        cmd = f"copy {self.t_name} from '{self.copy_path}';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('COPY', 100000), f'执行失败: {text}')

        cmd = f"select count(*) from {self.t_name};"
        self.LOG.info(cmd)
        sql = db.prepare(cmd).first()
        self.assertEqual(sql, 200000, f'执行失败: {text}')

        cmd = f'drop table if exists {self.t_name};'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.TABLE_DROP_SUCCESS,
                                 None), f'执行失败: {text}')

        text = '----step5: 断开连接 expect: 成功----'
        self.LOG.info(text)
        db.close()
        self.assertEqual('closed', db.state, f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----step6: 还原enable_copy_server_files参数值为off expect: 成功----'
        self.LOG.info(text)
        guc_res = self.pri_sh.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'enable_copy_server_files=off')
        self.assertTrue(guc_res)

        after_val = self.pri_sh.execute_gsguc('check', '',
                                              'enable_copy_server_files',
                                              get_detail=True)
        self.LOG.info(after_val)

        text = '----Opengauss_Function_Connect_Python_Case0022 end----'
        self.LOG.info(text)

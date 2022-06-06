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
Case Name   : 导出一个目录归档格式文件时设置压缩比级别
Description :
    1.创建数据库
    2.切换到新建的数据库创建表并插入数据
    3.导出一个目录归档格式文件时设置压缩比级别
    4.连接数据库，清理环境
Expect      :
    1.创建数据库成功
    2.切换到新建的数据库创建表并插入数据成功
    3.导出成功
    4.清理环境成功
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Tools_gs_dump_Case0021_start----')
        self.dbuser_node = Node('dbuser')
        self.pri_com = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.dump_path = os.path.join(macro.DB_INSTANCE_PATH, 'dump_qm')
        self.db_name = "db_dump0021"
        self.tb_name = "t_dump0021"

    def test_server_tools(self):
        text = '---step1:创建数据库;expect:创建成功---'
        self.log.info(text)
        sql_cmd = self.pri_com.execut_db_sql(f'''
                    drop database if exists {self.db_name};
                    create database {self.db_name};
                    ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '---step2:在创建好的数据库中创建表并插入数据;expect:创建成功---'
        self.log.info(text)
        sql_cmd = f'''
                drop table if exists {self.tb_name}; 
                create table {self.tb_name} (id int ,name char(10));
                insert into {self.tb_name} values (1,'aa'),(2,'bb');
                            '''
        self.log.info(sql_cmd)
        sql_result = self.pri_com.execut_db_sql(sql=sql_cmd,
                                              dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)

        text = '---step3:出一个目录归档格式文件时设置压缩比级别;expect:导出成功---'
        self.log.info(text)
        rm_cmd = f'''if [ -f "{self.dump_path}" ]
                     then
                        rm -rf {self.dump_path}
                     fi'''
        self.log.info(rm_cmd)
        rm_result = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_result)
        excute_cmd3 = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_dump -p {self.dbuser_node.db_port} {self.db_name} ' \
            f'--format=d  ' \
            f'-f {self.dump_path} ' \
            f'-Z 8;'
        self.log.info(excute_cmd3)
        msg3 = self.dbuser_node.sh(excute_cmd3).result()
        self.log.info(msg3)
        execute_cmd4 = f'du -h {self.dump_path};'
        msg4 = self.dbuser_node.sh(execute_cmd4).result()
        self.log.info(msg4)
        msg4_list = msg4.split()[0]
        self.assertTrue(float(msg4_list[:-1]) > 0)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg3)

    def tearDown(self):
        text = '---step4:清理环境;expect:清理成功---'
        self.log.info(text)
        rm_result = self.dbuser_node.sh(f'rm -rf {self.dump_path};').result()
        self.log.info(rm_result)
        sql_cmd = self.pri_com.execut_db_sql(f'drop database {self.db_name};')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertEqual('', rm_result, '执行失败:' + text)
        self.log.info(
            '-----Opengauss_Function_Tools_gs_dump_Case0021_finish-----')

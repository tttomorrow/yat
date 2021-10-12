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
Case Type   : 服务端工具
Case Name   : 在导出过程中再次发起导出(gs_dump+gs_dump)
Description :
    1.会话1,连接数据库构造大量的数据
    2.在会话1执行导出操作
    gs_dump dump -p port -f dump1.sql
    3.在会话1执行导出操作的同时在会话2执行导出操作
    gs_dump dump -p port -f dump2.sql
    4.对比导出的数据dump1.sql和dump2.sql
    5.清理环境：
    drop database databasename;
    rm -rf dump1.sql  dump2.sql;
Expect      :
    1.数据创建成功
    2.导出成功
    3.导出成功
    4.导出的过程互不影响都会导出成功,且导出的数据一致
    5.清理成功
History     : 
"""
import os
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Tools_gs_dump_Case0100start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.Primary_Node1 = Node('PrimaryDbUser')
        self.Primary_Node2 = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.com = Common()
        self.dump_path1 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump1.sql')
        self.dump_path2 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump2.sql')
        self.db_name = "db_dump0100"
        self.tb_name = "t_dump0100"

    def test_tools_dump(self):
        text = '---step1:创建测试数据;expect:创建成功---'
        self.log.info(text)
        self.log.info('------创建成功数据库-------')
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''
            drop database if exists {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        self.log.info('---在创建的数据库中创建表和数据---')
        sql_cmd = f'''drop table if  exists {self.tb_name};
            create table {self.tb_name} (id int);
            insert into {self.tb_name} values (generate_series(1,1000000));'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)
        text = '---step2:在会话1执行导出操作;expect:导出成功---'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_dump {self.db_name} \
            -p {self.Primary_Node1.db_port} \
            -f {self.dump_path1};
            '''
        self.log.info(dump_cmd)
        connect_thread1 = ComThread(
            self.com.get_sh_result, args=(self.Primary_Node1, dump_cmd))
        connect_thread1.setDaemon(True)
        connect_thread1.start()

        text = '-----step3.在会话1执行导出操作的同时在会话2执行导出操作;expect:导出成功-----'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_dump {self.db_name}\
            -p {self.Primary_Node2.db_port} \
            -f {self.dump_path2};
            '''
        self.log.info(dump_cmd)
        connect_thread2 = ComThread(
            self.com.get_sh_result, args=(self.Primary_Node2, dump_cmd))
        connect_thread2.setDaemon(True)
        connect_thread2.start()
        self.log.info('-----------获取session1结果-----------')
        connect_thread1.join(180)
        thread1_result = connect_thread1.get_result()
        self.log.info(thread1_result)
        self.assertIn(f'dump database {self.db_name} successfully',
                      thread1_result,
                      '执行失败:' + text)
        self.log.info('-----------获取session2结果-----------')
        connect_thread2.join(180)
        thread2_result = connect_thread2.get_result()
        self.log.info(thread2_result)
        self.assertIn(f'dump database {self.db_name} successfully',
                      thread2_result,
                      '执行失败:' + text)
        text = '---step4:对比导出的数据dump1.sql和dump2.sql;expect:导出的数据一致---'
        self.log.info(text)
        self.log.info('----------导出对象个数,大小对比----------')
        dump1 = thread1_result.split()[7].strip('.')
        self.log.info(dump1)
        dump2 = thread2_result.split()[7].strip('.')
        self.log.info(dump2)
        self.assertEqual(dump1, dump2, '执行失败:' + text)
        du_cmd1 = f'du -h {self.dump_path1}; '
        du_msg1 = self.Primary_Node1.sh(du_cmd1).result()
        self.log.info(du_msg1)
        dump_result1 = du_msg1.split()[0]
        self.log.info(dump_result1)
        du_cmd2 = f'du -h {self.dump_path2}; '
        du_msg2 = self.Primary_Node1.sh(du_cmd2).result()
        self.log.info(du_msg2)
        dump_result2 = du_msg2.split()[0]
        self.log.info(dump_result2)
        self.assertEqual(dump_result1, dump_result2, '执行失败:' + text)

    def tearDown(self):
        text = '--------------step5:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.dump_path1};rm -rf {self.dump_path2};'
        self.log.info(rm_cmd)
        result = self.Root_Node.sh(rm_cmd).result()
        self.log.info(result)
        sql_cmd = self.pri_sh.execut_db_sql(
            f'drop database if exists  {self.db_name};')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Tools_gs_dump_Case0100finish------')

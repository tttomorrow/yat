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
Case Type   : 功能
Case Name   : 在事务中创建hash索引，未提交之前以及提交后观察事务隔离性是否正确
Description :
    1.创建表、插入数据
    2.session1开启事务，为测试表创建hash索引，不提交并查询
    3.session1未提交前在session2中查询索引;待session1提交后，session2查询
    4.清理环境
Expect      :
    1.创建成功
    2.开启事务成功,创建索引成功，未提交session1查询索引存在
    3.索引不存在;索引存在
    4.清理环境完成
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DmlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DML_Lock_Case0009开始')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.commonsh2 = CommonSH('PrimaryDbUser')
        self.tb_name = "t_hash_index_0009"
        self.id_name = "i_hash_index_0009"
        self.db_name = "db_hash_index_0009"

    def test_dml_lock(self):
        text = '-----step1:创建表;expect:创建成功-----'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(f'''
            drop table if exists {self.tb_name};
            create table {self.tb_name} (id int, num int, sex varchar 
            default 'male');
            insert into {self.tb_name} select random()*10, random()*3, 'XXX' \
            from generate_series(1,5000);''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = 'step2:session1开启事务，为测试表创建hash索引，不提交并查询' \
               'expect:开启事务成功,创建索引成功，未提交session1查询索引存在'
        self.log.info(text)
        sql = f'''begin;
            drop index if exists {self.id_name};
            create index {self.id_name} on {self.tb_name} using hash (id);
            select relname from pg_class where  relname ='{self.id_name}';
            select pg_sleep(10);
            commit;'''
        thread_1 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()
        time.sleep(3)

        text = '-----step3:session1未提交前在session2中查询索引;' \
               '待session1提交后，session2查询;expect:索引不存在;索引存在---'
        self.log.info(text)
        sql = f'''select relname from pg_class where  relname ='{self.id_name}';
            select pg_sleep(15);
           select relname from pg_class where  relname ='{self.id_name}';'''
        thread_2 = ComThread(self.commonsh2.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        self.log.info('获取session1结果')
        thread_1.join(20)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)
        self.assertIn('BEGIN', msg_result_1, '执行失败:' + text)
        self.assertIn(f'{self.id_name}', msg_result_1, '执行失败:' + text)

        self.log.info('获取session2结果')
        thread_2.join(30)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)
        self.assertEqual('(0 rows)', msg_result_2.splitlines()[2].strip(),
                         '执行失败:' + text)
        self.assertEqual(f'{self.id_name}',
                         msg_result_2.splitlines()[-2].strip(),
                         '执行失败:' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(f'''drop table if exists \
            {self.tb_name};''')
        self.log.info(sql_cmd)
        self.log.info(
            '-Opengauss_Function_DDL_Hash_Index_Case0009finish--')

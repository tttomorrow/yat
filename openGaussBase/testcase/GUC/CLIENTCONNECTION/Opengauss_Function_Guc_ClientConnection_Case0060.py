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
Case Name   : 参数default_transaction_isolation保持默认，验证其参数值read committed（避免脏读）
Description :
    1.查询参数默认值
    2.创建表、插入数据
    3.session1开启事务，修改数据并查询
    4.session1未提交在session2中查询表数据;待session1提交后，session2查询
    4.清理环境
Expect      :
    1.默认值为read committed
    2.创建成功
    3.数据修改成功
    4.数据未发生变化;数据已修改
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
        self.log.info('-Opengauss_Function_Guc_ClientConnection_Case0060start')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.commonsh2 = CommonSH('PrimaryDbUser')
        self.tb_name = "t_guc_clientconnection_0060"

    def test_dml_lock(self):
        text = '--step1:查询参数默认值;expect:默认值为read committed'
        sql_cmd = self.commonsh1.execut_db_sql(f'''show  
            default_transaction_isolation;''')
        self.log.info(sql_cmd)
        self.assertIn('read committed', sql_cmd,  '执行失败:' + text)
        text = '-----step2:创建表并插入数据;expect:创建成功-----'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(f'''drop table if exists \
            {self.tb_name};
             create table {self.tb_name}(id int,name varchar(20));
             insert into {self.tb_name} values(1,'tom'),(2,'lily');''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        text = 'step3:session1开启事务，修改数据并查询;expect:数据修改成功'
        self.log.info(text)
        sql = f'''start transaction;
           update {self.tb_name} set id = id +1 where name = 'lily';
           select * from {self.tb_name};
           select pg_sleep(10);
           commit;'''
        thread_1 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()
        time.sleep(3)
        text = '--step4:session1未提交在session2中查询表数据;待session1提交' \
               '后，session2查询;expect:数据未发生变化;数据已修改'
        self.log.info(text)
        sql = f''' select * from {self.tb_name};
            select pg_sleep(15);
           select * from {self.tb_name};'''
        thread_2 = ComThread(self.commonsh2.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        self.log.info('获取step3结果')
        thread_1.join(20)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)
        self.assertIn('START TRANSACTION', msg_result_1, '执行失败:' + text)
        self.assertIn('3 | lily', msg_result_1, '执行失败:' + text)

        self.log.info('获取step4结果')
        thread_2.join(30)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)
        msg = msg_result_2.splitlines()
        self.log.info(msg)
        self.assertIn('2 | lily', msg_result_2.splitlines()[3].strip(),
                      '执行失败:' + text)
        self.assertIn('3 | lily', msg_result_2.splitlines()[-2].strip(),
                      '执行失败:' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.commonsh1.execut_db_sql(f'''drop table if exists \
            {self.tb_name};''')
        self.log.info(sql_cmd)
        self.log.info(
            '-Opengauss_Function_Guc_ClientConnection_Case0060finish--')

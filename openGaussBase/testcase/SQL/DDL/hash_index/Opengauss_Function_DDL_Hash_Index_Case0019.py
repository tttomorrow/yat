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
Case Name   :  shared_buffers和maintenance_work_mem值较小时，行存表建数据量较
               大的索引
Description :
    1.修改参数shared_buffers和maintenance_work_mem为128MB
    2.重启数据库
    3.创建测试表，创建哈希索引并插入50W数据
    4.使用索引
    5.清理环境
Expect      :
    1.修改成功
    2.重启数据库成功
    3.创建测试表，创建哈希索引并插入50W数据成功
    4.索引数据存在且查询计划走索引扫描
    5.清理环境完成
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0019start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = "t_hash_index_0019"
        self.id_name = "i_hash_index_0019"

    def test_hash_index(self):
        text = '---step1:修改参数shared_buffers和maintenance_work_mem;' \
               'expect:修改成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('''show shared_buffers;''')
        self.log.info(sql_cmd)
        self.res1 = sql_cmd.splitlines()[-2].strip()
        sql_cmd = self.pri_sh.execut_db_sql('''show maintenance_work_mem;''')
        self.log.info(sql_cmd)
        self.res2 = sql_cmd.splitlines()[-2].strip()
        msg = self.pri_sh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'shared_buffers = 128MB')
        self.log.info(msg)
        self.assertTrue(msg, '执行失败:' + text)
        msg = self.pri_sh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'maintenance_work_mem = 128MB')
        self.log.info(msg)
        self.assertTrue(msg, '执行失败:' + text)
        text = '--step2:重启数据库;expect:数据库重启成功且状态正常--'
        self.log.info(text)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '---step3:创建表并插入数据；创建哈希索引;expect:创建成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists \
            {self.tb_name};
            create table {self.tb_name} (id int, num int, sex varchar 
            default 'male');
            insert into {self.tb_name} select random()*10, random()*3, 'XXX' \
            from generate_series(1,500000);
            drop index if exists {self.id_name};
            create index {self.id_name} on {self.tb_name} using hash (id);''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '--step4:使用索引;expect:索引数据存在且数据量大时走索引扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''set enable_seqscan = off;\
            select count(*) from {self.tb_name} where id=10;\
            explain select count(*) from {self.tb_name} where id=10;''')
        self.assertIn('1 row', sql_cmd, '执行失败:' + text)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '---step5:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists \
            {self.tb_name};''')
        self.log.info(sql_cmd)
        msg = self.pri_sh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'shared_buffers={self.res1}')
        self.log.info(msg)
        msg = self.pri_sh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'maintenance_work_mem={self.res2}')
        self.log.info(msg)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0019finish--')

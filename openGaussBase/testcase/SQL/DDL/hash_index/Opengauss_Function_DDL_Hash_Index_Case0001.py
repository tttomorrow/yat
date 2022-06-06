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
Case Name   : 创建hash索引后，对索引数据进行DML操作，创建逻辑复制槽并解码
Description :
        1.修改参数wal_level为logical;
        2.重启数据库
        3.创建逻辑复制槽
        4.建表并创建hash索引
        5.读取复制槽解码结果；解码insert语句
        6.修改索引数据
        7.读取复制槽解码结果；解码update语句
        8.查询索引数据
        9.删除索引数据
        10.读取复制槽解码结果；解码delete语句
        11.删除索引后查看解码
        12.清理环境
Expect      :
        1.修改参数wal_level为logical成功
        2.重启数据库成功
        3.创建逻辑复制槽成功
        4.建表并创建hash索引成功
        5.解码成功
        6.修改索引数据成功
        7.解码成功
        8.数据量少时查询计划走顺序扫描
        9.删除索引数据成功
        10.解码成功
        11.删除索引不解码
        12.清理环境完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0001start-')
        self.constant = Constant()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.slot_name = "slot_hash_index_0001"
        self.tb_name = "t_hash_index_0001"
        self.id_name = "i_hash_index_0001"

    def test_standby(self):
        text = '--step1:修改wal_level为logical;expect:修改成功--'
        self.log.info(text)
        mod_msg = self.primary_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        text = '--step2:重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = self.primary_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:创建逻辑复制槽;expect:创建成功--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''select * from \
            pg_create_logical_replication_slot('{self.slot_name}', \
            'mppdb_decoding');''')
        self.log.info(sql_cmd)
        self.assertIn(f'{self.slot_name}', sql_cmd, '执行失败:' + text)

        text = '--step4:建表并创建hash索引;expect:创建成功--'
        self.log.info(text)
        create_cmd = self.primary_sh.execut_db_sql(f'''drop table if exists 
            {self.tb_name};
            create table {self.tb_name} (id int, sex varchar(20));
            insert into {self.tb_name} values(5, 'XXX');
            drop index if exists {self.id_name};
            create index {self.id_name} on {self.tb_name} using hash (id);''')
        self.log.info(create_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, create_cmd,
                      '执行失败:' + text)

        text = '--step5:读取复制槽解码结果；解码insert语句;expect:解码成功--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''select * from \
            pg_logical_slot_peek_changes('{self.slot_name}', null, 4096);''')
        self.log.info(sql_cmd)
        self.assertIn('"op_type":"INSERT"', sql_cmd, '执行失败:' + text)

        text = '--step6:修改索引数据;expect:修改成功--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''update {self.tb_name} \
            set id = id*10;''')
        self.log.info(sql_cmd)
        self.assertIn('UPDATE', sql_cmd, '执行失败:' + text)

        text = '--step7:读取复制槽解码结果；解码update语句;expect:解码成功--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''select * from \
        pg_logical_slot_peek_changes('{self.slot_name}', null, 4096);''')
        self.log.info(sql_cmd)
        self.assertIn('"op_type":"UPDATE"', sql_cmd, '执行失败:' + text)

        text = '--step8:查询索引数据;expect:数据量少时查询计划走顺序扫描--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''explain select * from \
            {self.tb_name} where id =50;''')
        self.log.info(sql_cmd)
        self.assertIn('Seq Scan', sql_cmd, '执行失败:' + text)

        text = '--step9:删除索引数据;expect:删除成功--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''delete from {self.tb_name} \
            where id =50;''')
        self.log.info(sql_cmd)

        text = '--step10:读取复制槽解码结果；解码delete语句;expect:解码成功--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''select * from \
            pg_logical_slot_peek_changes('{self.slot_name}', null, 4096);''')
        self.log.info(sql_cmd)
        self.assertIn('"op_type":"DELETE"', sql_cmd, '执行失败:' + text)

        text = '--step11:删除索引后查看解码;expect:删除索引不解码;--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''drop index {self.id_name};
            select * from pg_logical_slot_peek_changes\
            ('{self.slot_name}', NULL, 4096); ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.DROP_INDEX_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.assertNotIn('"op_type":"DROP"', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step12:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''select * from \
            pg_drop_replication_slot('{self.slot_name}');\
            drop table if exists {self.tb_name};''')
        self.log.info(sql_cmd)
        restore_cmd = self.primary_sh.execute_gsguc('set',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               'wal_level=hot_standby')
        self.log.info(restore_cmd)
        restart_msg = self.primary_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0001finish--')

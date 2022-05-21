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
Case Name   : 并行回放模式下，创建并使用hash索引
Description :
        1.修改参数recovery_max_workers
        2.重启数据库
        3.建表并创建hash索引
        4.使用索引
        5.备机查询
        6.主机修改索引所属空间
        7.主机查询索引
        8.备机查询索引
        9.主机修改索引数据并查询
        10.备机查询索引数据
        11.清理环境
Expect      :
        1.修改成功
        2.重启数据库成功
        3.建表并创建hash索引成功
        4.索引数据存在且查询计划走索引扫描
        5.索引数据与主机一致且查询计划走索引扫描
        6.修改成功
        7.索引空间已变更
        8.索引空间已变更
        9.修改成功
        10.查询计划走索引扫描
        11.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0003start-')
        self.constant = Constant()
        self.common = Common()
        self.com = CommonSH("PrimaryDbUser")
        self.primary_node = Node("PrimaryDbUser")
        self.standby_sh = CommonSH('Standby1DbUser')
        self.tb_name = "t_hash_index_0003"
        self.id_name = "i_hash_index_0003"
        self.ts_name = "ts_hash_index_0003"

        text = "备份postgres.conf文件"
        self.log.info(text)
        self.file = os.path.join(macro.DB_INSTANCE_PATH,
                                 macro.DB_PG_CONFIG_NAME)
        result = self.common.get_sh_result(self.primary_node,
                                           f"cp {self.file} "
                                           f"{self.file}backup")
        self.assertNotIn("bash", result, "执行失败:" + text)
        self.assertNotIn("ERROR", result, "执行失败:" + text)
        
    def test_standby(self):
        self.log.info(f"--修改参数 确认落盘--")
        result = Primary_SH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"synchronous_standby_names='*'")
        self.assertTrue(result)
        result = Primary_SH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"synchronous_commit='remote_apply'")
        self.assertTrue(result)
        result = Primary_SH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"hot_standby=on")
        self.assertTrue(result)
        result = Primary_SH.execute_gsguc("set",
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       f"wal_level='hot_standby'")
        self.assertTrue(result)
        status = Primary_SH.restart_db_cluster()
        self.log.info(status)
        status = Primary_SH.get_db_cluster_status()
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        
        text = '--step1:设置参数大于1即可;expect:修改成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql('''show recovery_max_workers;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'recovery_max_workers=4')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        text = '--step2:重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status('detail')
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:建表并创建hash索引;expect:创建成功--'
        self.log.info(text)
        create_cmd = Primary_SH.execut_db_sql(f'''drop table if exists \
            {self.tb_name};
            create table {self.tb_name} (id int, num int, sex varchar(20) \
            default 'male');
            insert into {self.tb_name} select random()*10, random()*3, \
            'XXX' from generate_series(1,5000);
            drop index if exists {self.id_name};
            create index {self.id_name} on {self.tb_name} using hash (id);''')
        self.log.info(create_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, create_cmd,
                      '执行失败:' + text)

        text = '--step4:使用索引;expect:索引数据存在且查询计划走索引扫描--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f'''select count(*) from \
            {self.tb_name} where id=10;
            explain select count(*) from {self.tb_name} where id=10;''')
        self.log.info(sql_cmd)
        msg = sql_cmd.splitlines()
        self.log.info(msg)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

        text = '--step5:备机查询;expect:索引数据与主机一致且查询计划' \
               '走索引扫描--'
        self.log.info(text)
        sql_cmd = self.standby_sh.execut_db_sql(f'''select count(*) from \
            {self.tb_name} where id=10;
            explain select count(*) from {self.tb_name} where id=10;''')
        self.log.info(sql_cmd)
        msg = sql_cmd.splitlines()
        self.log.info(msg)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

        text = '--step6:主机修改索引所属空间;expect:修改成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f'''drop tablespace if exists \
            {self.ts_name};\
            create tablespace {self.ts_name} relative location \
            '{self.ts_name}/tablespace_1';
            alter index {self.id_name} set tablespace {self.ts_name};
            ;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant. ALTER_INDEX_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '--step7:主机查询索引;expect:索引空间已变更，' \
               '查询计划走索引扫描--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f'''\d+ {self.tb_name};''')
        self.log.info(sql_cmd)
        self.assertIn(f'{self.ts_name}', sql_cmd, '执行失败:' + text)
        sql_cmd = Primary_SH.execut_db_sql(f'''explain select count(*) from \
            {self.tb_name} where id=10;''')
        self.log.info(sql_cmd)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

        text = '--step8:备机查询索引;expect:索引空间已变更，' \
               '查询计划走索引扫描--'
        self.log.info(text)
        sql_cmd = self.standby_sh.execut_db_sql(f'''\d+ {self.tb_name}; ''')
        self.log.info(sql_cmd)
        self.assertIn(f'{self.ts_name}', sql_cmd, '执行失败:' + text)
        sql_cmd = self.standby_sh.execut_db_sql(f'''explain select count(*) \
            from {self.tb_name} where id=10;''')
        self.log.info(sql_cmd)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

        text = '--step9:主机修改索引数据并查询;expect:修改成功，' \
               '查询计划走索引扫描--'
        self.log.info(text)
        sql_cmd = self.standby_sh.execut_db_sql(f'''update {self.tb_name} \
            set id=10*10;
            explain select count(*) from {self.tb_name} where id=100;''')
        self.log.info(sql_cmd)
        self.assertIn('UPDATE', sql_cmd, '执行失败:' + text)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

        text = '--step10:备机查询索引数据;expect:查询计划走索引扫描--'
        self.log.info(text)
        sql_cmd = self.standby_sh.execut_db_sql(f'''explain select count(*) \
            from {self.tb_name} where id=100;''')
        self.log.info(sql_cmd)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step11:清理环境;expect:清理环境完成--'
        self.log.info(text)
        
        self.log.info(f"恢复postgres.conf文件")
        cmd_result = self.common.get_sh_result(self.primary_node,
                                           f"mv {self.file}backup "
                                           f"{self.file}")
        self.log.info(cmd_result)
        
        sql_cmd = Primary_SH.execut_db_sql(f'''drop table if exists \
            {self.tb_name};''')
        self.log.info(sql_cmd)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f'recovery_max_workers={self.res}')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status('detail')
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0003finish--')

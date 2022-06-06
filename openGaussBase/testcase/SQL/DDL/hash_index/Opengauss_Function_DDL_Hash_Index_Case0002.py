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
Case Name   : 极致rto下，创建并使用hash索引
Description :
        1.修改参数
        2.重启数据库
        3.建表并创建hash索引
        4.使用索引
        5.主备切换
        6.新主机使用索引
        7.清理环境
Expect      :
        1.修改成功
        2.重启数据库成功
        3.建表并创建hash索引成功
        4.索引数据存在且查询计划走索引扫描
        5.主备切换成功
        6.索引数据与原主机一致且查询计划走索引扫描
        7.清理环境完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0002start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.standby_sh = CommonSH('Standby1DbUser')
        self.tb_name = "t_hash_index_0002"
        self.id_name = "i_hash_index_0002"

    def test_standby(self):
        text = '--step1:开启极致RTO;expect:修改成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql('''show replication_type;''')
        self.log.info(sql_cmd)
        self.res1 = sql_cmd.splitlines()[-2].strip()
        sql_cmd = Primary_SH.execut_db_sql('''show recovery_parse_workers;''')
        self.log.info(sql_cmd)
        self.res2 = sql_cmd.splitlines()[-2].strip()
        sql_cmd = Primary_SH.execut_db_sql('''show recovery_redo_workers;''')
        self.log.info(sql_cmd)
        self.res3 = sql_cmd.splitlines()[-2].strip()
        sql_cmd = Primary_SH.execut_db_sql('''show hot_standby;''')
        self.log.info(sql_cmd)
        self.res4 = sql_cmd.splitlines()[-2].strip()
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'replication_type=1')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'recovery_parse_workers=4')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'recovery_redo_workers=4')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'hot_standby=off')
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
        res_count1 = sql_cmd.splitlines()[2].strip()
        self.log.info(res_count1)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

        text = '--step5:主备切换;expect:切换成功--'
        self.log.info(text)
        result = self.standby_sh.execute_gsctl('switchover',
                                               'switchover completed')
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)
        result = self.standby_sh.exec_refresh_conf()
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)
        result = self.standby_sh.get_db_cluster_status('detail')
        self.log.info(result)
        self.assertTrue("Degraded" in result or "Normal" in result,
                        '执行失败:' + text)

        text = '--step6:新主机查询;expect:索引数据与原主机一致且查询计划' \
               '走索引扫描--'
        self.log.info(text)
        sql_cmd = self.standby_sh.execut_db_sql(f'''select count(*) from \
            {self.tb_name} where id=10;
            explain select count(*) from {self.tb_name} where id=10;''')
        self.log.info(sql_cmd)
        res_count2 = sql_cmd.splitlines()[2].strip()
        self.log.info(res_count2)
        self.assertEqual(res_count1, res_count2, '执行失败:' + text)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step7:清理环境;expect:清理环境完成--'
        self.log.info(text)
        result = Primary_SH.execute_gsctl('switchover',
                                          'switchover completed')
        self.log.info(result)
        self.assertTrue(result)
        result = Primary_SH.exec_refresh_conf()
        self.log.info(result)
        self.assertTrue(result)
        result = Primary_SH.get_db_cluster_status('detail')
        self.log.info(result)
        self.assertTrue("Degraded" in result or "Normal" in result,
                        '执行失败:' + text)
        sql_cmd = Primary_SH.execut_db_sql(f'''drop table if exists \
        {self.tb_name};''')
        self.log.info(sql_cmd)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f'replication_type={self.res1}')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f'recovery_parse_workers\
                                           ={self.res2}')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f'recovery_redo_workers\
                                           ={self.res3}')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f'hot_standby={self.res4}')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0002finish--')

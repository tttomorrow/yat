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
Case Type   : MOT
Case Name   : 结合MOT表，结合系统表或系统视图查询内存表信息
Description :
    1、检查参数，修改配置，并重启数据库
       gs_guc set -D cluster/dn1 -c "enable_incremental_checkpoint=off"
    2、创建MOT内存表，与系统表pg_class结合测试
    3、创建和内存表关联视图，与系统表pg_class结合测试
    4、清理环境
Expect      :
    1、修改成功，重启数据库成功；
    2、创建内存表成功，系统表中可以查到相关信息；
    3、创建关联视图成功；
    4、清理环境成功；
History     :
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class MotDdlTest(unittest.TestCase):

    def setUp(self):
        logger.info("======Opengauss_Function_MOT_Case0102开始执行======")
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.mot_table = 'mot_table_test'
        logger.info('======步骤1：检查参数，修改配置，并重启数据库======')
        self.config_item = "enable_incremental_checkpoint=off"
        check_res = self.sh_primysh.execut_db_sql(
            f'''show enable_incremental_checkpoint;''')
        if 'off' not in check_res.split('\n')[-2].strip():
            self.sh_primysh.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG, self.config_item)
            self.sh_primysh.restart_db_cluster()
            result = self.sh_primysh.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)

    def test_mot_ddl(self):
        logger.info("======步骤2：创建MOT内存表，与系统表pg_class结合测试======")
        sql_cmd1 = f'''--创建MOT表
            drop foreign table if exists {self.mot_table};
            create foreign table {self.mot_table}(id int,name varchar(10));
            --插入数据
            insert into {self.mot_table} values(generate_series(1,200),'a');
            --查看系统表pg_class中内存表的字段数量信息
            select relnatts from pg_class where relname='{self.mot_table}';
            --查看系统表中pg_class数据库对象(mot_table_test)的类型,f表示外表
            select relkind from pg_class where relname='{self.mot_table}';
            '''
        msg1 = self.sh_primysh.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg1)
        self.assertEqual('2', msg1.splitlines()[-7].strip())
        self.assertEqual('f', msg1.splitlines()[-2].strip())

        logger.info("======步骤3：创建和内存表关联视图，与系统表pg_class结合测试======")
        sql_cmd2 = f'''--创建视图
            create view mot_view as 
            select * from {self.mot_table} where id < 100;
            --查看系统表pg_class中视图的字段数量信息
            select relnatts from pg_class where relname='mot_view';
            --查看系统表中pg_class数据库对象(mot_table_test)的类型,v表示视图
            select relkind from pg_class where relname='mot_view';
            '''
        msg2 = self.sh_primysh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.constant.CREATE_VIEW_SUCCESS_MSG, msg2)
        self.assertEqual('2', msg2.splitlines()[-7].strip())
        self.assertEqual('v', msg2.splitlines()[-2].strip())

    def tearDown(self):
        logger.info("======后置处理,清理环境======")
        rm_cmd = f'''drop foreign table {self.mot_table} cascade'''
        rm_res = self.sh_primysh.execut_db_sql(rm_cmd)
        logger.info(rm_res)
        logger.info("======Opengauss_Function_MOT_Case0102执行完成======")

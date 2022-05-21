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
Case Type   : GSC功能模块
Case Name   : 非线程池模式场景下，进行gs_gsc_clean，清理功能正常
Description :
    1、修改enable_global_syscache为on;enable_thread_pool为off;
    2、重启数据库，使参数生效;
    3、创建5个数据库;
    4、执行批量建表删除表函数创建，批量建表;
    5、查询所有库并进行连接;
    6、查看syscache占用情况;
    7、并发对5个库所有表进行查询;
    8、查看syscache占用情况;
    9、进行gs_gsc_clean;
    10、查看syscache占用情况;
Expect      :
    1、修改enable_global_syscache为on;enable_thread_pool为off; 成功
    2、重启数据库，使参数生效; 重启成功
    3、创建5个数据库; 创建成功
    4、执行批量建表删除表函数创建，批量建表; 成功
    5、查询所有库并进行连接; 连接成功
    6、查看syscache占用情况; 查询成功
    7、并发对5个库所有表进行查询; 执行成功
    8、查看syscache占用情况; 查询成功
    9、进行gs_gsc_clean; 清理成功
    10、查看syscache占用情况; 比步骤8占用减少
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


class GscTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.table_num = 300
        self.db_num = 5
        self.fun_create_name = 'fun_create_tb_gsc0015'
        self.fun_drop_name = 'fun_drop_tb_gsc0015'
        self.db_ex_name = 'db_gsc0015_'
        self.tb_ex_name = 'tb_gsc0015_'
        self.fun_create_tb = f'''
        drop function if exists public.{self.fun_create_name};
        create or replace function public.{self.fun_create_name} (
        table_num integer)
        returns void
        language 'plpgsql'
        cost 100
        volatile 
        as \$body\$
        declare
        v_idx integer := 0;
        v_strtable varchar :='';
        v_strsql varchar :='';
        begin
          while v_idx < table_num loop
          v_idx = v_idx+1;
          v_strtable = concat('{self.tb_ex_name}', v_idx);
          v_strsql = 'create table '||v_strtable||'(idx integer,log varchar)';
          execute v_strsql;
          end loop;
         end
        \$body\$;'''

        self.fun_drop_tb = f'''
        drop function if exists  public.{self.fun_drop_name};
        create or replace function public.{self.fun_drop_name}(
        table_num_in integer)
        returns void
        language 'plpgsql'
        cost 100
        volatile 
        as \$body\$
        declare
        v_idx integer := 0;
        v_strtable varchar :='';
        v_strsql varchar :='';
        begin
          while v_idx < table_num_in loop
          v_idx = v_idx+1;
          v_strtable = concat('{self.tb_ex_name}', v_idx);
          v_strsql = 'drop table if exists '||v_strtable;
          execute v_strsql;
          end loop;
         end
        \$body\$;
        '''

    def test_main(self):
        step_txt = '----step0:查看enable_global_syscache初始配置值;----'
        self.log.info(step_txt)
        self.init_para1 = self.com.show_param('enable_global_syscache')
        step_txt = '----step0:查看enable_thread_pool初始值;----'
        self.log.info(step_txt)
        self.init_para2 = self.com.show_param('enable_thread_pool')

        step_txt = '----step1:修改enable_global_syscache为on;' \
                   'enable_thread_pool为off; expect:成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= on")
        self.assertTrue(msg, '执行失败:' + step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_thread_pool= off")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step2:重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result)
        self.log.info('----查询参数----')
        self.new_para1 = self.com.show_param('enable_global_syscache')
        self.assertEqual(self.new_para1, 'on', '执行失败:' + step_txt)
        self.new_para2 = self.com.show_param('enable_thread_pool')
        self.assertEqual(self.new_para2, 'off', '执行失败:' + step_txt)

        step_txt = f'----step3:创建{self.db_num}个数据库; expect:创建成功----'
        self.log.info(step_txt)
        for i in range(self.db_num):
            create_db = f'create database {self.db_ex_name}{i};'
            create_result = self.sh.execut_db_sql(create_db)
            self.log.info(create_result)
            self.assertIn(self.constant.CREATE_DATABASE_SUCCESS,
                          create_result, '执行失败:' + step_txt)

        step_txt = '----step4:执行批量建表删除表函数创建，批量建表; expect:成功----'
        self.log.info(step_txt)
        for i in range(self.db_num):
            result = self.sh.execut_db_sql(self.fun_create_tb,
                                           dbname=f'{self.db_ex_name}{i}')
            self.log.info(result)
            self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result,
                          '执行失败:' + step_txt)
            result = self.sh.execut_db_sql(self.fun_drop_tb,
                                           dbname=f'{self.db_ex_name}{i}')
            self.log.info(result)
            self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result,
                          '执行失败:' + step_txt)

            self.log.info(f"--{self.db_ex_name}{i}执行批量建表函数--")
            create_tb = f"select public.{self.fun_create_name} " \
                f"({self.table_num});"
            result = self.sh.execut_db_sql(create_tb,
                                           dbname=f'{self.db_ex_name}{i}')
            self.log.info(result)
            check_tb = f"select count(*) from pg_class where relname " \
                f"like '{self.tb_ex_name}%';"
            result = self.sh.execut_db_sql(check_tb,
                                           dbname=f'{self.db_ex_name}{i}')
            self.log.info(result)
            self.assertEqual(int(result.splitlines()[-2].strip()),
                             self.table_num, '执行失败:' + step_txt)

        step_txt = '----step5:查询所有库并进行连接; expect:连接成功----'
        self.log.info(step_txt)
        select_db_sql = "select datname from pg_database where datname " \
                        "not like('template%');"
        select_db_result = self.sh.execut_db_sql(select_db_sql)
        self.log.info(select_db_result)
        db_list = select_db_result.splitlines()[2:-1:1]
        for i in db_list:
            con_result = self.sh.execut_db_sql('select current_database();',
                                               dbname=f'{i}')
            self.log.info(con_result)
            self.assertIn(i, con_result, '执行失败:' + step_txt)

        step_txt = '----step6:查看syscache占用情况; expect:查询成功----'
        self.log.info(step_txt)
        check_sql = "select sum(totalsize) from gs_gsc_memory_detail ;" \
                    "select * from gs_gsc_memory_detail; "
        result = self.sh.execut_db_sql(check_sql)
        self.log.info(result)

        step_txt = f'----step7:并发对{self.db_num}个库所有表进行查询; expect:执行成功----'
        self.log.info(step_txt)
        select_sql = ''
        for j in range(1, int(self.table_num) + 1):
            select_sql = select_sql + \
                         f'select * from {self.tb_ex_name}{j};'
        connect_thread = []
        for i in range(self.db_num):
            connect_thread.append(ComThread(self.sh.execut_db_sql, args=(
                select_sql, '', f'{self.db_ex_name}{i}')))
            connect_thread[i].setDaemon(True)
            connect_thread[i].start()
        for i in range(self.db_num):
            connect_thread[i].join(600)
            result = connect_thread[i].get_result()
            self.assertEqual(result.count('0 rows'), self.table_num,
                             '执行失败:' + step_txt)

        step_txt = '----step8:查看syscache占用情况; expect:查询成功----'
        self.log.info(step_txt)
        check_result = self.sh.execut_db_sql(check_sql)
        self.log.info(check_result)
        total_size1 = int(check_result.splitlines()[2].split()[0].strip())
        self.assertGreater(total_size1, 0, '执行失败:' + step_txt)

        step_txt = '----step9:进行gs_gsc_clean; expect:清理成功----'
        self.log.info(step_txt)
        clean_sql = "select * from gs_gsc_clean();"
        clean_result = self.sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)
        self.assertEqual(clean_result.splitlines()[2].strip(), 't',
                         '执行失败:' + step_txt)

        step_txt = '----step10:查看syscache占用情况; expect:比步骤8占用减少----'
        self.log.info(step_txt)
        check_result = self.sh.execut_db_sql(check_sql)
        self.log.info(check_result)
        total_size2 = int(check_result.splitlines()[2].split()[0].strip())
        self.assertGreater(total_size1, total_size2, '执行失败:' + step_txt)

    def tearDown(self):
        step_txt = '----this is teardown----'
        self.log.info(step_txt)
        step1_txt = '----删除数据库 expect:删除成功----'
        self.log.info(step1_txt)
        drop_db_result = ''
        for i in range(self.db_num):
            drop_db = f'drop database {self.db_ex_name}{i}'
            drop_db_result = drop_db_result + self.sh.execut_db_sql(drop_db)

        step2_txt = '----恢复参数为初始值并查询; expect:设置成功----'
        self.log.info(step2_txt)
        msg1 = self.sh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"enable_global_syscache="
                                     f"{self.init_para1}")
        msg2 = self.sh.execute_gsguc('reload',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"enable_thread_pool="
                                     f"{self.init_para2}")
        step3_txt = '----重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step3_txt)
        restart_result = self.sh.restart_db_cluster()
        step4_txt = '----查询数据库状态; expect:状态正常----'
        self.log.info(step4_txt)
        status_result = self.sh.get_db_cluster_status('status')

        self.log.info(f'----{os.path.basename(__file__)}:end----')
        flag = drop_db_result.count(self.constant.DROP_DATABASE_SUCCESS)
        self.assertEqual(flag, self.db_num, '执行失败:' + step_txt + step1_txt)
        self.assertTrue(msg1, '执行失败:' + step_txt + step2_txt)
        self.assertTrue(msg2, '执行失败:' + step_txt + step2_txt)
        self.assertTrue(restart_result, '执行失败:' + step_txt + step3_txt)
        self.assertTrue(status_result, '执行失败:' + step_txt + step4_txt)

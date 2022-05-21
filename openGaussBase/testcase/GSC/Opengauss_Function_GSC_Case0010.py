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
Case Name   : global_syscache_threshold内存阈值修改后不重启数据库，验证参数值是否正确生效
Description :
    1、修改enable_global_syscache为on;
    2、重启数据库，使参数生效;
    3、修改global_syscache_threshold为20MB并查询;
    4、查看syscache占用情况;
    5、执行批量建表删除表函数创建，批量建表;
    6、进行表查询过程中，查看syscache占用情况;
    7、分批进行表查询;
Expect      :
    1、修改enable_global_syscache为on; 成功
    2、重启数据库，使参数生效;
    3、修改global_syscache_threshold为20MB并查询;
    4、查看syscache占用情况; 查询成功
    5、执行批量建表删除表函数创建，批量建表; 成功
    6、进行表查询过程中，查看syscache占用情况; 查询结果小于阈值*1.2
    7、分批进行表查询; 执行成功
History     :
"""
import os
import time
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
        self.table_num = 3000
        self.fun_create_name = 'fun_create_tb_gsc0010'
        self.fun_drop_name = 'fun_drop_tb_gsc0010'
        self.tb_ex_name = 'tb_gsc0010_'
        self.threshold = 20
        self.fun_create_tb = f'''
        drop function if exists  {self.fun_create_name};
        create or replace function {self.fun_create_name}(table_num integer)
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
        drop function if exists  {self.fun_drop_name};
        create or replace function {self.fun_drop_name}(
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
        self.check_sql = f"select sum(totalsize) total,sum(usedsize) used " \
            f"from gs_gsc_memory_detail;" \
            f"select sum(total_memory) from gs_gsc_dbstat_info();" \
            f"select count(*) from gs_gsc_table_detail() " \
            f"where relname like '{self.tb_ex_name}%';"

    def test_main(self):
        step_txt = '----step0:查看enable_global_syscache初始配置值;----'
        self.log.info(step_txt)
        self.init_para1 = self.com.show_param('enable_global_syscache')
        step_txt = '----step0:查看global_syscache_threshold初始值;----'
        self.log.info(step_txt)
        self.init_para2 = self.com.show_param('global_syscache_threshold')

        step_txt = '----step1:修改enable_global_syscache为on; ' \
                   'expect:成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= on")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step2:重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result)
        self.log.info('----查询参数----')

        self.new_para = self.com.show_param('enable_global_syscache')
        self.assertEqual(self.new_para, 'on', '执行失败:' + step_txt)

        step_txt = f'----step3:修改global_syscache_threshold为' \
            f'{self.threshold}MB并查询; expect:成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"global_syscache_threshold= "
                                    f"{self.threshold}MB")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----查询所有库并进行连接----'
        self.log.info(step_txt)
        db = "select datname from pg_database where datname " \
             "not like('template%');"
        result = self.sh.execut_db_sql(db)
        self.log.info(result)
        db_list = result.splitlines()[2:-1:1]
        for i in db_list:
            con_result = self.sh.execut_db_sql('select current_database();',
                                               dbname=f'{i}')
            self.log.info(con_result)
            self.assertIn(i, con_result, '执行失败:' + step_txt)

        step_txt = '----step4:查看syscache占用情况; expect:查询成功----'
        self.log.info(step_txt)
        result = self.sh.execut_db_sql(self.check_sql)
        self.log.info(result)

        step_txt = '----step5:执行批量建表删除表函数创建，批量建表; expect:成功----'
        self.log.info(step_txt)
        result = self.sh.execut_db_sql(self.fun_create_tb)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        result = self.sh.execut_db_sql(self.fun_drop_tb)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        self.log.info("--执行批量建表函数--")
        create_tb = f"select {self.fun_create_name}({self.table_num});"
        result = self.sh.execut_db_sql(create_tb)
        self.log.info(result)
        check_tb = f"select count(*) from pg_class where relname " \
            f"like '{self.tb_ex_name}%';"
        check_tb_result = self.sh.execut_db_sql(check_tb)
        self.log.info(result)
        self.assertEqual(int(check_tb_result.splitlines()[-2].strip()),
                         self.table_num, '执行失败:' + step_txt)

        step6_txt = '----step6:进行表查询过程中，查看syscache占用情况; ' \
                    'expect:查询结果小于阈值*1.2----'
        self.log.info(step6_txt)
        check_thread = ComThread(self.check_sys_cache, args=(20,))
        check_thread.setDaemon(True)
        check_thread.start()

        step_txt = '----step7: 分批进行表查询; expect:执行成功----'
        self.log.info(step_txt)
        select_sql = ''
        for i in range(int(self.table_num / 100)):
            for j in range(1, 100 + 1):
                select_sql = select_sql + \
                             f'select * from {self.tb_ex_name}{i * 100 + j};'
            select_result = self.sh.execut_db_sql(select_sql)
            self.assertEqual(select_result.count('0 rows'), 100,
                             '执行失败:' + step_txt)
            select_sql = ''

        check_thread.join()
        check_result = check_thread.get_result()
        self.log.info('check结果：' + check_result)
        rel_size = check_result.splitlines()[2].strip().split('|')[0]
        self.log.info('总占用', rel_size)
        self.assertLessEqual(int(rel_size),
                             int(self.threshold * 1024 * 1024 * 1.2),
                             '执行失败:' + step6_txt)

    def check_sys_cache(self, circle_num):
        result = ''
        for i in range(circle_num):
            result = self.sh.execut_db_sql(self.check_sql)
            self.log.info(result)
            time.sleep(1)
        return result

    def tearDown(self):
        step_txt = '----this is teardown----'
        self.log.info(step_txt)
        step1_txt = '----执行drop函数清除表; expect:删除成功----'
        self.log.info(step1_txt)
        drop_tb = f"select {self.fun_drop_name}({self.table_num});"
        result = self.sh.execut_db_sql(drop_tb)
        self.log.info(result)
        check_tb = f"select count(*) from pg_class where relname " \
            f"like '{self.tb_ex_name}%';"
        check_result = self.sh.execut_db_sql(check_tb)
        self.log.info(check_result)

        step2_txt = '----删除创建函数和删除函数; expect:设置成功----'
        self.log.info(step2_txt)
        drop_fun = f"drop function if exists  {self.fun_drop_name};" \
            f"drop function if exists  {self.fun_create_name};"
        drop_fun_msg = self.sh.execut_db_sql(drop_fun)
        self.log.info(drop_fun_msg)

        step3_txt = '----恢复参数为初始值并查询; expect:设置成功----'
        self.log.info(step3_txt)
        msg1 = self.sh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"enable_global_syscache="
                                     f"{self.init_para1}")
        msg2 = self.sh.execute_gsguc('reload',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"global_syscache_threshold="
                                     f"{self.init_para2}")
        step4_txt = '----重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step4_txt)
        restart_result = self.sh.restart_db_cluster()
        step5_txt = '----查询数据库状态; expect:状态正常----'
        self.log.info(step5_txt)
        status_result = self.sh.get_db_cluster_status('status')

        self.log.info(f'----{os.path.basename(__file__)}:end----')
        self.assertEqual(int(check_result.splitlines()[-2].strip()),
                         0, '执行失败:' + step1_txt)
        flag = drop_fun_msg.count(self.constant.DROP_FUNCTION_SUCCESS_MSG)
        self.assertEqual(flag, 2, '执行失败:' + step_txt + step2_txt)
        self.assertTrue(msg1, '执行失败:' + step_txt + step3_txt)
        self.assertTrue(msg2, '执行失败:' + step_txt + step3_txt)
        self.assertTrue(restart_result, '执行失败:' + step_txt + step4_txt)
        self.assertTrue(status_result, '执行失败:' + step_txt + step5_txt)

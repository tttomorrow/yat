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
Case Name   : gsc打开，非线程池模式下，并行/串行连接相同db，gsc缓存占用比对验证
Description :
    1、修改enable_global_syscache为on;enable_thread_pool为off;
    2、重启数据库，使参数生效;
    3、查询所有库并进行连接;
    4、查看syscache占用情况;
    5、创建数据库;
    6、新建库进行连接;
    7、查看syscache占用情况;
    8、多次串行对新建库进行连接;
    9、查看syscache占用情况;
    10、多次并行对新建库进行连接;
    11、查看syscache占用情况;
Expect      :
    1、修改enable_global_syscache为on;enable_thread_pool为off; 成功
    2、重启数据库，使参数生效; 重启成功
    3、查询所有库并进行连接; 连接成功
    4、查看syscache占用情况; 查询成功
    5、创建数据库; 创建成功
    6、新建库进行连接; 连接成功
    7、查看syscache占用情况; gsc缓存占用增加
    8、多次串行对新建库进行连接; 连接成功
    9、查看syscache占用情况; gsc缓存占用不变
    10、多次并行对新建库进行连接; 连接成功
    11、查看syscache占用情况; gsc缓存占用不变
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
        self.db_name = 'db_gsc0017'
        self.circle_num = 10

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

        step_txt = '----step3:查询所有库并进行连接; expect:连接成功----'
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

        step_txt = '----step4:查看syscache占用情况; expect:查询成功----'
        self.log.info(step_txt)
        check_sql = "select sum(totalsize) from gs_gsc_memory_detail ;" \
                    "select * from gs_gsc_memory_detail; "
        check_result = self.sh.execut_db_sql(check_sql)
        self.log.info(check_result)
        total_size1 = int(check_result.splitlines()[2].split()[0].strip())
        self.assertGreater(total_size1, 0, '执行失败:' + step_txt)

        step_txt = f'----step5:创建数据库; expect:创建成功----'
        self.log.info(step_txt)
        create_db = f'create database {self.db_name};'
        create_result = self.sh.execut_db_sql(create_db)
        self.log.info(create_result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS,
                      create_result, '执行失败:' + step_txt)

        step_txt = '----step6:新建库进行连接; expect:连接成功----'
        con_sql = "select current_database();" \
                  "select pg_sleep(3);" \
                  "select * from gs_gsc_memory_detail;"
        self.log.info(step_txt)
        con_result = self.sh.execut_db_sql(con_sql,
                                           dbname=f'{self.db_name}')
        self.log.info(con_result)
        self.assertIn(self.db_name, con_result, '执行失败:' + step_txt)

        step_txt = '----step7:查看syscache占用情况; expect:gsc缓存占用增加----'
        self.log.info(step_txt)
        check_result = self.sh.execut_db_sql(check_sql)
        self.log.info(check_result)
        total_size2 = int(check_result.splitlines()[2].split()[0].strip())
        self.assertGreater(total_size2, total_size1, '执行失败:' + step_txt)

        step_txt = '----step8:多次串行对新建库进行连接; expect:连接成功----'
        self.log.info(step_txt)
        for i in range(self.circle_num):
            con_result = self.sh.execut_db_sql(con_sql,
                                               dbname=f'{self.db_name}')
            self.log.info(con_result)
            self.assertIn(self.db_name, con_result, '执行失败:' + step_txt)

        step_txt = '----step9:查看syscache占用情况; expect:gsc缓存占用不变----'
        self.log.info(step_txt)
        check_result = self.sh.execut_db_sql(check_sql)
        self.log.info(check_result)
        total_size3 = int(check_result.splitlines()[2].split()[0].strip())
        self.assertEqual(total_size3, total_size2, '执行失败:' + step_txt)

        step_txt = '----step10:多次并行对新建库进行连接; expect:连接成功----'
        self.log.info(step_txt)
        connect_thread = []
        for i in range(self.circle_num):
            connect_thread.append(ComThread(self.sh.execut_db_sql,
                                            args=(con_sql, '',
                                                  f'{self.db_name}')))
            connect_thread[i].setDaemon(True)
            connect_thread[i].start()
        for i in range(self.circle_num):
            connect_thread[i].join(20)
            result = connect_thread[i].get_result()
            self.log.info(result)

        step_txt = '----step11:查看syscache占用情况; expect:gsc缓存占用不变----'
        self.log.info(step_txt)
        check_result = self.sh.execut_db_sql(check_sql)
        self.log.info(check_result)
        total_size4 = int(check_result.splitlines()[2].split()[0].strip())
        self.assertEqual(total_size4, total_size3, '执行失败:' + step_txt)

    def tearDown(self):
        step_txt = '----this is teardown----'
        self.log.info(step_txt)
        step1_txt = '----删除数据库 expect:删除成功----'
        self.log.info(step1_txt)
        drop_db = f'drop database {self.db_name}'
        drop_db_result = self.sh.execut_db_sql(drop_db)

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
        flag = self.constant.DROP_DATABASE_SUCCESS
        self.assertIn(flag, drop_db_result, '执行失败:' + step_txt + step1_txt)
        self.assertTrue(msg1, '执行失败:' + step_txt + step2_txt)
        self.assertTrue(msg2, '执行失败:' + step_txt + step2_txt)
        self.assertTrue(restart_result, '执行失败:' + step_txt + step3_txt)
        self.assertTrue(status_result, '执行失败:' + step_txt + step4_txt)

"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : 基础功能
Case Name   : 开启gpc时，并发执行ddl
Description :
    1.开启GPC
    2.重启数据库
    3.创建表
    4.创建prepare语句
    5.插入数据
    6.更新数据
    7.执行vacuum
    8.查询计划
Expect      :
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread


class Gpcclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_GPC_case0058 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.tb_name = "gpc_tb"
        self.pre_name = "gpc_tb_pre"

        result = self.commonshpri.execut_db_sql('show enable_thread_pool;')
        self.log.info(f"enable_thread_pool is {result}")
        self.enable_thread_pool = result.strip().splitlines()[-2]

        result = self.commonshpri.execut_db_sql(
            'show enable_global_plancache;')
        self.log.info(f"enable_global_plancache is {result}")
        self.enable_global_plancache = result.strip().splitlines()[-2]

    def test_index(self):
        self.log.info('-------------1.开启GPC-----------')
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG, "enable_thread_pool = on")
        self.assertTrue(result)
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            "enable_global_plancache = on")
        self.assertTrue(result)

        self.log.info('--------------2.重启数据库------------------')
        result = self.commonshpri.restart_db_cluster()
        self.assertTrue(result)

        self.log.info("---------------3.创建表----------------------")
        cmd = f"drop table if exists {self.tb_name};" \
            f"create table {self.tb_name}(i int) " \
            f"partition by range(i) " \
            f"(partition p1 values less than (100)," \
            f"partition p2 values less than (1000)," \
            f"partition p3 values less than(MAXVALUE));" \
            f"insert into {self.tb_name} values (generate_series(1,3999999);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info("------4.创建prepare语句-----")
        cmd = f"prepare {self.pre_name} as " \
            f"select count(*) from {self.tb_name};" \
            f"select pg_sleep(10);" \
            f"execute {self.pre_name};"
        pre_thread = ComThread(self.commonshpri.execut_db_sql, args=(cmd, ''))
        pre_thread.setDaemon(True)
        pre_thread.start()

        self.log.info("-----------5.插入数据------------------")
        cmd = f"insert into {self.tb_name} " \
            f"values (generate_series(1,1000000));"
        insert_thread = ComThread(self.commonshpri.execut_db_sql,
                                  args=(cmd, ''))
        insert_thread.setDaemon(True)
        insert_thread.start()

        self.log.info("------6.更新数据----")
        cmd = f"prepare {self.pre_name}1 as " \
            f"update {self.tb_name} set i=9999 where i<\$1;" \
            f"select pg_sleep(10);" \
            f"execute {self.pre_name}1(888);"
        update_thread = ComThread(
            self.commonshpri.execut_db_sql, args=(cmd, ''))
        update_thread.setDaemon(True)
        update_thread.start()

        self.log.info("------7.vacuum----")
        cmd = f"vacuum;"
        vacuum_thread = ComThread(self.commonshpri.execut_db_sql,
                                  args=(cmd, ''))
        vacuum_thread.setDaemon(True)
        vacuum_thread.start()

        self.log.info("------------获取结果-------------")
        pre_thread.join(60)
        result = pre_thread.get_result()
        self.log.info(result)
        self.assertIn('count', result)

        insert_thread.join(600)
        result = insert_thread.get_result()
        self.log.info(result)
        self.assertIn('INSERT', result)

        update_thread.join(600)
        result = update_thread.get_result()
        self.log.info(result)
        self.assertIn('UPDATE', result)

        vacuum_thread.join(600)
        result = vacuum_thread.get_result()
        self.log.info(result)
        self.assertIn('VACUUM', result)

        self.log.info("-----------8 查询计划------------------")
        cmd = f"select * from dbe_perf.global_plancache_status; "
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('prepare gpc_tb_pre as '
                      'select count(*) from gpc_tb;', result)
        self.assertIn('prepare gpc_tb_pre1 as '
                      'update gpc_tb set i=9999 where i<$1;', result)
        result = self.commonshpri.get_db_cluster_status("status")
        self.assertTrue(result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"drop table if exists {self.tb_name} cascade;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)

        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_thread_pool = {self.enable_thread_pool}")
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_global_plancache = {self.enable_global_plancache}")

        self.commonshpri.restart_db_cluster()
        self.log.info("-Opengauss_Function_GPC_case0058 end-")

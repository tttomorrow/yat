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
Case Name   : 使用GLOBAL_PLANCACHE_CLEAN清除无效缓存
Description :
    1.开启GPC
    2.重启数据库
    3.创建表
    4.开启三个session创建语句
    5.查询计划(保持之前三个session不退出)
Expect      :
History     :
"""
import unittest
import time
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread


class Gpcclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_GPC_case0050 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.tb_name = "gpc_tb"
        self.tb_name1 = "gpc_tb1"
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
        cmd = f"create  table {self.tb_name}(i int, j int);" \
            f"create table {self.tb_name1}(i int, j int);" \
            f"insert into {self.tb_name} values(1,2),(2,3);" \
            f"insert into {self.tb_name1} values(1,5),(2,5);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info("------开启3个session-----")
        session = []
        sql = f"prepare {self.pre_name}(int, int) as " \
            f"merge into {self.tb_name} t1 using {self.tb_name1} t2 " \
            f"on (t1.i=t2.i) when matched " \
            f"then update set t1.j=t2.j " \
            f"when not matched then insert values(\$1, \$2);" \
            f"execute {self.pre_name}(4,6);select * from {self.tb_name}; " \
            f"select pg_sleep(40);"
        for i in range(3):
            session.append(
                ComThread(self.commonshpri.execut_db_sql, args=(sql, '')))
        for i in range(3):
            session[i].setDaemon(True)
            session[i].start()

        self.log.info("--------------开启一个session，执行后退出-----------")
        sql = f"prepare {self.pre_name}1 as select count(*) " \
            f"from {self.tb_name}; execute {self.pre_name}1;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)

        self.log.info("-----------查询计划------------------")
        time.sleep(2)
        cmd = f"select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(2 rows)', result)

        self.log.info("--------------删除计划---------------")
        sql = "select * from dbe_perf.GLOBAL_PLANCACHE_CLEAN;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('t', result)
        sql = "select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('(1 row)', result)

        self.log.info("-----------获取线程结果----------------")
        for i in range(3):
            session[i].join(40)
            result = session[i].get_result()
            self.log.info(result)
            self.assertIn('PREPARE', result)

        self.log.info("-----------查询计划------------------")
        time.sleep(2)
        cmd = f"select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(1 row)', result)

        self.log.info("--------------删除计划---------------")
        sql = "select * from dbe_perf.GLOBAL_PLANCACHE_CLEAN;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('t', result)
        sql = "select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('(0 rows)', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"drop table if exists {self.tb_name} cascade;" \
            f"drop table if exists {self.tb_name1} cascade;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)

        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_thread_pool = {self.enable_thread_pool}")
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_global_plancache = {self.enable_global_plancache}")

        self.commonshpri.restart_db_cluster()
        self.log.info("-Opengauss_Function_GPC_case0050 end-")

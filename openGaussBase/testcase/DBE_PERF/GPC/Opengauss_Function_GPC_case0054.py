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
Case Name   : 修改gpc_clean_timeout
Description :
    1.开启GPC，并修改gpc_clean_timeout
    2.重启数据库
    3.创建表
    4.创建prepare语句
    5.调用p1_1
    6.等待10min查询计划,极端为15min
Expect      :
History     :
"""
import unittest
import time
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class Gpcclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_GPC_case0054 start")
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

        result = self.commonshpri.execut_db_sql(
            'show gpc_clean_timeout;')
        self.log.info(f"gpc_clean_timeout is {result}")

    def test_index(self):
        self.log.info('---------1.开启GPC,并修改enable_global_plancache---')
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG, "enable_thread_pool = on")
        self.assertTrue(result)
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            "enable_global_plancache = on")
        self.assertTrue(result)
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            "gpc_clean_timeout = 600")
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
            f"partition p3 values less than(MAXVALUE));"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info("------4.创建prepare语句5.执行prepare6.查询计划-----")
        cmd = f"prepare {self.pre_name} as " \
            f"select * from {self.tb_name};" \
            f"execute {self.pre_name};" \
            f"select * from dbe_perf.global_plancache_status " \
            f"where query='prepare {self.pre_name} " \
            f"as select * from {self.tb_name};' " \
            f"and valid = 't';"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, result)
        self.assertIn('0 rows', result)
        self.assertIn('as select * from', result)

        self.log.info("----------7.查询计划------------------")
        time.sleep(300)
        cmd = f"select * from dbe_perf.global_plancache_status ;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(1 row)', result)
        time.sleep(400)
        cmd = f"select * from dbe_perf.global_plancache_status ;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        time.sleep(200)
        cmd = f"select * from dbe_perf.global_plancache_status ;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(0 rows)', result)

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
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"gpc_clean_timeout = 1800")

        self.commonshpri.restart_db_cluster()
        self.log.info("-Opengauss_Function_GPC_case0054 end-")

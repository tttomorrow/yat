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
Case Name   : 不同schema下同名表创建缓存不共享
Description :
    1.开启GPC，并修改gpc_clean_timeout大于1h
    2.重启数据库
    3.创建模式创建表
    4.创建prepare语句(session 1)
    5.创建prepare语句(session 2)
    6.查询计划
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
        self.log.info("Opengauss_Function_GPC_case0053 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.tb_name = "gpc_tb"
        self.pre_name = "gpc_tb_pre"
        self.schema_name = "gpc_test"

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
        cmd = f"create schema {self.schema_name};" \
            f"create table if not exists {self.tb_name}(i int);" \
            f"create table if not exists " \
            f"{self.schema_name}.{self.tb_name}(i int);" \
            f"create index i on {self.tb_name}(i);" \
            f"create index i1 on {self.schema_name}.{self.tb_name}(i);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info("------4.创建prepare语句-----")
        cmd = f"prepare {self.pre_name} as " \
            f"select * from {self.tb_name} where i>99;" \
            f"explain execute {self.pre_name};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, result)

        self.log.info("------5.创建prepare语句-----")
        cmd = f"prepare {self.pre_name} as " \
            f"select * from {self.schema_name}.{self.tb_name} where i>99 ;" \
            f"explain execute {self.pre_name};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, result)

        self.log.info("-----------6.查询计划------------------")
        cmd = f"select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(2 rows)', result)

        self.log.info("----------------7.插入数据------------")
        cmd = f"insert into {self.tb_name} " \
            f"values(generate_series(1,999999));" \
            f"insert into {self.schema_name}.{self.tb_name} " \
            f"values(generate_series(1,999999));" \
            f"analyze;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('INSERT', result)

        self.log.info("------8.创建prepare语句-----")
        cmd = f"prepare {self.pre_name} as " \
            f"select * from {self.tb_name} where i>99;" \
            f"explain execute {self.pre_name};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, result)

        self.log.info("------9.创建prepare语句-----")
        cmd = f"prepare {self.pre_name} as " \
            f"select * from {self.schema_name}.{self.tb_name} where i>99 ;" \
            f"explain execute {self.pre_name};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, result)

        self.log.info("-----------10.查询计划------------------")
        cmd = f"select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(2 rows)', result)


    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')

        cmd = f"drop table if exists {self.tb_name} cascade;" \
            f"drop table if exists " \
            f"{self.schema_name}.{self.tb_name} cascade;" \
            f"drop schema if exists {self.schema_name};"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)

        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_thread_pool = {self.enable_thread_pool}")
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_global_plancache = {self.enable_global_plancache}")

        self.commonshpri.restart_db_cluster()
        self.log.info("-Opengauss_Function_GPC_case0053 end-")

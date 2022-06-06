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
Case Type   : 基础功能
Case Name   : 开启gpc的同时开启bypass，并更新数据
Description :
    1.开启GPC,并开启bypass
    2.重启数据库
    3.创建表及索引
    4.创建prepare
    5.查询视图
    6.插入并更新数据
    7.执行计划
    8.查询视图
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
        self.log.info("Opengauss_Function_GPC_case0038 start")
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
            'show enable_opfusion;')
        self.log.info(f"enable_opfusion is {result}")
        self.enable_opfusion = result.strip().splitlines()[-2]

        result = self.commonshpri.execut_db_sql(
            'show enable_bitmapscan;')
        self.log.info(f"enable_bitmapscan is {result}")
        self.enable_bitmapscan = result.strip().splitlines()[-2]

        result = self.commonshpri.execut_db_sql(
            'show enable_seqscan;')
        self.log.info(f"enable_seqscan is {result}")
        self.enable_seqscan = result.strip().splitlines()[-2]

        result = self.commonshpri.execut_db_sql(
            'show opfusion_debug_mode;')
        self.log.info(f"opfusion_debug_mode is {result}")
        self.opfusion_debug_mode = result.strip().splitlines()[-2]

    def test_index(self):
        self.log.info('-------------1.开启GPC-----------')
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG, "enable_thread_pool = on")
        self.assertTrue(result)
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            "enable_global_plancache = on")
        self.assertTrue(result)
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG, "enable_opfusion=on")
        self.assertTrue(result)
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            "enable_bitmapscan=on")
        self.assertTrue(result)
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG, "enable_seqscan=on")
        self.assertTrue(result)
        result = self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            "opfusion_debug_mode = off")
        self.assertTrue(result)

        self.log.info('--------------2.重启数据库------------------')
        result = self.commonshpri.restart_db_cluster()
        self.assertTrue(result)

        self.log.info("---------------3.创建表----------------------")
        cmd = f"create table {self.tb_name}(a int, b int, c int);" \
            f"create index i_x on {self.tb_name}(b);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info("---------------4.创建缓存----------------------")
        cmd = f"prepare {self.pre_name}(int) as " \
            f"select a from {self.tb_name} where b=\$1;" \
            f"explain execute {self.pre_name}(1);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, result)
        self.assertIn("Bitmap Heap Scan", result)

        self.log.info("-----------查询计划------------------")
        time.sleep(2)
        cmd = f"select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('select a from ', result)

        self.log.info("-----------6.插入并更新数据----------------")
        cmd = f"insert into {self.tb_name}(a) " \
            f"values (generate_series(1,10000)); " \
            f"update {self.tb_name} set b = a, c= a;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)

        self.log.info("-----------7查询计划------------------")
        time.sleep(2)
        cmd = f"select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('select a from ', result)

        self.log.info("---------------8.创建缓存----------------------")
        cmd = f"prepare {self.pre_name}(int) as " \
            f"select a from {self.tb_name} where b=\$1;analyze;" \
            f"explain execute {self.pre_name}(1);" \
            f"analyze;explain execute {self.pre_name}(1);"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG, result)
        self.assertIn("Bypass", result)
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
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_opfusion={self.enable_opfusion}")
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_bitmapscan={self.enable_bitmapscan}")
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_seqscan={self.enable_seqscan}")
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"opfusion_debug_mode = {self.opfusion_debug_mode}")

        self.commonshpri.restart_db_cluster()
        self.log.info("-Opengauss_Function_GPC_case0038 end-")

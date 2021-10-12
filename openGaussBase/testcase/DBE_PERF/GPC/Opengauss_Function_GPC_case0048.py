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
Case Name   : 备升主后gpc功能正常
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

commonshpri = CommonSH('PrimaryDbUser')


@unittest.skipIf(' 6002 ' not in commonshpri.get_db_cluster_status('detail'),
                 'Single node, and subsequent codes are not executed.')
class Gpcclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_GPC_case0048 start")
        self.constant = Constant()
        self.commonshsta = CommonSH('Standby1DbUser')
        self.tb_name = "gpc_tb"
        self.pre_name = "gpc_tb_pre"

        result = commonshpri.execut_db_sql('show enable_thread_pool;')
        self.log.info(f"enable_thread_pool is {result}")
        self.enable_thread_pool = result.strip().splitlines()[-2]

        result = commonshpri.execut_db_sql(
            'show enable_global_plancache;')
        self.log.info(f"enable_global_plancache is {result}")
        self.enable_global_plancache = result.strip().splitlines()[-2]

    def test_index(self):
        self.log.info('-------------1.开启GPC-----------')
        result = commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG, "enable_thread_pool = on")
        self.assertTrue(result)
        result = commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            "enable_global_plancache = on")
        self.assertTrue(result)

        self.log.info('--------------2.重启数据库------------------')
        result = commonshpri.restart_db_cluster()
        self.assertTrue(result)

        self.log.info("-------------备升主-------------------")
        result = commonshpri.stop_db_instance()
        self.log.info(result)
        self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, result)
        result = self.commonshsta.execute_gsctl(
            'failover', self.constant.FAILOVER_SUCCESS_MSG)
        self.assertTrue(result)
        result = self.commonshsta.exec_refresh_conf()
        self.assertTrue(result)

        self.log.info("---------------3.创建表----------------------")
        cmd = f"create table {self.tb_name}(i int );" \
            f"insert into {self.tb_name} values(1);"
        result = self.commonshsta.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

        self.log.info("------开启3个session-----")
        session = []
        sql = f"prepare {self.pre_name} " \
            f"as update {self.tb_name} set i =5 where i=1;" \
            f"execute {self.pre_name};" \
            f"select * from {self.tb_name}; " \
            f"select pg_sleep(30);"
        for i in range(3):
            session.append(
                ComThread(self.commonshsta.execut_db_sql, args=(sql, '')))
        for i in range(3):
            session[i].setDaemon(True)
            session[i].start()

        self.log.info("-----------查询计划------------------")
        time.sleep(2)
        cmd = f"select * from dbe_perf.global_plancache_status " \
            f"where query='prepare {self.pre_name} as update " \
            f"{self.tb_name} set i =5 where i=1;' " \
            f"and refcount = 3 and valid='t';"
        result = self.commonshsta.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(1 row)', result)

        self.log.info("-----------获取线程结果----------------")
        for i in range(3):
            session[i].join(30)
            result = session[i].get_result()
            self.log.info(result)
            self.assertIn('UPDATE', result)

        self.log.info("-----------查询计划------------------")
        time.sleep(2)
        cmd = f"select * from dbe_perf.global_plancache_status " \
            f"where query='prepare {self.pre_name} as update " \
            f"{self.tb_name} set i =5 where i=1;' " \
            f"and refcount = 0 and valid='t';"
        result = self.commonshsta.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(1 row)', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"drop table if exists {self.tb_name} cascade;"
        result = self.commonshsta.execut_db_sql(cmd)
        self.log.info(result)

        self.log.info('---------主备还原------------------')
        result = commonshpri.start_db_instance('standby')
        self.log.info(result)

        commonshpri.execute_gsctl(
            'switchover', self.constant.SWITCH_SUCCESS_MSG)
        commonshpri.exec_refresh_conf()

        commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_thread_pool = {self.enable_thread_pool}")
        commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_global_plancache = {self.enable_global_plancache}")

        commonshpri.restart_db_cluster()
        self.log.info("-Opengauss_Function_GPC_case0048 end-")

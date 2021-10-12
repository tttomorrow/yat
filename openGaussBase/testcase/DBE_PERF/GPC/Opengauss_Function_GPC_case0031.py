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
Case Name   : 不同用户间缓存共享
Description :
    1.开启GPC
    2.重启数据库
    3.创建用户
    4.使用初始用户test在session1创建prepare
    5.使用普通用户在session2创建相同prepare
    6.查询缓存计划
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.存在缓存，不同用户间不共享
History     :
"""
import unittest
import time
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread


class Gpcclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_GPC_case0031 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.tb_name = "gpc_tb"
        self.pre_name = "gpc_tb_pre"
        self.user = "pre_test"
        self.password = "test@123"

        result = self.commonshpri.execut_db_sql('show enable_thread_pool;')
        self.log.info(f"enable_thread_pool is {result}")
        self.enable_thread_pool = result.strip().splitlines()[-2]

        result = self.commonshpri.execut_db_sql(
            'show enable_global_plancache;')
        self.log.info(f"enable_global_plancache is {result}")
        self.enable_global_plancache = result.strip().splitlines()[-2]
        self.db_primary_user_node = Node(node='PrimaryDbUser')

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

        self.log.info("--------------3.创建用户----------------------")
        cmd = f"create user {self.user} with password '{self.password}';" \
            f"grant all privileges to {self.user};" \
            f"grant {self.db_primary_user_node.ssh_user} to {self.user};"
        result = self.commonshpri.execut_db_sql(
            cmd,
            sql_type=f"-U {self.db_primary_user_node.ssh_user} "
            f"-W {self.db_primary_user_node.ssh_password}")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result)

        self.log.info("------4.使用初始用户test在session1创建prepare-----")
        sql = f"create table {self.tb_name}(a int, b int, c int);" \
            f"prepare {self.pre_name}(int) as " \
            f"select a from {self.tb_name} where b=\$1;" \
            f"execute {self.pre_name}(1);" \
            f"analyze ;" \
            f"explain execute {self.pre_name}(1);" \
            f"select pg_sleep(30);"
        sql_type = f"-U {self.db_primary_user_node.ssh_user} "
        f"-W {self.db_primary_user_node.ssh_password}"
        ini_thread = ComThread(self.commonshpri.execut_db_sql,
                               args=(sql, sql_type))
        ini_thread.setDaemon(True)
        ini_thread.start()

        self.log.info("------------5.使用普通用户在session2创建相同prepare-------------")
        time.sleep(5)
        cmd = f"prepare {self.pre_name}(int) " \
            f"as select a from {self.tb_name} where b=\$1;" \
            f"execute {self.pre_name}(1);" \
            f"analyze ;" \
            f"explain execute {self.pre_name}(1);" \
            f"select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(
            cmd,
            sql_type=f"-U {self.user} -W {self.password}")
        self.log.info(result)
        self.assertIn(self.constant.ANALYZE_SUCCESS_MSG, result)
        self.assertEqual(result.count(
            "prepare gpc_tb_pre(int) as select a from gpc_tb where "), 2)

        self.log.info("-----------查询计划------------------")
        time.sleep(2)
        cmd = f"select * from {self.tb_name};" \
            f"select * from dbe_perf.global_plancache_status;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)
        self.assertIn('(2 rows)', result)
        self.assertEqual(result.count(
            "prepare gpc_tb_pre(int) as select a from gpc_tb where "), 2)

        self.log.info("-----------获取线程结果----------------")
        ini_thread.join(30)
        result = ini_thread.get_result()
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = f"drop table if exists {self.tb_name} cascade;" \
            f"drop user if exists {self.user} cascade;"
        result = self.commonshpri.execut_db_sql(cmd)
        self.log.info(result)

        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_thread_pool = {self.enable_thread_pool}")
        self.commonshpri.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
            f"enable_global_plancache = {self.enable_global_plancache}")

        self.commonshpri.restart_db_cluster()
        self.log.info("-Opengauss_Function_GPC_case0031 end-")

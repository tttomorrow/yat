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
Case Type   : GUC
Case Name   : 使用gs_guc reload方式修改job_queue_processes为100，观察预期结果；
Description :
    1、查询job_queue_processes默认值,show job_queue_processes;
    2、使用gs_guc reload方式修改job_queue_processes为100，
       gs_guc reload -D {cluster/dn1} -c "job_queue_processes=100";
       并校验其预期结果，show query_band;
    3、重启后做简单DML
    4、恢复默认值；
Expect      :
    1、显示默认值；
    2、参数修改成功，校验系统参数值；
    3、DML无报错；
    4、恢复默认值成功；
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0025开始执行===")
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        self.table = 'test'
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询job_queue_processes期望，默认值10======")
        sql_cmd1 = self.commonsh.execut_db_sql('''show job_queue_processes;''')
        logger.info(sql_cmd1)
        self.assertEqual("10", sql_cmd1.split("\n")[-2].strip())

        logger.info("======修改job_queue_processes为100，期望：不重启设置失败======")
        result = self.commonsh.execute_gsguc('reload',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                            "job_queue_processes=100")
        self.assertTrue(result)

        logger.info("======期望：查询结果为默认值10======")
        sql_cmd2 = self.commonsh.execut_db_sql('''show job_queue_processes;''')
        logger.info(sql_cmd2)
        self.assertIn("10", sql_cmd2)

        logger.info("======执行相关DML======")
        sql_cmd3 = f'''drop table if exists {self.table} cascade;
            create table {self.table}(c_int int);
            insert into {self.table} values(1),(2);
            update {self.table} set c_int = 5 where c_int = 1;
            delete from {self.table} where c_int = 2;
            select * from {self.table};
            '''
        result = self.commonsh.execut_db_sql(sql_cmd3)
        logger.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result)

        logger.info("======恢复默认值 & 删除表======")
        sql_cmd = f'''drop table {self.table} cascade;'''
        result_sql = self.commonsh.execut_db_sql(sql_cmd)
        logger.info(result_sql)
        result_set = self.commonsh.execut_db_sql('''alter system set 
            job_queue_processes to 10;''')
        self.assertIn(self.constant.ALTER_SYSTEM_SUCCESS_MSG, result_set)
        result = self.commonsh.restart_db_cluster()
        self.assertTrue(result)

    def tearDown(self):
        logger.info("======恢复默认值======")
        sql_cmd = self.commonsh.execut_db_sql('''show job_queue_processes; ''')
        logger.info(sql_cmd)
        if "10" not in sql_cmd.split('\n')[-2].strip():
            self.commonsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       "job_queue_processes=10")
            result = self.commonsh.restart_db_cluster()
            logger.info(result)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0025执行结束===")

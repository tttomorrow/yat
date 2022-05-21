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
Case Type   : Query_Dop并行查询
Case Name   : 设置query_dop=2,创建并执行function查询（若能正确执行就说明不支持并行查询）
Description :
    1、创建测试表
    2、向表中插入数据
    3、设置query_dop参数值为2
    4、重启数据库集群使参数生效
    5、创建并执行function查询，是否启用并行查询
    6、清理环境
Expect      :
    1、创建测试表成功
    2、插入数据成功
    3、设置query_dop参数值为2成功
    4、重启数据库集群成功
    5、创建并执行function操作成功，不支持并行查询
    6、清理环境成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class QueryDopCase(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0024开始执行---")
        self.constant = Constant()
        self.commonsh = CommonSH("PrimaryDbUser")
        self.common = Common()
        self.initial_query_dop = self.common.show_param("query_dop")
        self.t_name_sc = "t_score_0024"
        self.func_name = "func_loop_0024"

    def test_query_dop(self):
        step1_text = "---step1:创建测试表;expect:建表成功---"
        self.logger.info(step1_text)
        sql_cmd1 = f'''drop table if exists {self.t_name_sc};
            create table {self.t_name_sc}(
            s_id int,
            s_score int,
            c_id int);'''
        self.logger.info(sql_cmd1)
        sql_res1 = self.commonsh.execut_db_sql(sql_cmd1)
        self.logger.info(sql_res1)
        self.assertIn("CREATE TABLE", sql_res1, "执行失败" + step1_text)

        step2_text = "---step2:为测试表插入数据;expect:插入数据成功---"
        self.logger.info(step2_text)
        sql_cmd2 = f'''insert into {self.t_name_sc} values(
            generate_series(1, 1000000), 
            random()*100,
            generate_series(1, 1000000));'''
        self.logger.info(sql_cmd2)
        sql_res2 = self.commonsh.execut_db_sql(sql_cmd2)
        self.logger.info(sql_res2)
        self.assertIn("INSERT", sql_res2, "执行失败:" + step2_text)

        step3_text = "---step3:设置query_dop参数值为2;expect:设置成功---"
        self.logger.info(step3_text)
        guc_cmd = self.commonsh.execute_gsguc("set",
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              "query_dop = 2")
        self.logger.info(guc_cmd)
        self.assertTrue(guc_cmd, "执行失败:" + step3_text)

        step4_text = "---step4:重启数据库集群;expect:重启成功---"
        self.logger.info(step4_text)
        gs_cmd = self.commonsh.restart_db_cluster()
        self.logger.info(gs_cmd)
        self.logger.info("---检查数据库状态是否正常---")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        step5_text = "---step5:创建并执行function查询;expect:成功执行,不支持并行查询---"
        self.logger.info(step5_text)
        function_cmd = self.commonsh.execut_db_sql(
            f'''create or replace function {self.func_name} return int 
                as 
                exp int;
                begin
                select count(*) from {self.t_name_sc} into exp;
                return exp;
                end;''')
        self.logger.info(function_cmd)
        function_res = self.commonsh.execut_db_sql(
            f'select {self.func_name}();')
        self.logger.info(function_res)
        assert_info = f'{self.func_name}'
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG,
                      function_cmd, "执行失败:" + step5_text)
        self.assertIn(assert_info, function_res, "执行失败:" + step5_text)

    def tearDown(self):
        self.logger.info("---清理环境---")

        drop_text = "---step:删除表及function;expect:删除成功---"
        self.logger.info(drop_text)
        drop_cmd = f'''drop function if exists {self.func_name};
            drop table if exists {self.t_name_sc};'''
        self.logger.info(drop_cmd)
        drop_res = self.commonsh.execut_db_sql(drop_cmd)
        self.logger.info(drop_res)

        reset_text = "---step:重置query_dop参数值;expect:重置成功---"
        self.logger.info(reset_text)
        re_cmd = self.commonsh.execute_gsguc("set",
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f"query_dop = "
                                             f"{self.initial_query_dop}")
        self.logger.info(re_cmd)

        restart_text = "---step:重启数据库集群;expect:重启成功---"
        self.logger.info(restart_text)
        restart_cmd = self.commonsh.restart_db_cluster()
        self.logger.info(restart_cmd)
        self.logger.info("---检查数据库状态是否正常---")
        status_res = self.commonsh.get_db_cluster_status()

        self.assertIn("DROP TABLE", drop_res, "执行失败" + drop_text)
        self.assertIn("DROP FUNCTION", drop_res, "执行失败" + drop_text)
        self.assertTrue(re_cmd, "执行失败:" + reset_text)
        self.assertTrue("Degraded" in status_res or "Normal" in status_res)
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0024执行结束---")

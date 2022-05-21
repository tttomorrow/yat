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
Case Name   : 创建范围分区表,设置query_dop=2，使用join的查询执行explain，查看是否启用并行查询
Description :
    1、创建范围分区表
    2、向分区表中插入数据
    3、设置query_dop参数值为2
    4、重启数据库集群使参数生效
    5、对分区表执行analyze操作
    6、使用explain查看分区表是否启用并行查询
    7、清理环境
Expect      :
    1、创建范围分区表
    2、插入数据成功
    3、设置query_dop参数值为2成功
    4、重启数据库集群成功
    5、对分区表执行analyze操作成功
    6、使用explain查看分区表，成功启用并行查询
    7、清理环境成功
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
            "---Opengauss_Function_Tools_Query_Dop_Case0013开始执行---")
        self.constant = Constant()
        self.commonsh = CommonSH("PrimaryDbUser")
        self.common = Common()
        self.initial_query_dop = self.common.show_param("query_dop")
        self.t_name_sc = "t_score_0013"
        self.t_name_stu = "t_student_0013"

    def test_query_dop(self):
        step1_text = "---step1:创建范围分区表;expect:建表成功---"
        self.logger.info(step1_text)
        sql_cmd1 = f'''drop table if exists {self.t_name_sc};
            create table {self.t_name_sc}(
            s_id int,
            s_score int,
            s_course char(8))
            partition by range (s_score)
            (partition score_p1
            values less than (60),
            partition score_p2
            values less than (1000001));
            drop table if exists {self.t_name_stu};
            create table {self.t_name_stu}(
            s_id int,
            s_name char(8));'''
        self.logger.info(sql_cmd1)
        sql_res1 = self.commonsh.execut_db_sql(sql_cmd1)
        self.logger.info(sql_res1)
        self.assertIn("CREATE TABLE", sql_res1, "执行失败" + step1_text)

        step2_text = "---step2:为范围分区表插入数据;expect:插入数据成功---"
        self.logger.info(step2_text)
        sql_cmd2 = f'''insert into {self.t_name_sc} values(
            generate_series(1, 1000000), 
            generate_series(1, 1000000),
            'course');
            insert into {self.t_name_stu} values(
            generate_series(1, 1000000), 
            'name');'''
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

        step5_text = "---step5:对分区表执行analyze操作;expect:操作成功---"
        self.logger.info(step5_text)
        analyse_res = self.commonsh.execut_db_sql(
            f'''analyze {self.t_name_sc};
                analyze {self.t_name_stu};''')
        self.logger.info(analyse_res)
        self.assertIn("ANALYZE", analyse_res, "执行失败:" + step5_text)

        step6_text = "---step6:explain查看是否启用并行查询;expect:并行查询启用成功---"
        self.logger.info(step6_text)
        explain_res = self.commonsh.execut_db_sql(
            f'''explain 
            select b.s_id,b.s_name,ROUND(AVG(a.s_score),2) as avg_score 
            from {self.t_name_stu} b left join {self.t_name_sc} a 
            on b.s_id = a.s_id 
            GROUP BY b.s_id,b.s_name 
            HAVING avg_score < 60 union 
            select a.s_id,a.s_name,0 as avg_score 
            from {self.t_name_stu} a 
            where a.s_id not in (
                select distinct s_id from {self.t_name_sc});''')
        self.logger.info(explain_res)
        self.assertIn("Streaming(type: LOCAL GATHER dop: 1/2)",
                      explain_res, "执行失败:" + step6_text)

    def tearDown(self):
        self.logger.info("---清理环境---")

        drop_text = "---删除分区表---"
        self.logger.info(drop_text)
        drop_cmd = f'''drop table if exists {self.t_name_sc};
            drop table if exists {self.t_name_stu};'''
        self.logger.info(drop_cmd)
        drop_res = self.commonsh.execut_db_sql(drop_cmd)
        self.logger.info(drop_res)

        reset_text = "---重置query_dop参数值---"
        self.logger.info(reset_text)
        re_cmd = self.commonsh.execute_gsguc("set",
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f"query_dop = "
                                             f"{self.initial_query_dop}")
        self.logger.info(re_cmd)

        restart_text = "---重启数据库集群---"
        self.logger.info(restart_text)
        restart_cmd = self.commonsh.restart_db_cluster()
        self.logger.info(restart_cmd)
        self.logger.info("---检查数据库状态是否正常---")
        status_res = self.commonsh.get_db_cluster_status()

        self.assertTrue(drop_res.count(self.constant.TABLE_DROP_SUCCESS)
                        == 2, "执行失败" + drop_text)
        self.assertTrue(re_cmd, "执行失败:" + reset_text)
        self.assertTrue("Degraded" in status_res or "Normal" in status_res)
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0013执行结束---")

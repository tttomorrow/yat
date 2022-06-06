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
Case Name   : 开启并行查询，执行查询，查看视图pgxc_thread_wait_status
Description :
    1、创建测试表
    2、向测试表中插入数据
    3、设置各参数的值query_dop=8并执行查询、查看视图
    4、清理环境
Expect      :
    1、创建测试表成功
    2、插入数据成功
    3、设置各参数的值query_dop=8并执行查询、查看视图
    4、清理环境
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
            "---Opengauss_Function_Tools_Query_Dop_Case0033开始执行---")
        self.constant = Constant()
        self.commonsh = CommonSH("PrimaryDbUser")
        self.t_name_sc = "t_score_0033"

    def test_query_dop(self):
        step1_text = "---step1:创建测试表;expect:建表成功---"
        self.logger.info(step1_text)
        sql_cmd1 = f'''drop table if exists {self.t_name_sc};
            CREATE TABLE {self.t_name_sc}(
            s_id int,
            s_score int,
            s_course char(8),
            c_id int);'''
        self.logger.info(sql_cmd1)
        sql_res1 = self.commonsh.execut_db_sql(sql_cmd1)
        self.logger.info(sql_res1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS,
                      sql_res1, "执行失败" + step1_text)

        step2_text = "---step2:为测试表插入数据;expect:插入数据成功---"
        self.logger.info(step2_text)
        sql_cmd2 = f'''insert into {self.t_name_sc} values(
            generate_series(1, 1000000), 
            random()*100,
            'course',
            generate_series(1, 1000000));'''
        self.logger.info(sql_cmd2)
        sql_res2 = self.commonsh.execut_db_sql(sql_cmd2)
        self.logger.info(sql_res2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                      sql_res2, "执行失败:" + step2_text)

        step3_text = "---step3:设置参数的值并执行查询;expect:设置成功---"
        self.logger.info(step3_text)
        sql_cmd3 = f'''SET query_dop TO 8;

            --执行查询
            select count(*) from bmsql_history;

            --查看视图
            select * from pgxc_thread_wait_status;'''
        self.logger.info(sql_cmd3)
        sql_res3 = self.commonsh.execut_db_sql(sql_cmd3)
        self.logger.info(sql_res3)
        self.assertIn(" unsupported view in single node mode",
                      sql_res3, "执行失败:" + step3_text)

    def tearDown(self):
        self.logger.info("---清理环境---")

        drop_text = "---step:删除测试表;expect:删除成功---"
        self.logger.info(drop_text)
        drop_cmd = f'''drop table if exists {self.t_name_sc};'''
        self.logger.info(drop_cmd)
        drop_res = self.commonsh.execut_db_sql(drop_cmd)
        self.logger.info(drop_res)

        self.assertIn(self.constant.DROP_TABLE_SUCCESS,
                      drop_res, '执行失败:' + drop_text)
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0033执行结束---")

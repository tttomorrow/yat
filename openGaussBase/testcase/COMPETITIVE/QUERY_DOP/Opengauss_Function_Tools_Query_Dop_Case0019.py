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
Case Name   : 创建本地临时,设置query_dop=2,执行explain，查看是否启用并行查询
Description :
    1、创建本地临时表
    2、向表中插入数据
    3、设置query_dop参数值为2
    4、对临时表执行analyze操作
    5、使用explain查看临时表是否启用并行查询
    6、清理环境
Expect      :
    1、创建本地临时表成功
    2、插入数据成功
    3、设置query_dop参数值为2成功
    4、对临时表执行analyze操作成功
    5、使用explain查看临时表，成功启用并行查询
    6、清理环境成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class QueryDopCase(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0019开始执行---")
        self.commonsh = CommonSH("PrimaryDbUser")
        self.t_name_sc = "t_score_0019"
        self.t_name_stu = "t_student_0019"

    def test_query_dop(self):
        step_text = "---step:创建本地临时表;expect:建表成功---"
        self.logger.info(step_text)
        sql_cmd = f'''
            --创建本地临时表
            drop table if exists {self.t_name_sc};
            create local temp table {self.t_name_sc}(
            s_id int,
            s_score int,
            c_id int);
            drop table if exists {self.t_name_stu};
            create local temp table {self.t_name_stu}(
            s_id int,
            s_name char(8));
            
            --插入数据
            insert into {self.t_name_sc} values(
            generate_series(1, 1000000), 
            random()*100,
            generate_series(1, 1000000));
            insert into {self.t_name_stu} values(
            generate_series(1, 1000000),
            '张三');
            
            --设置query_dop=2
            SET query_dop TO 2;
            
            --对两表执行analyze操作
            analyze {self.t_name_sc};
            analyze {self.t_name_stu};
            
            --explain查看是否启用并行查询
            explain select a.* ,b.s_score as score01
            from {self.t_name_stu} a join {self.t_name_sc} b
            on a.s_id=b.s_id;'''
        self.logger.info(sql_cmd)
        sql_res = self.commonsh.execut_db_sql(sql_cmd)
        self.logger.info(sql_res)
        assert_info = "Streaming(type: LOCAL GATHER dop: 1/2)"
        self.assertIn(assert_info, sql_res, "执行失败:" + step_text)

    def tearDown(self):
        self.logger.info("---清理环境---")

        drop_text = "---删除临时表---"
        self.logger.info(drop_text)
        drop_cmd = f'''drop table if exists {self.t_name_sc};
            drop table if exists {self.t_name_stu};'''
        self.logger.info(drop_cmd)
        drop_res = self.commonsh.execut_db_sql(drop_cmd)
        self.logger.info(drop_res)

        self.assertIn("DROP TABLE", drop_res, "执行失败" + drop_text)
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0019执行结束---")

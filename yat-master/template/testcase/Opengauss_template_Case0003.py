"""
Case Type   : 功能测试 -- Query_Dop并行查询
Case Name   : 描述本测试用例内容，例：设置query_dop=2,enable_hashjoin=on,enable_nestloop=off,
              enable_mergejoin=on,执行explain，查看是否启用并行查询
Description :
    1、创建测试表
    2、向测试表中插入数据
    3、分别设置各参数的值query_dop=2,enable_hashjoin=on,enable_nestloop=off,
            enable_mergejoin=on，执行analyze操作并使用explain查看是否启用并行查询
    4、清理环境
Expect      :
    1、创建测试表成功
    2、插入数据成功
    3、设置参数值、analyze及explain操作成功，启用并行查询
    4、清理环境成功
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
            "---{os.path.basename(__file__)} start---")
        self.constant = Constant()
        self.commonsh = CommonSH("PrimaryDbUser")
        self.t_name_sc = "t_score_tmplate_0003_1"
        self.t_name_stu = "t_student_tmplate_0003_2"

    def test_query_dop(self):
        step1_text = "---step1:创建测试表;expect:建表成功---"
        self.logger.info(step1_text)
        sql_cmd1 = f'''drop table if exists {self.t_name_sc};
            CREATE TABLE {self.t_name_sc}(
            s_id int,
            s_score int,
            s_course char(8),
            c_id int);
            drop table if exists {self.t_name_stu};
            CREATE TABLE {self.t_name_stu}(
            s_id int,
            s_name char(8));'''
        self.logger.info(sql_cmd1)
        sql_res1 = self.commonsh.execut_db_sql(sql_cmd1)
        self.logger.info(sql_res1)
        self.assertTrue(sql_res1.count(self.constant.CREATE_TABLE_SUCCESS)
                        == 2, '执行失败:' + step1_text)

        step2_text = "---step2:为测试表插入数据;expect:插入数据成功---"
        self.logger.info(step2_text)
        sql_cmd2 = f'''insert into {self.t_name_sc} values(
            generate_series(1, 1000000), 
            random()*100,
            'course',
            generate_series(1, 1000000));
            insert into {self.t_name_stu} values(
            generate_series(1, 1000000), 
            'name');'''
        self.logger.info(sql_cmd2)
        sql_res2 = self.commonsh.execut_db_sql(sql_cmd2)
        self.logger.info(sql_res2)
        self.assertTrue(sql_res2.count(self.constant.INSERT_SUCCESS_MSG)
                        == 2, '执行失败:' + step2_text)

        step3_text = "---step3:设置各参数的值;expect:设置成功---"
        self.logger.info(step3_text)
        sql_cmd3 = f'''SET query_dop TO 2;
            SET enable_hashjoin TO on;
            SET enable_nestloop TO off;
            SET enable_mergejoin TO on;
            
            --analyze表
            analyze {self.t_name_sc};
            analyze {self.t_name_stu};
            
            explain select a.* ,b.s_score as score01
                from {self.t_name_stu} a join {self.t_name_sc} b 
                on a.s_id=b.s_id;'''
        self.logger.info(sql_cmd3)
        sql_res3 = self.commonsh.execut_db_sql(sql_cmd3)
        self.logger.info(sql_res3)
        self.assertIn("Streaming(type: LOCAL GATHER dop: 1/2)",
                      sql_res3, "执行失败:" + step3_text)

    def tearDown(self):
        self.logger.info("---清理环境---")

        drop_text = "---step:删除测试表;expect:删除成功---"
        self.logger.info(drop_text)
        drop_cmd = f'''drop table if exists {self.t_name_sc};
            drop table if exists {self.t_name_stu};'''
        self.logger.info(drop_cmd)
        drop_res = self.commonsh.execut_db_sql(drop_cmd)
        self.logger.info(drop_res)

        self.assertTrue(drop_res.count(self.constant.TABLE_DROP_SUCCESS)
                        == 2, '执行失败:' + drop_text)
        self.logger.info(
            "---{os.path.basename(__file__)} end---")

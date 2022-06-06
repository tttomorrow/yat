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
Case Name   : 发布订阅系统表--pg_publication
Description :
    1.创建发布端
    2.查询pg_publication结构，及内容
    3.修改发布端信息
    4.查询系统表内容 
Expect      :
    1.成功
    2.类型与资料一致且内容正确
    3.成功
    4.内容正确
History     :
"""
import unittest
import os
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant



class Pubsubclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} start-----")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.com_pub = Common()
        self.tb_name1 = 'tb_pubsub_case126_1'
        self.pubname = "pub_case126"
        self.pubname2 = "pub_case126_2"
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.user_param_pub = f'-U {self.pri_userdb_pub.db_user} ' \
            f'-W {self.pri_userdb_pub.db_password}'

    def test_pubsub(self):
        text = '--step1:创建发布端 expect:成功--'
        self.log.info(text)
        sql = f"create table {self.tb_name1}( i int);"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                     result, '执行失败:' + text)
        sql = f"CREATE PUBLICATION {self.pubname} FOR all TABLES ;" \
            f"CREATE PUBLICATION {self.pubname2} FOR table {self.tb_name1} ;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step2:查询pg_publication结构，及内容 expect:类型与资料一致且内容正确--'
        self.log.info(text)
        sql = f"\d+  pg_publication"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('pubname      | name ', result, '执行失败:' + text)
        self.assertIn('pubowner     | oid ', result, '执行失败:' + text)
        self.assertIn('puballtables | boolean', result, '执行失败:' + text)
        self.assertIn('pubinsert    | boolean', result, '执行失败:' + text)
        self.assertIn('pubupdate    | boolean', result, '执行失败:' + text)
        self.assertIn('pubdelete    | boolean', result, '执行失败:' + text)
        sql = f"select * from pg_publication;"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(f'{self.pubname}   |    16385 | t            '
                      f'| t         | t         | t',
                      result, '执行失败:' + text)
        self.assertIn(f'{self.pubname2} |    16385 | f            '
                      f'| t         | t         | t',
                      result, '执行失败:' + text)

        text = '--step3:修改发布端信息 expect:成功--'
        self.log.info(text)
        sql = f"alter PUBLICATION {self.pubname} set (publish='delete');"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.alter_pub_succ_msg, result,
                      '执行失败:' + text)

        text = '--step4:查询系统表内容  expect:内容正确--'
        self.log.info(text)
        sql = f"select * from pg_publication;"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(f'{self.pubname}   |    16385 | t            '
                      f'| f         | f         | t',
                      result, '执行失败:' + text)
        self.assertIn(f'{self.pubname2} |    16385 | f            '
                      f'| t         | t         | t',
                      result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname};" \
            f"DROP PUBLICATION if exists {self.pubname2};" \
            f"drop table if exists {self.tb_name1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

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
Case Name   : 发布订阅--pg_replication_origin_create
Description :
    1.创建复制源
    2.查询复制源
Expect      :
    1.成功
    2.成功，可查询到1条
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
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.com_pub = Common()
        self.repli_name = "repli_pub_su_case132"

    def test_pubsub(self):
        text = '--step1:创建复制源 expect:成功--'
        self.log.info(text)        
        sql = f"select pg_replication_origin_create('{self.repli_name}');"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        self.assertEqual(result.splitlines()[-2].strip(),
                         '1', '执行失败'+text)

        text = '--step2:查询复制源 expect:成功，可查询到1条--'
        self.log.info(text)
        sql = f"select * from pg_replication_origin " \
            f"where roname='{self.repli_name}';"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.repli_name, result, '执行失败'+text)

    def tearDown(self):
            self.log.info('------------this is tearDown-------------')
            text = '--清理环境--'
            self.log.info(text)
            sql = f"select pg_replication_origin_drop ('{self.repli_name}');"
            result = self.commsh_pub.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('1 row', result, '执行失败'+text)
            self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

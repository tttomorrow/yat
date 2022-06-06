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
Case Type   : postgres_fdw功能
Case Name   : postgres_fdw扩展加载、删除功能正常
Description :
    1、创建数据库db1
    2、加载扩展前查询fdw;
    3、加载扩展;
    4、加载扩展后查询fdw;
    5、重复加载postgres_fdw扩展;
    6、创建基于fdw的服务;
    7、扩展存在依赖，进行删除;
    8、扩展存在依赖，进行cascade删除;
    9、扩展不存在依赖，进行删除;
    10、扩展不存在，进行删除;
    11、扩展不存在，进行if exists删除;
Expect      :
    1、创建数据库db1成功
    2、加载扩展前查询fdw; expect: 无结果
    3、加载扩展; expect:成功
    4、加载扩展后查询fdw; expect: 成功
    5、重复加载postgres_fdw扩展; expect: 失败
    6、创建基于fdw的服务; expect: 成功
    7、扩展存在依赖，进行删除; expect: 失败
    8、扩展存在依赖，进行cascade删除; expect: 成功
    9、扩展不存在依赖，进行删除; expect: 成功
    10、扩展不存在，进行删除; expect: 失败
    11、扩展不存在，进行if exists删除; expect: 成功
History     :
    modified：2022-3-17 by 5328113;生成加密密码文件断言信息变更；
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class PostgresFdw0001(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:初始化----')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.db_1 = 'db_postgresfdw_case0002'
        self.pg_server = 'svc_postgresfdw_case0002'
        self.err_msg1 = 'ERROR:  extension "postgres_fdw" already exists'
        self.err_msg2 = 'ERROR:  cannot drop extension postgres_fdw ' \
                        'because other objects depend on it'
        self.err_msg3 = 'ERROR:  extension "postgres_fdw" does not exist'

        step_txt = '----step0: 创建usermapping密钥文件;' \
                   ' expect:创建成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execute_generate(self.pri_dbuser.db_password,
                                              'usermapping')
        self.assertIn(self.constant.create_keycipher_success, result,
                      '执行失败:' + result)

    def test_main(self):
        step_txt = '----step1: 创建数据库db1; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop database if exists {self.db_1};" \
            f"create database {self.db_1};"
        create_result = self.pri_sh.execut_db_sql(sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_DATABASE_SUCCESS)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step2: 加载扩展前查询fdw; expect: 无结果----'
        self.log.info(step_txt)
        sql = f"select fdwname from pg_foreign_data_wrapper where " \
            f"fdwname='postgres_fdw';"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn('0 rows', result, "执行失败" + step_txt)

        step_txt = '----step3：加载扩展; expect:成功----'
        self.log.info(step_txt)
        sql = f"create extension postgres_fdw;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.constant.create_extension_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step4：加载扩展后查询fdw; expect: 成功----'
        self.log.info(step_txt)
        sql = f"select fdwname from pg_foreign_data_wrapper where " \
            f"fdwname='postgres_fdw';"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn('1 row', result, "执行失败" + step_txt)

        step_txt = '----step5：重复加载postgres_fdw扩展; expect: 失败----'
        self.log.info(step_txt)
        sql = f"create extension postgres_fdw;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.err_msg1, result, "执行失败" + step_txt)

        step_txt = '----step6：创建基于fdw的服务; expect: 成功----'
        self.log.info(step_txt)
        sql = f"create server {self.pg_server} foreign data " \
            f"wrapper postgres_fdw;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.constant.create_server_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step7：扩展存在依赖，进行删除; expect: 失败----'
        self.log.info(step_txt)
        sql = f"drop extension postgres_fdw;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.err_msg2, result, "执行失败" + step_txt)

        step_txt = '----step8：扩展存在依赖，进行cascade删除; expect: 成功----'
        self.log.info(step_txt)
        sql = f"drop extension postgres_fdw cascade;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.constant.drop_extension_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step9：扩展不存在依赖，进行删除; expect: 成功----'
        self.log.info(step_txt)
        sql = f"create extension postgres_fdw;" \
            f"drop extension postgres_fdw;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.constant.drop_extension_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step10: 扩展不存在，进行删除; expect: 失败----'
        self.log.info(step_txt)
        sql = f"drop extension postgres_fdw;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.err_msg3, result, "执行失败" + step_txt)

        step_txt = '----step11: 扩展不存在，进行if exists删除; expect: 成功----'
        self.log.info(step_txt)
        sql = f"drop extension if exists postgres_fdw;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.constant.drop_extension_success, result,
                      "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----清理数据; expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f"drop extension if exists postgres_fdw;"
        result1 = self.pri_sh.execut_db_sql(drop_sql, dbname=self.db_1)
        self.log.info(result1)
        drop_sql = f"drop database if exists {self.db_1};"
        result2 = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result2)

        step_txt = '----teardown断言----'
        self.assertIn(self.constant.drop_extension_success, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, result2,
                      "执行失败" + step_txt)

        self.log.info(f'----{os.path.basename(__file__)}:执行完毕----')

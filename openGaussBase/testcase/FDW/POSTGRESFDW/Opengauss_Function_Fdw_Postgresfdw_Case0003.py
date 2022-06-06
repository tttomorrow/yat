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
Case Name   : postgres_fdw外表功能验证（使用fastcheck脚本进行验证）
Description :
    1、创建数据库db1
    2、db1执行sql脚本（fastcheck脚本）
    3、比对执行结果（实际结果与预期脚本文件比对）
Expect      :
    1、创建数据库db1，创建成功
    2、db1执行sql脚本（fastcheck脚本），执行成功
    3、比对执行结果（实际结果与预期脚本文件比对），比对一致
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class PostgresFdw0003(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:初始化----')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_root = Node(node='PrimaryRoot')
        self.com = Common()
        self.constant = Constant()
        self.db_1 = 'db_postgresfdw_case0003'
        self.sql_name = 'Postgresfdw_Case0003.sql'
        self.expect_name = 'Postgresfdw_Case0003.out'
        self.result_name = 'Postgresfdw_Case0003_result.out'
        self.connect_info = f'-U {self.pri_dbuser.db_user} ' \
            f'-W {self.pri_dbuser.db_password}'
        self.target_path = os.path.join(macro.DB_BACKUP_PATH, "postgres_fdw")

        self.log.info('----远程复制sql及expec文件，并修改权限----')
        self.com.scp_file(self.pri_root,
                          f"{self.sql_name}", self.target_path)
        self.com.scp_file(self.pri_root,
                          f"{self.expect_name}", self.target_path)
        chmod_cmd = f"chmod 777 -R {self.target_path};" \
            f"ls -al {self.target_path}"
        self.log.info(chmod_cmd)
        chmod_result = self.pri_root.sh(chmod_cmd).result()
        self.log.info(chmod_result)

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

        step_txt = '----step2: db1执行sql脚本; expect:执行成功----'
        self.log.info(step_txt)
        shell = f'cd {self.target_path};' \
            f'source {macro.DB_ENV_PATH}; ' \
            f'gsql -d {self.db_1} ' \
            f'-p {self.pri_dbuser.db_port} ' \
            f'-a < {self.sql_name} > {self.result_name} 2>&1'
        result = self.pri_dbuser.sh(shell).result()
        self.log.info(result)
        self.assertEqual('', result, "执行失败" + step_txt)

        step_txt = '----step3:比对执行结果; expect:执行结果正确----'
        shell = f'cd {self.target_path};' \
            f'diff {self.expect_name} {self.result_name}'
        result = self.pri_dbuser.sh(shell).result()
        self.log.info(result)
        self.assertEqual('', result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----清理数据; expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f"drop extension postgres_fdw cascade;"
        result1 = self.pri_sh.execut_db_sql(drop_sql, dbname=self.db_1)
        self.log.info(result1)
        self.log.info(step_txt)
        drop_sql = f"drop database if exists {self.db_1};"
        result2 = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result2)
        step_txt = '----删除执行脚本; expect:删除成功----'
        self.log.info(step_txt)
        rm_cmd = f"rm -rf {self.target_path};ls -al {self.target_path}"
        self.log.info(rm_cmd)
        result3 = self.pri_root.sh(rm_cmd).result()
        self.log.info(result3)

        step_txt = '----teardown断言----'
        self.log.info(step_txt)
        self.assertIn(self.constant.drop_extension_success, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, result2,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.NO_FILE_MSG, result3,
                      "执行失败" + step_txt)

        self.log.info(f'----{os.path.basename(__file__)}:执行完毕----')

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
Case Name   : postgres_fdw基础功能验证--同个数据库应用不同库场景验证
Description :
    1、创建数据库db1，db2
    2、db1创建本地表并插入数据
    3、创建usermapping密钥文件
    4、db2创建postgres_fdw扩展、server、用户映射、创建外表
    5、配置新库db1的hba白名单
    6、映射用户对db2外表进行增删改操作
    7、非映射用户对db2外表进行增删改操作
    8、db1本地表与db2外表进行查询验证
Expect      :
    1、创建两个数据库db1，db2
    2、db1创建本地表并插入数据成功
    3、创建usermapping密钥文件成功
    4、db2创建postgres_fdw扩展、server、用户映射、创建外表，操作成功
    5、配置新库db1的hba白名单，配置成功
    6、映射用户对db2外表进行增删改操作，操作成功
    7、非映射用户对db2外表进行增删改操作，操作失败
    8、db1本地表与db2外表进行查询验证，结果正确且相等
History     :
    modified：2022-3-17 by 5328113;新增测试点非映射用户场景，生成加密密码文件断言信息变更；
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
        self.db_1 = 'db_postgresfdw_case0001_1'
        self.db_2 = 'db_postgresfdw_case0001_2'
        self.tb_local = 'tb_postgresfdw_case0001_local'
        self.tb_foreign = 'tb_postgresfdw_case0001_foreign'
        self.pg_server = 'svc_postgresfdw_case0001'
        self.connect_info = f'-U {self.pri_dbuser.db_user} ' \
            f'-W {self.pri_dbuser.db_password}'

    def test_main(self):
        step_txt = '----step1: 创建两个数据库db1，db2; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop database if exists {self.db_1};" \
            f"drop database if exists {self.db_2};" \
            f"create database {self.db_1};" \
            f"create database {self.db_2}"
        create_result = self.pri_sh.execut_db_sql(sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_DATABASE_SUCCESS)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step2: db1创建本地表并插入数据成功; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"create table {self.tb_local} " \
            f"(id int primary key,name text);" \
            f"insert into {self.tb_local} (name, id) values ('bob', 1);"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step3: 创建usermapping密钥文件;' \
                   ' expect:创建成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execute_generate(self.pri_dbuser.db_password,
                                              'usermapping')
        self.assertIn(self.constant.create_keycipher_success, result,
                      '执行失败:' + result)

        step_txt = '----step4: db2创建postgres_fdw扩展、server、用户映射、创建外表，操作成功;' \
                   ' expect:创建成功----'
        self.log.info(step_txt)
        sql = f"create extension postgres_fdw;" \
            f"create server {self.pg_server} foreign data wrapper " \
            f"postgres_fdw options (host '{self.pri_dbuser.db_host}', " \
            f"dbname '{self.db_1}', port '{self.pri_dbuser.db_port}');" \
            f"create user mapping for {self.pri_dbuser.db_user} server " \
            f"{self.pg_server} options (user '{self.pri_dbuser.db_user}', " \
            f"password '{self.pri_dbuser.db_password}');" \
            f"create foreign table {self.tb_foreign} (id int,name text) " \
            f"server {self.pg_server} options (table_name '{self.tb_local}');"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_2)
        self.log.info(result)
        self.assertIn(self.constant.create_extension_success, result,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.create_server_success, result,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.create_usermapping_success, result,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step5: 配置新库db1的hba白名单; expect:配置成功----'
        self.log.info(step_txt)
        param = f'host {self.db_1} {self.pri_dbuser.db_user} ' \
            f'{self.pri_dbuser.db_host}/32 sha256'
        result = self.pri_sh.execute_gsguc('reload',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           '', pghba_param=param)
        self.assertTrue(result, "执行失败" + step_txt)

        step_txt = '----step6: 映射用户对db2外表进行增删改操作; expect:操作成功----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_foreign};" \
            f"insert into {self.tb_foreign} (name, id) values " \
            f"('tom', 2),('jim', 3);" \
            f"update {self.tb_foreign} set name ='bob_new' where id =1;" \
            f"delete from {self.tb_foreign} where id =3;"
        result = self.pri_sh.execut_db_sql(sql, self.connect_info,
                                           dbname=self.db_2)
        self.log.info(result)
        self.assertIn('INSERT 0 2', result, "执行失败" + step_txt)
        self.assertIn('UPDATE 1', result, "执行失败" + step_txt)
        self.assertIn('DELETE 1', result, "执行失败" + step_txt)

        step_txt = '----step7: 非映射用户对db2外表进行增删改操作; expect:操作失败----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_2)
        self.log.info(result)
        err_msg = f'ERROR:  user mapping not found ' \
            f'for "{self.pri_dbuser.ssh_user}"'
        self.log.info('断言信息', err_msg)
        assert_flag = result.count(err_msg)
        self.assertEqual(4, assert_flag, "执行失败" + step_txt)

        step_txt = '----step8: db1本地表与db2外表进行查询验证;expect:结果正确且相等----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_foreign};"
        foreign_result = self.pri_sh.execut_db_sql(sql, self.connect_info,
                                                   dbname=self.db_2)
        self.log.info(foreign_result)
        sql = f"select * from {self.tb_local};"
        local_result = self.pri_sh.execut_db_sql(sql, dbname=self.db_1)
        self.log.info(local_result)
        self.assertIn('bob_new', foreign_result, "执行失败" + step_txt)
        self.assertIn('2 rows', foreign_result, "执行失败" + step_txt)
        self.assertEqual(foreign_result, local_result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----清理数据; expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table {self.tb_foreign};" \
            f"drop user mapping for {self.pri_dbuser.db_user} " \
            f"server {self.pg_server};" \
            f"drop server {self.pg_server};" \
            f"drop extension postgres_fdw;"
        result1 = self.pri_sh.execut_db_sql(drop_sql, dbname=self.db_2)
        self.log.info(result1)
        drop_sql = f"drop database if exists {self.db_1};" \
            f"drop database if exists {self.db_2};"
        result2 = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result2)
        step_txt = '----恢复hba白名单; expect:配置成功----'
        self.log.info(step_txt)
        param = f'host {self.db_1} {self.pri_dbuser.db_user} ' \
            f'{self.pri_dbuser.db_host}/32'
        result3 = self.pri_sh.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            '', pghba_param=param)

        step_txt = '----teardown断言----'
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.drop_usermapping_success, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.drop_server_success, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.drop_extension_success, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, result2,
                      "执行失败" + step_txt)
        self.assertTrue(result3, "执行失败" + step_txt)

        self.log.info(f'----{os.path.basename(__file__)}:执行完毕----')

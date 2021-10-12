"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : SQL_DCL
Case Name   : 在文本检索词典上添加注释
Description :
    1.创建字典文件
    2.创建全文检索词典
    3.给全文检索词典添加注释信息
    4.在相关系统表中查看注释是否添加成功
    5.清理环境
Expect      :
    1.创建字典文件成功
    2.创建全文检索词典成功
    3.给全文检索词典添加注释信息成功
    4.在相关系统表中查看，注释成功
    5.清理环境成功
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Comment_Case0016开始--')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('-----步骤1.创建字典文件-----')
        check_cmd1 = f"echo -e 'postgres pg\npgsql pg\npostgresql pg' " \
            f"> {macro.DB_INSTANCE_PATH}/pg_dict.syn;"
        self.log.info(check_cmd1)
        echo_msq = self.dbuser.sh(check_cmd1).result()
        self.log.info(echo_msq)

        self.log.info('-----步骤2.创建全文检索词典-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f"create text search dictionary pg_dict "
            f"(template=synonym,synonyms=pg_dict,filepath='"
            f"file://{macro.DB_INSTANCE_PATH}');")
        self.log.info(sql_cmd)
        self.assertIn('CREATE TEXT SEARCH DICTIONARY', sql_cmd)

        self.log.info('-----步骤3.给全文检索词典添加注释信息-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f"comment on text search dictionary "
            f"pg_dict is '测试全文检索词典注释添加成功';")
        self.log.info(sql_cmd)
        self.assertIn('COMMENT', sql_cmd)

        self.log.info('-----步骤4.在相关系统表中查看注释是否添加成功-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f"select description from pg_description where "
            f"objoid=(select oid from pg_ts_dict where dictname='pg_dict');")
        self.log.info(sql_cmd)
        self.assertIn('测试全文检索词典注释添加成功', sql_cmd)

    def tearDown(self):
        self.log.info('-----步骤5.清理环境-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f"drop text search dictionary pg_dict;")
        self.log.info(sql_cmd)
        check_cmd1 = f"rm -rf  {macro.DB_INSTANCE_PATH}/pg_dict.syn"
        self.log.info(check_cmd1)
        echo_msq = self.dbuser.sh(check_cmd1).result()
        self.log.info(echo_msq)
        self.log.info('--Opengauss_Function_Comment_Case0016结束--')

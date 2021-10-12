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
Case Type   : 基础功能
Case Name   : 创建数据库指定表空间，在该数据库上创建表和索引
Description :
    1.创建数据库;
    2. 修改参数默认值ignore_checksum_failure
    3.切换到数据库test查看该参数值
    4.修改该参数为当前数据库值
    5.切换到数据库test查看该参数值
    6.连接数据库test修改其参数
    7.切换到数据库test查看该参数值
    8.重置该参数
    9.切换到数据库test查看该参数值
    10.重置所有参数
    11.切换到数据库test查看该参数值
Expect      :
    1.创建数据库成功
    2.修改默认值成功
    3.参数值为on
    4.修改成功
    5.参数值为off
    6.修改成功
    7.参数为on
    8.修改成功
    9.参数为off
    10.重置成功
    11.参数为off
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Ddldatabasecase0007(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Database_Case0007.py 开始执行--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.dbname = 'database_case013'

    def test_database_case0007(self):
        self.log.info('-------------1.创建数据库-----------')
        result = self.commonshpri.execut_db_sql(
            f"drop database if exists {self.dbname};"
            f"create database {self.dbname} ;")
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)

        self.log.info('---------2. 修改参数默认值ignore_checksum_failure-----------')
        sql = f"alter database {self.dbname} set " \
            f"ignore_checksum_failure to on;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('---------3.切换到数据库test查看该参数值-----------')
        sql = f"show ignore_checksum_failure;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn('on', result)
        self.assertNotIn('off', result)

        self.log.info('---------4.修改该参数为当前数据库值-----------')
        sql = f"alter database {self.dbname} set " \
            f"ignore_checksum_failure  from current;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('---------5.切换到数据库test查看该参数值-----------')
        sql = f"show ignore_checksum_failure;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn('off', result)

        self.log.info('---------6.连接数据库test修改其参数-----------')
        sql = f"alter database {self.dbname} set " \
            f"ignore_checksum_failure  to on;alter database {self.dbname} " \
            f"set enable_force_vector_engine to on"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('---------7.切换到数据库test查看该参数值-----------')
        sql = f"show ignore_checksum_failure;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertNotIn('off', result)
        self.assertIn('on', result)
        sql = f"show enable_force_vector_engine;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertNotIn('off', result)
        self.assertIn('on', result)

        self.log.info('---------8.重置该参数-----------')
        sql = f"alter database {self.dbname} reset ignore_checksum_failure;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('---------9.切换到数据库test查看该参数值-----------')
        sql = f"show ignore_checksum_failure;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn('off', result)
        sql = f"show enable_force_vector_engine;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertNotIn('off', result)
        self.assertIn('on', result)

        self.log.info('---------10.重置所有参数-----------')
        sql = f"alter database {self.dbname} reset all;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result)

        self.log.info('---------11.切换到数据库test查看该参数值-----------')
        sql = f"show ignore_checksum_failure;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn('off', result)
        sql = f"show enable_force_vector_engine;"
        result = self.commonshpri.execut_db_sql(sql, '', self.dbname)
        self.log.info(result)
        self.assertIn('off', result)

    def tearDown(self):
        self.log.info('--------------------环境清理------------------')
        self.log.info('----------删除数据库--------')
        sql = f"drop database if exists {self.dbname};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('---Opengauss_Function_DDL_Database_Case0007.py 执行结束--')

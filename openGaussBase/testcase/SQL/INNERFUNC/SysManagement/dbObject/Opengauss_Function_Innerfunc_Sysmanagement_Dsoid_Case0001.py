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
Case Type   : 功能测试
Case Name   : 使用pg_database_size(oid)函数查询指定OID代表的数据库使用的磁盘空间。
Description :
    1.查询当前数据库postgres
    2.新建数据库new
    3.在postgres中查询new
    4.连接test查询自己
Expect      : 
    1.查询成功
    2.新建成功
    3.查询成功
    4.比在postgres中查询的值大
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.log.info("""
        ---Opengauss_Function_Innerfunc_Sysmanagement_Dsoid_Case0001开始---""")

    def test_dbsize(self):

        def query(dbname):
            cmd = f"""select pg_database_size(a.oid) from pg_database a 
                    where a.datname = {dbname};"""
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            size = int(msg.splitlines()[2].strip())
            return size

        self.log.info("""---------查询当前数据库-----------------------""")
        size0 = query('current_catalog')

        self.log.info("""---------新建数据库通过其它数据库查询其大小-----""")
        db_create = f"""drop database if exists new;
                        create database new encoding = 'utf-8';"""
        msg1 = self.commonsh.execut_db_sql(db_create)
        self.log.info(msg1)
        self.assertTrue('CREATE' in msg1)
        size1 = query("'new'")

        self.log.info("""---------连接上新建的数据库查询自己------------""")
        cmd2 = f'''source {self.DB_ENV_PATH};
        gsql -d new -p {self.node.db_port} -c "select 
        pg_database_size(a.oid) from pg_database a 
        where a.datname = current_catalog;"'''
        msg2 = self.node.sh(cmd2).result()
        self.log.info(msg2)
        size2 = int(msg2.splitlines()[2].strip())
        self.assertTrue(size2 > size1)  # 新建的数据库在连接后会产生系统表

    def tearDown(self):
        db_drop = f"""drop database if exists new;"""
        self.commonsh.execut_db_sql(db_drop)
        self.log.info(db_drop)
        self.log.info("""
        ---Opengauss_Function_Innerfunc_Sysmanagement_Dsoid_Case0001结束---""")
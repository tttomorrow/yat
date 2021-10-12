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
Case Name   : 超级用户执行shutdown命令
Description :
    1. 查询数据库创建用户
    2. 不指定关闭模式shutdown(默认为fast)
    3. 指定关闭模式shutdown为fast
Expect      :
    1. 是超级管理员用户
    2. 当前连接的数据库节点关闭
    3. 不等待客户端中断连接，将所有活跃事务回滚并且强制断开客户端，
    然后关闭数据库节点。
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')
        self.env = macro.DB_ENV_PATH
        self.constant = Constant()
        self.log.info('---Opengauss_Function_DML_Set_Case0150开始---')

    def test_shutdown(self):
        self.log.info('-----------查询数据库创建用户是超级用户管理员---------')
        cmd1 = f""" select rolname,rolsuper from pg_authid 
                    where rolname='{self.user.ssh_user}';"""
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue('| t' in msg1)

        self.log.info('-------------shutdown默认关闭以及带关闭模式fast关闭--')
        shutdown_list = ['shutdown;', 'shutdown fast;']
        check = 'select sysdate;'
        info1 = 'SHUTDOWN'
        info2 = 'failed to connect Unknown'
        info3 = 'Broken pipe'

        for i in range(2):
            self.log.info('开启事务创建表，不关闭事务')
            cmd1 = '''start transaction;
                drop table if exists xhy;
                create table xhy(id int);
                insert into xhy values(89);'''
            msg1 = self.commonsh.execut_db_sql(cmd1)
            self.log.info(msg1)
            self.assertTrue('CREATE' in msg1)

            self.log.info('执行关闭命令')
            cmd2 = f''' source {self.env}
                gsql -d {self.user.db_name} \
               -p {self.user.db_port} -c "{shutdown_list[i]}"'''
            self.log.info(cmd2)
            msg2 = self.user.sh(cmd2).result()
            self.log.info(msg2)
            self.assertTrue(info1 in msg2)

            cmd0 = f''' source {self.env};
                gsql -d {self.user.db_name}\
               -p {self.user.db_port} -c "{check}"'''
            self.log.info(cmd0)
            msg0 = self.user.sh(cmd0).result()
            self.log.info(msg0)
            self.assertTrue(info2 in msg0 or info3 in msg0)

            self.log.info('重启数据库并检查')
            result = self.commonsh.execute_gsctl('restart', 'server started',
                                                 '-M primary')
            self.assertTrue(result)
            result = self.commonsh.execute_gsctl('query', '', get_detail=True)
            self.log.info(result)
            self.assertTrue("Degraded" in result or "Normal" in result)

            self.log.info('检查事务里创建的表是否存在')
            cmd3 = f'''source {self.env}
                gsql -d {self.user.db_name} \
                -p {self.user.db_port} -c "select * from xhy;"'''
            self.log.info(cmd3)
            msg3 = self.user.sh(cmd3).result()
            self.assertTrue('relation "xhy" does not exist' in msg3)

    def tearDown(self):
        status = self.commonsh.get_db_cluster_status()
        if 'Normal' or 'Degraded' not in status:
            self.commonsh.restart_db_cluster()
        cmd = f'drop user if exists xi cascade;'
        self.commonsh.execut_db_sql(cmd)
        self.log.info('------Opengauss_Function_DML_Set_Case0150结束------')

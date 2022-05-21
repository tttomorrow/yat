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
Case Type   : 功能测试
Case Name   : 管理员执行shutdown命令
Description :
    1. 创建具有shutdown权限的管理员用户
    2.1. 开启事务创建表，不关闭事务
    2.2. 执行shutdown(默认关闭以及带关闭模式fast关闭)并执行其他sql语句
    2.2. 重启数据库,检查事务里创建的表
    3. 清理环境
Expect      :
    1. 创建成功
    2.1. 成功
    2.2. shutdown为默认模式时,当前连接的数据库节点关闭
         关闭fast试,不等待客户端中断连接，将所有活跃事务回滚并且强制断开客户端,然后关闭数据库节点
    2.3. 重启成功,表不存在
    3. 清理成功
History     :
"""

import os
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
        self.pwd = macro.COMMON_PASSWD
        self.env = macro.DB_ENV_PATH
        self.constant = Constant()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')

    def test_shutdown(self):
        test = '-----step1:创建具有shutdown权限的管理员用户 expect:成功-----'
        self.log.info(test)
        cmd0 = f'''drop user if exists hong cascade;
                  create user hong with sysadmin password '{self.pwd}';'''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('CREATE ROLE') > -1)
        cmd1 = '''select rolname, rolsystemadmin  
        from pg_authid where rolname = 'hong';'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue('hong    | t' in msg1, '执行失败:' + test)

        test = '-----shutdown默认关闭以及带关闭模式fast关闭-----'
        self.log.info(test)
        shutdown_list = ['shutdown;', 'shutdown fast;']
        check = 'select sysdate;'
        info1 = 'SHUTDOWN'
        info2 = 'failed to connect'
        info3 = 'Broken pipe'
        for i in range(2):
            test = '-----step2.1:开启事务创建表，不关闭事务 expect:成功-----'
            self.log.info(test)
            cmd1 = '''start transaction;
                drop table if exists xhy;
                create table xhy(id int);
                insert into xhy values(89);'''
            msg1 = self.commonsh.execut_db_sql(cmd1)
            self.log.info(msg1)
            self.assertTrue('CREATE' in msg1, '执行失败:' + test)

            test = '-----step2.2:执行shutdown(默认关闭以及带关闭模式fast关闭)并执行其他sql语句 ' \
                   'expect:shutdown为默认模式时,当前连接的数据库节点关闭;' \
                   '关闭fast试,不等待客户端中断连接，将所有活跃事务回滚并且强制断开客户端,然后关闭数据库节点-----'
            self.log.info(test)
            cmd2 = f''' source {self.env};
                gsql -d {self.user.db_name} -U hong -W {self.pwd} \
               -p {self.user.db_port} -c "{shutdown_list[i]}"'''
            self.log.info(cmd2)
            msg2 = self.user.sh(cmd2).result()
            self.log.info(msg2)
            self.assertTrue(info1 in msg2)
            cmd0 = f''' source {self.env};
                gsql -d {self.user.db_name} -U hong -W {self.pwd} \
               -p {self.user.db_port} -c "{check}"'''
            self.log.info(cmd0)
            msg0 = self.user.sh(cmd0).result()
            self.log.info(msg0)
            self.assertTrue(info2 in msg0 or info3 in msg0, '执行失败:' + test)

            test = '-----step2.3:重启数据库,检查事务里创建的表 expect:重启成功,表不存在-----'
            self.log.info(test)
            result = self.commonsh.execute_gsctl('restart', 'server started',
                                                 '-M primary')
            self.assertTrue(result)
            result = self.commonsh.execute_gsctl('query', '', get_detail=True)
            self.log.info(result)
            self.assertTrue("Degraded" in result or "Normal" in result,
                            '执行失败:' + test)

            cmd3 = f'''source {self.env}
                gsql -d {self.user.db_name} -U hong -W {self.pwd} \
                -p {self.user.db_port} -c "select * from xhy;"'''
            self.log.info(cmd3)
            msg3 = self.user.sh(cmd3).result()
            self.log.info(msg3)
            self.assertTrue('relation "xhy" does not exist' in msg3,
                            '执行失败:' + test)

    def tearDown(self):
        self.log.info('-----step3:清理环境-----')
        test_1 = '-----检查数据库状态，异常时重启数据库 expect:成功-----'
        self.log.info(test_1)
        status = self.commonsh.get_db_cluster_status()
        if 'Normal' or 'Degraded' not in status:
            status = self.commonsh.restart_db_cluster()
            self.log.info(status)
            self.assertTrue(status, '执行失败:' + test_1)

        test_2 = '-----删除用户 expect:成功-----'
        self.log.info(test_2)
        drop_cmd = f'drop user if exists hong cascade;'
        drop_res = self.commonsh.execut_db_sql(drop_cmd)
        self.log.info(drop_res)

        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, drop_res,
                      '执行失败:' + test_2)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

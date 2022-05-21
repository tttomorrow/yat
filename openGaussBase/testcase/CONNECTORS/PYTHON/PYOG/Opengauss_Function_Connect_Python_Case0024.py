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
Case Type   : python驱动pyog
Case Name   : openGauss模式连接数据库，锁定表
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.在执行删除操作时对一个有主键的表进行 SHARE ROW EXCLUSIVE 锁
    --3.1创建表
    --3.2开启事务，为测试表加SHARE ROW EXCLUSIVE锁，不做提交
    --3.3开启新的session，在新的session中开启事务，对测试表进行插入操作
    --3.4查看视图PG_THREAD_WAIT_STATUS与PG_LOCKS，查看SHARE ROW EXCLUSIVE锁是否添加成功，
        插入事务是否阻塞
    --3.5清理环境
    4.断开连接
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.1执行成功
    3.2开启事务，为测试表加SHARE ROW EXCLUSIVE锁，不做提交操作成功
    3.3开启新的session，在新的session中开启事务，对测试表进行插入操作失败，事务阻塞
    3.4查看视图PG_THREAD_WAIT_STATUS与PG_LOCKS，查看SHARE ROW EXCLUSIVE锁添加成功，插入事务阻塞
    4.执行成功，db.state返回'closed'
History     :
"""
import os
import time
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython24(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        text = '----Opengauss_Function_Connect_Python_Case0024 start----'
        self.LOG.info(text)

    def test_conn(self):
        text = '----step1: 配置pg_hba入口 expect: 成功----'
        self.LOG.info(text)
        host_cmd = "ifconfig -a|grep inet6 -a2|" \
                   "grep broadcast|awk '{print $2}'"
        self.host = os.popen(host_cmd).readlines()[0].strip()
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
            f'-h "host {self.pri_user.db_name} {self.pri_user.db_user} ' \
            f'{self.host}/32 sha256"'
        self.LOG.info(guc_cmd)
        guc_res = self.pri_user.sh(guc_cmd).result()
        self.LOG.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res, text)

        text = '----step2: 连接数据库 expect: 成功----'
        self.LOG.info(text)
        conn_info = f'opengauss://{self.pri_user.db_user}:' \
            f'{self.pri_user.db_password}@{self.pri_user.db_host}:' \
            f'{self.pri_user.db_port}/{self.pri_user.db_name}'
        db = py_opengauss.open(conn_info)
        self.assertEqual('idle', db.state, text)

        text = '----step3: 在执行删除操作时对一个有主键的表进行 SHARE ROW EXCLUSIVE 锁 ' \
               'expect: 成功----'
        self.LOG.info(text)

        text = '----step3.1: 创建表 expect: 成功----'
        self.LOG.info(text)
        cmd = 'drop table if exists t_py_lock24;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.TABLE_DROP_SUCCESS,
                                 None), text)

        cmd = 'create table t_py_lock24 (a int, b text);'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.CREATE_TABLE_SUCCESS,
                                 None), text)

        text = '----step3.2: 开启事务，为测试表加SHARE ROW EXCLUSIVE锁，不做提交 ' \
               'expect: 操作成功----'
        self.LOG.info(text)
        cmd = 'start transaction;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.START_TRANSACTION_SUCCESS_MSG,
                                 None), text)

        cmd = 'lock table t_py_lock24 in share row exclusive mode;'
        sql = db.prepare(cmd)
        self.assertEqual(sql(), ('LOCK TABLE', None), text)

        text = '----step3.3: 开启新的session，在新的session中开启事务，对测试表进行插入操作 ' \
               'expect: 插入操作失败，事务阻塞----'
        self.LOG.info(text)
        new_session = py_opengauss.open(conn_info)
        self.assertEqual('idle', new_session.state, text)

        cmd = r"select substring(pg_current_sessionid from '\.(.*)') " \
              r"from pg_current_sessionid();"
        self.LOG.info(cmd)
        sql = new_session.prepare(cmd)
        session_id = sql()[0][0]
        self.LOG.info(session_id)
        self.assertIsNotNone(session_id)

        cmd = "insert into t_py_lock24 values (generate_series(1, 10000), " \
              "generate_series(1, 10000)||'bbbbbb');"
        self.LOG.info('----start insert thread----')
        insert_thread = ComThread.ComThread(new_session.prepare, args=[cmd, ])
        insert_thread.setDaemon(True)
        insert_thread.start()

        cmd = "select * from PG_LOCKS where relation=(select oid from " \
              "pg_class where relname='t_py_lock24') and " \
              "mode='ShareRowExclusiveLock';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        sql_res = sql()
        self.LOG.info(sql_res)
        self.assertGreaterEqual(len(sql_res), 1, text)

        cmd = f"select * from PG_THREAD_WAIT_STATUS where " \
            f"sessionid='{session_id}' and wait_status='acquire lock' " \
            f"and lockmode='RowExclusiveLock';"
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        sql_res = sql()
        self.LOG.info(sql_res)
        self.assertGreaterEqual(len(sql_res), 1, text)

        self.LOG.info('----get thread result----')
        time.sleep(30)
        insert_thread.join(30)
        insert_res = insert_thread.get_result()
        self.assertIsNone(insert_res)
        self.LOG.info('----assert db is busy----')
        self.assertEqual(new_session.state, 'busy', text)

        sql = db.prepare('rollback;')
        self.assertEqual(sql(), (self.constant.ROLLBACK_MSG, None), text)

        cmd = 'drop table if exists t_py_lock24;'
        self.LOG.info(cmd)
        sql = db.prepare(cmd)
        self.assertEqual(sql(), (self.constant.TABLE_DROP_SUCCESS,
                                 None), text)

        text = '----step4: 断开连接 expect: 成功----'
        self.LOG.info(text)
        self.LOG.info(db.state)
        db.close()
        self.LOG.info(db.state)
        self.assertEqual('closed', db.state, text)

        new_session.close()
        self.assertEqual('closed', new_session.state, text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----Opengauss_Function_Connect_Python_Case0024 end----'
        self.LOG.info(text)

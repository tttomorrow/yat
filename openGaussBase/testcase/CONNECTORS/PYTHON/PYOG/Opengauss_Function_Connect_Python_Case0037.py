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
Case Name   : openGauss模式连接数据库，关闭当前节点
Description :
    1.配置pg_hba入口
    2.连接数据库
    3.执行SHUTDOWN关闭当前节点
    4.查看数据库状态
    5.启动当前节点
    6.查看数据库状态
    7.连接数据库
    8.执行SHUTDOWN fast关闭当前节点
    9.查看数据库状态
    10.启动当前节点
    11.查看数据库状态
    12.连接数据库
    13.执行SHUTDOWN immediate关闭当前节点
    14.查看数据库状态
    15.启动当前节点
    16.查看数据库状态
Expect      :
    1.执行成功
    2.连接成功，db.state返回'idle'
    3.执行成功
    4.执行成功，回显Is server running?
    5.执行成功，回显server started
    6.执行成功，回显instance_state            : Normal个数等于节点数
    7.连接成功，db.state返回'idle'
    8.执行成功
    9.执行成功，回显Is server running?
    10.执行成功，回显server started
    11.执行成功，回显instance_state            : Normal个数等于节点数
    12.连接成功，db.state返回'idle'
    13.执行成功
    14.执行成功，回显Is server running?
    15.执行成功，回显server started
    16.执行成功，回显instance_state            : Normal个数等于节点数
History     :
"""
import os
import re
import time
import unittest

import py_opengauss
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ConnPython37(unittest.TestCase):
    def setUp(self):
        self.pri_user = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.LOG = Logger()
        self.node_num = self.pri_sh.get_node_num()
        text = '----Opengauss_Function_Connect_Python_Case0037 start----'
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

        text = '----step3: 执行SHUTDOWN关闭当前节点 expect: 成功----'
        self.LOG.info(text)
        cmd = 'shutdown;'
        sql_res = db.execute(cmd)
        self.assertIsNone(sql_res)

        time.sleep(30)

        text = '----step4: 查看数据库状态 expect: 当前节点状态异常----'
        self.LOG.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.LOG.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.LOG.info(db_status)
        regex_res = re.findall('instance_state.*:.*Manually stopped',
                               db_status)
        self.LOG.info(regex_res)
        self.assertEqual(len(regex_res), 1, text)

        text = '----step5: 启动当前节点 expect: 成功----'
        self.LOG.info(text)
        expect_msg = self.constant.RESTART_SUCCESS_MSG
        node_status = self.pri_sh.execute_gsctl('start', expect_msg)
        self.assertTrue(node_status)

        text = '----step6: 查看数据库状态 expect: 数据库状态正常----'
        self.LOG.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.LOG.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.LOG.info(db_status)
        regex_res = re.findall('instance_state.*:.*Normal', db_status)
        self.LOG.info(regex_res)
        self.assertEqual(len(regex_res), self.node_num, text)

        text = '----step7: 连接数据库 expect: 成功----'
        self.LOG.info(text)
        conn_info = f'opengauss://{self.pri_user.db_user}:' \
            f'{self.pri_user.db_password}@{self.pri_user.db_host}:' \
            f'{self.pri_user.db_port}/{self.pri_user.db_name}'
        db = py_opengauss.open(conn_info)
        self.assertEqual('idle', db.state, text)

        text = '----step8: 执行SHUTDOWN FAST关闭当前节点 expect: 成功----'
        self.LOG.info(text)
        cmd = 'shutdown fast;'
        sql_res = db.execute(cmd)
        self.assertIsNone(sql_res)

        time.sleep(5)

        text = '----step9: 查看数据库状态 expect: 当前节点状态异常----'
        self.LOG.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.LOG.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.LOG.info(db_status)
        regex_res = re.findall('instance_state.*:.*Manually stopped',
                               db_status)
        self.LOG.info(regex_res)
        self.assertEqual(len(regex_res), 1, text)

        text = '----step10: 启动当前节点 expect: 成功----'
        self.LOG.info(text)
        expect_msg = self.constant.RESTART_SUCCESS_MSG
        node_status = self.pri_sh.execute_gsctl('start', expect_msg)
        self.assertTrue(node_status)

        text = '----step11: 查看数据库状态 expect: 数据库状态正常----'
        self.LOG.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.LOG.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.LOG.info(db_status)
        regex_res = re.findall('instance_state.*:.*Normal', db_status)
        self.LOG.info(regex_res)
        self.assertEqual(len(regex_res), self.node_num, text)

        text = '----step12: 连接数据库 expect: 成功----'
        self.LOG.info(text)
        conn_info = f'opengauss://{self.pri_user.db_user}:' \
            f'{self.pri_user.db_password}@{self.pri_user.db_host}:' \
            f'{self.pri_user.db_port}/{self.pri_user.db_name}'
        db = py_opengauss.open(conn_info)
        self.assertEqual('idle', db.state, text)

        text = '----step13: 执行SHUTDOWN IMMEIDATE关闭当前节点 expect: 成功----'
        self.LOG.info(text)
        cmd = 'shutdown immediate;'
        sql_res = db.execute(cmd)
        self.assertIsNone(sql_res)

        text = '----step14: 查看数据库状态 expect: 当前节点状态异常----'
        self.LOG.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.LOG.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.LOG.info(db_status)
        regex_res = re.findall('instance_state.*:.*Manually stopped',
                               db_status)
        self.LOG.info(regex_res)
        self.assertEqual(len(regex_res), 1, text)

        text = '----step15: 启动当前节点 expect: 成功----'
        self.LOG.info(text)
        expect_msg = self.constant.RESTART_SUCCESS_MSG
        node_status = self.pri_sh.execute_gsctl('start', expect_msg)
        self.assertTrue(node_status)

        text = '----step16: 查看数据库状态 expect: 数据库状态正常----'
        self.LOG.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.LOG.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.LOG.info(db_status)
        regex_res = re.findall('instance_state.*:.*Normal', db_status)
        self.LOG.info(regex_res)
        self.assertEqual(len(regex_res), self.node_num, text)

    def tearDown(self):
        text = '----run teardown----'
        self.LOG.info(text)

        text = '----查看数据库状态 expect: 数据库状态正常----'
        self.LOG.info(text)
        cmd = f'source {macro.DB_ENV_PATH}; gs_om -t status --all'
        self.LOG.info(cmd)
        db_status = self.pri_user.sh(cmd).result()
        self.LOG.info(db_status)
        regex_res = re.findall('instance_state.*:.*Normal', db_status)
        self.LOG.info(regex_res)
        if len(regex_res) < self.node_num:
            self.pri_sh.restart_db_cluster_for_func('')

        text = '----Opengauss_Function_Connect_Python_Case0037 end----'
        self.LOG.info(text)

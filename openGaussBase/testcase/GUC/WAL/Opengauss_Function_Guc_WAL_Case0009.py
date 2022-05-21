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
Case Type   : guc参数
Case Name   : 修改参数synchronous_commit为remote_write，并校验其预期结果
Description :
    1、查看synchronous_commit默认值
    2、修改synchronous_commit为on，重启使其生效
    3、主机创建表，同时kill掉备机数据库进程，主机向表中插入数据，校验其预期结果
    4、恢复默认值
    5、重启数据库
Expect      :
    1、显示默认值
    2、参数修改成功，重启生效
    3、主机创建表成功，备机kill进程成功，主机插入数据后系统未返回插入成功信息
    4、恢复默认值成功
    5、重启数据库成功
History     : 
"""
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class Guc(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0009_开始---')
        self.st_root = Node('Standby1Root')
        self.sh_user = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        self.t_name = 't_guc_09'

    def test_guc(self):
        text = '--step1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.com.show_param("synchronous_commit")
        self.log.info(self.default_value)

        text = '--step2.1.修改参数值;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"synchronous_commit=remote_write")
        self.log.info(guc_msg1)
        self.assertTrue(guc_msg1, '执行失败:' + text)

        text = '--step2.2.重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)

        text = '--step2.3.show参数值;expect:参数值修改成功--'
        self.log.info(text)
        self.modify_value = self.com.show_param("synchronous_commit")
        self.assertIn('remote_write', self.modify_value, '执行失败:' + text)

        text = '--step3.主机创建表，同时kill掉备机数据库进程，主机向表中插入数据;' \
               'expect:主机创建表成功，备机kill进程成功，主机插入数据后系统未返回插入成功信息--'
        self.log.info(text)
        text = '--step3.1.主机创建表--'
        self.log.info(text)
        sql_cmd = f'drop table if exists {self.t_name};' \
            f'create table {self.t_name}(id int, name character(20));'
        self.log.info(sql_cmd)
        sql_msg = self.sh_user.execut_db_sql(sql_cmd)
        self.log.info(sql_msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_msg,
                      '执行失败:' + text)
        text = '--step3.2.kill掉备机进程--'
        self.log.info(text)
        msg = self.com.kill_pid(self.st_root, 9)
        self.log.info(msg)
        self.assertEqual(msg, '')
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertIn('Manually stopped', status,  '执行失败:' + text)

        text = '--step3.3.主机向表中插入数据，无返回信息--'
        self.log.info(text)
        sql_cmd = f"insert into {self.t_name} values(1, 'guc');"
        self.log.info(sql_cmd)
        connect_thread1 = ComThread(
            self.com.get_sh_result, args=(self.sh_user, sql_cmd))
        connect_thread1.start()
        connect_thread1.join(60)
        thread1_result = connect_thread1.get_result()
        self.log.info(thread1_result)
        self.assertIsNone(thread1_result, '执行失败:' + text)

        text = '--step3.4.重启数据库--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)

    def tearDown(self):
        text = '--step4.恢复默认值;expect:恢复成功--'
        self.log.info(text)
        guc_msg1 = self.sh_user.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"synchronous_commit="
                                              f"{self.default_value}")
        self.log.info(guc_msg1)
        sql_cmd = f'drop table if exists {self.t_name};'
        self.log.info(sql_cmd)
        sql_msg = self.sh_user.execut_db_sql(sql_cmd)
        self.log.info(sql_msg)
        text = '--step5.重启数据库;expect:重启数据库成功--'
        self.log.info(text)
        restart_msg = self.sh_user.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.sh_user.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.com.show_param("synchronous_commit")
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_msg,
                      '执行失败:' + text)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info('---Opengauss_Function_Guc_WAL_Case0009_结束---')

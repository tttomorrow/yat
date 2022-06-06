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
Case Type   : 基础功能
Case Name   : 指定-m参数执行pg_resetxlog命令,设置下一个multitransaction ID重置日志是否成功
Description :
    1.查看数据库状态，若为开启状态则关闭数据库
    2.在对应目录下查看原有xlog列表与pg_multixact/offsets目录下的最大文件名
    3.指定-m参数执行pg_resetxlog命令
    4.查看multitransaction ID(Latest checkpoint's NextMultiXactId)
    5.开启主数据库
    6.进行备机重建
Expect      :
    1.检查数据库状态成功
    2.在对应目录下查看xlog列表与pg_multixact/offsets目录下的最大文件名成功
    3.执行pg_resetxlog命令成功
    4.查看multitransaction ID
    5.开启主数据库成功
    6.进行备机重建成功
History     :
"""
import unittest
import os
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class Resetxlogclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_Tools_pg_resetxlog_Case0006 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.primary_user_node = Node(node='PrimaryDbUser')

    def test_resetxlog0006(self):
        text = '----step1: 查看数据库状态，若为开启状态则关闭数据库 expect:成功----'
        self.log.info(text)
        result = self.commonshpri.stop_db_cluster()
        self.assertTrue(result, '执行失败:' + text)

        text = '-step2: 在对应目录下查看原有xlog列表与pg_multixact/offsets目录下的最大文件名 ' \
               'expect:在对应目录下查看xlog列表与pg_multixact/offsets目录下的最大文件名成功-'
        self.log.info(text)
        cmd = f"ls -l {os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')} " \
            f"| grep 00"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.last_xlog = result.splitlines()[-1].split(' ')[-1]
        self.log.info(f"lastest xlog is {self.last_xlog}")
        cmd = f"ls -l " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_multixact/offsets')}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.offset = result.splitlines()[-1].split(' ')[-1]
        self.next_multitransaction = str(hex(int(self.offset, 16) + 1)) \
                                     + "0000"

        text = '----step3: 指定-m参数执行pg_resetxlog命令 ' \
               'expect:执行pg_resetxlog命令成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"pg_resetxlog {macro.DB_INSTANCE_PATH} " \
            f"-m {self.next_multitransaction}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn("Transaction log reset", result, '执行失败:' + text)

        text = '----step4: 查看multitransaction ' \
               'ID(Latest checkpoint s NextMultiXactId) ' \
               'expect:查看multitransaction ID----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"pg_controldata {macro.DB_INSTANCE_PATH} | grep NextMultiXactId"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)

        text = '----step5: 开启主数据库 expect:开启主数据库成功----'
        self.log.info(text)
        result = self.commonshpri.start_db_cluster(True)
        self.assertTrue(self.constant.START_SUCCESS_MSG in result or
                        'Degraded.' in result, '执行失败:' + text)

        text = '--step6: 进行备机重建  expect:进行备机重建成功--'
        self.log.info(text)
        if 1 != self.commonshpri.get_node_num():
            commonshsta1 = CommonSH('Standby1DbUser')
            commonshsta2 = CommonSH('Standby2DbUser')
            result = commonshsta1.build_standby()
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result,
                          '执行失败:' + text)
            result = commonshsta2.build_standby()
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result,
                          '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        self.commonshpri.start_db_cluster(True)
        if 1 != self.commonshpri.get_node_num():
            commonshsta1 = CommonSH('Standby1DbUser')
            commonshsta2 = CommonSH('Standby2DbUser')
            commonshsta1.build_standby()
            commonshsta2.build_standby()
        self.log.info("-Opengauss_Function_Tools_pg_resetxlog_Case0006 end-")

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
Case Name   : 指定-e参数执行pg_resetxlog命令，设置下一个事务id是否成功,日志重置是否成功
Description :
    1.查看数据库状态，若为开启状态则关闭数据库
    2.在对应目录下查看原有xlog列表
    3.查看下一个事务id(Latest checkpoint's NextXID)
    4.指定-m参数执行pg_resetxlog命令
    5.查看下一个事务id是否为设置值
    6.在对应目录下查看现有xlog列表，是否重置成功
    7.开启主数据库
    8.进行备机重建
Expect      :
    1.检查数据库状态成功
    2.在对应目录下查看xlog列表成功
    3.查看下一个事务id(Latest checkpoint's NextXID)成功
    4.执行pg_resetxlog命令成功
    5.查看下一个事务id为成功
    6.对应目录下查看xlog列表成功，日志重置成功
    7.开启主数据库成功
    8.进行备机重建成功
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
        self.log.info("Opengauss_Function_Tools_pg_resetxlog_Case0013 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.primary_user_node = Node(node='PrimaryDbUser')

    def test_resetxlog0006(self):
        text = '----step1: 查看数据库状态，若为开启状态则关闭数据库 expect:成功----'
        self.log.info(text)
        result = self.commonshpri.stop_db_cluster()
        self.assertTrue(result, '执行失败:' + text)

        text = '-step2: 在对应目录下查看原有xlog列表 ' \
               'expect:在对应目录下查看原有xlog列表-'
        self.log.info(text)
        cmd = f"ls -al {os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')} " \
            f"--ignore='arch*' --ignore='.backup'"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.last_xlog = result.splitlines()[-1].split(' ')[-1]
        self.log.info(f"lastest xlog is {self.last_xlog}")

        text = '----step3: 查看下一个事务id(Latest checkpoint s NextXID) expect:' \
               '查看下一个事务成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"pg_controldata  {macro.DB_INSTANCE_PATH} | grep NextXID"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.nextxid = result.split(' ')[-1]
        self.log.info(f"NextXID is {self.nextxid}")

        text = '----step4: 指定-x参数执行pg_resetxlog命令 expect:执行pg_resetxlog命令成功-'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"pg_resetxlog {macro.DB_INSTANCE_PATH} -x " \
            f"{str(int(self.nextxid)+2)}"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn("Transaction log reset", result, '执行失败:' + text)

        text = '----step5: 查看下一个事务id是否为设置值 ' \
               'expect:查看下一个事务id为成功，设置成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"pg_controldata {macro.DB_INSTANCE_PATH} | grep NextXID"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertEqual(result.split(' ')[-1], str(int(self.nextxid)+2),
                         '执行失败:' + text)

        text = '----step6: 在对应目录下查看现有xlog列表，是否重置成功 ' \
               'expect: 对应目录下查看xlog列表成功，日志重置成功----'
        self.log.info(text)
        cmd = f"ls -l {os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')} " \
            f"| grep 00"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertNotIn(self.last_xlog, result, '执行失败:' + text)

        text = '----step7: 开启主数据库 expect:开启主数据库成功----'
        self.log.info(text)
        result = self.commonshpri.start_db_cluster(True)
        self.assertTrue(self.constant.START_SUCCESS_MSG in result or
                        'Degraded.' in result, '执行失败:' + text)

        text = '--step8: 进行备机重建  expect:进行备机重建成功--'
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
        self.log.info("-Opengauss_Function_Tools_pg_resetxlog_Case0013 end-")

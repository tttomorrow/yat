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
Case Name   : 使用gaussdb指定-i参数启动数据库是否成功
Description :
    1.关闭正在运行的数据库
    2.更改postgresql.conf中的replconninfo1参数，将localport的值改小2（比如19708改为19706）
    3.使用gaussdb工具指定-i启动数据库
Expect      :
    1.关闭正在运行的数据库成功
    2.更改参数成功
    3.使用gaussdb工具指定-i启动数据库成功
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class Gaussdbclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_Tools_Gaussdb_Case0080 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.primary_user_node = Node(node='PrimaryDbUser')
        self.node_name = self.primary_user_node.sh('hostname').result()

    def test_gaussdb(self):
        text = '----step1: 关闭正在运行的数据库 expect:关闭正在运行的数据库成功----'
        self.log.info(text)
        result = self.commonshpri.stop_db_cluster()
        self.assertTrue(result, '执行失败:' + text)

        text = '-step2: 更改postgresql.conf中的replconninfo1参数 expect:更改成功-'
        self.log.info(text)
        result = self.commonshpri.execute_gsguc('check',
                                                'Failed GUC values: 0',
                                                'replconninfo1',
                                                self.node_name, True)
        self.replconninfo1 = result.splitlines()[-1]
        self.log.info(self.replconninfo1)
        local_port = self.replconninfo1.split('=')[3].split(' ')[0]
        self.log.info(local_port)
        new_port = str(int(local_port) - 2)
        self.log.info(new_port)
        self.log.info(self.replconninfo1.strip().split(' ')[1])
        new_replconninfo1 = self.replconninfo1.replace(
            self.replconninfo1.strip().split(' ')[1], f"localport={new_port}")
        result = self.commonshpri.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"{new_replconninfo1}", self.node_name)
        self.assertTrue(result,  '执行失败:' + text)

        text = '----step3: 使用gaussdb工具指定-i启动数据库 expect:成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH};" \
            f"gaussdb  -D {macro.DB_INSTANCE_PATH} -p " \
            f"{new_port} -i"
        self.log.info(cmd)
        start_thread = ComThread(self.common.get_sh_result,
            args=(self.primary_user_node, cmd))
        start_thread.setDaemon(True)
        start_thread.start()
        start_thread.join(60)
        result = start_thread.get_result()
        self.log.info(result)
        cmd = f"ps ux"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.assertIn('gaussdb -D', result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('------------------清理环境-------------')
        cmd = "ps ux | grep 'gaussdb -D'"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        pid1 = result.splitlines()[0].split(' ')[1]
        pid2 = result.splitlines()[1].split(' ')[1]
        cmd = f"kill -9 {pid1} ; kill -9 {pid2}; "
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        self.commonshpri.start_db_cluster(True)
        self.commonshpri.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            f"{self.replconninfo1}", self.node_name)
        self.log.info("-Opengauss_Function_Tools_Gaussdb_Case0080 end-")

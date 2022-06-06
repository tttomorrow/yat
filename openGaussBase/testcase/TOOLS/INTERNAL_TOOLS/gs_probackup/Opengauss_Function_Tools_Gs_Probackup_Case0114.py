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
Case Type   : 系统内部使用工具
Case Name   : 指定--recovery-target-timeline=1，检查备份文件
Description :
    1.新建目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.进行备份
    5.执行validate
    6.删除新建目录
Expect      :
    1.新建目录成功
    2.进行初始化成功
    3.在备份路径内初始化一个新的备份实例成功
    4.进行备份成功
    5.执行validate失败，报错unrecognized option '--recovery-target-timeline=1'
    6.删除新建目录成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0114开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------step1 新建文件与备份目录--------------')
        instance_path = f'{macro.DB_INSTANCE_PATH}'
        LOG.info('实例路径为：' + instance_path)
        index1 = instance_path.find('/')
        index2 = instance_path.rfind('/')
        self.cluster_path = instance_path[index1:index2]
        LOG.info(self.cluster_path)
        mkdir_cmd = f"mkdir {self.cluster_path}/testdir;" \
            f"mkdir {self.cluster_path}/prodir;" \
            f"ls {self.cluster_path} ;"
        LOG.info(mkdir_cmd)
        mkdir_msg = self.PrimaryNode.sh(mkdir_cmd).result()
        LOG.info(mkdir_msg)
        self.assertTrue('testdir' and 'prodir' in mkdir_msg)

        LOG.info('----------step2 进行初始化------------------')
        init_cmd = f"source {macro.DB_ENV_PATH};gs_probackup init -B " \
            f"{self.cluster_path}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)

        LOG.info('-----step3 在备份路径内初始化一个新的备份实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance -B {self.cluster_path}/testdir " \
            f"-D {macro.DB_INSTANCE_PATH} --instance=pro1 ;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'pro1' " + self.constant.init_success, init_msg)

        LOG.info('-----------------step4 执行备份-------------------')
        fullback_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -b full  -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} ;"
        LOG.info(fullback_cmd)
        fullback_msg = self.PrimaryNode.sh(fullback_cmd).result()
        LOG.info(fullback_msg)
        self.assertIn('completed', fullback_msg)
        self.backupmsg = fullback_msg.splitlines()[-1]
        LOG.info(self.backupmsg)
        self.backupid = self.backupmsg.split()[2]
        LOG.info('备份ID为：' + self.backupid)

        LOG.info('-----------step5 执行validate--------------')
        validate_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup validate -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -i {self.backupid} " \
            f"--recovery-target-timeline=1;"
        LOG.info(validate_cmd)
        validate_msg = self.PrimaryNode.sh(validate_cmd).result()
        LOG.info(validate_msg)
        self.assertIn('unrecognized option ', validate_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown----------------------')
        LOG.info('-----------------step6 删除新建目录------------------')
        clear_cmd = f"rm -rf {self.cluster_path}/testdir;" \
            f"rm -rf {self.cluster_path}/prodir;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0114执行完成-')

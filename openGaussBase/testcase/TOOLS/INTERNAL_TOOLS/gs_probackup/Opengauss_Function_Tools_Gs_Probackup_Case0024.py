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
Case Name   : 指定--ttl选项从恢复时间开始计算，备份要固定的时间量
Description :
    1.新建目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.进行备份
    5.指定从恢复时间开始计算，备份要固定的时间量
    6.删除新建目录
Expect      :
    1.新建目录成功
    2.进行初始化成功
    3.在备份路径内初始化一个新的备份实例成功
    4.备份成功
    5.指定从恢复时间开始计算，备份要固定的时间量成功，显示备份的过期时间为：
      当前时间+ttl时间
    6.删除新建目录成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0024开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------step1 新建备份目录--------------')
        instance_path = f'{macro.DB_INSTANCE_PATH}'
        LOG.info('实例路径为：' + instance_path)
        index1 = instance_path.find('/')
        index2 = instance_path.rfind('/')
        self.cluster_path = instance_path[index1:index2]
        LOG.info(self.cluster_path)
        init_cmd = f"mkdir {self.cluster_path}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], init_msg)

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
            f"-D {macro.DB_INSTANCE_PATH} --instance=pro1;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'pro1' " + self.constant.init_success, init_msg)

        LOG.info('--------------------step4 进行备份-------------------')
        back_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -b Full  -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} "
        LOG.info(back_cmd)
        back_msg = self.PrimaryNode.sh(back_cmd).result()
        LOG.info(back_msg)
        self.assertIn('completed', back_msg)
        self.backupmsg = back_msg.splitlines()[-1]
        LOG.info(self.backupmsg)
        self.backupid = self.backupmsg.split()[2]
        LOG.info('备份ID为：' + self.backupid)

        LOG.info('---step5 指定从恢复时间开始计算，备份要固定的时间量----')
        time_cmd = 'date +"%Y-%m-%d"'
        LOG.info(time_cmd)
        time_msg = self.PrimaryNode.sh(time_cmd).result()
        LOG.info('当前时间为：' + time_msg)
        newtime_cmd = f'date -d "+5 day" +"%Y-%m-%d"'
        LOG.info(newtime_cmd)
        newtime_msg = self.PrimaryNode.sh(newtime_cmd).result()
        LOG.info('新的时间为：' + newtime_msg)
        set_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup set-backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -i {self.backupid} --ttl=5d; "
        LOG.info(set_cmd)
        set_msg = self.PrimaryNode.sh(set_cmd).result()
        LOG.info(set_msg)
        self.assertIn(f"{newtime_msg}", set_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown--------------------')
        LOG.info('---------------step6 删除新建目录-----------------')
        clear_cmd = f"rm -rf {self.cluster_path}/testdir;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0024执行完成-')

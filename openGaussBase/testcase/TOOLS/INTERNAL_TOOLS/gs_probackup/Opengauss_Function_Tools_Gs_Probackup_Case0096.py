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
Case Name   : 指定--delete-wal与--delete-expired参数，执行delete
Description :
    1.新建目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.进行全量备份
    5.在wal文件夹下创建文件
    6.执行delete
    7.删除新建目录
Expect      :
    1.新建目录成功
    2.进行初始化成功
    3.在备份路径内初始化一个新的备份实例成功
    4.进行备份成功
    5.文件创建成功
    6.delete成功，并且提示unexpected WAL file name "aaa"，
    不满足留存策略的备份文件被删除
    7.删除新建目录成功
History     :
"""

import unittest
import time

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0096开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.comsh = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('------step1.1 新建文件与备份目录-----------')
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
        LOG.info('---------step1.2 设置相关参数-----------------------')
        LOG.info('----------------查看archive_mode初始值--------------')
        mode_msg = self.comsh.execut_db_sql('show archive_mode;')
        LOG.info(mode_msg)
        self.mode_pv = mode_msg.splitlines()[-2].strip()
        LOG.info('----------------查看archive_command初始值--------------')
        c_msg = self.comsh.execut_db_sql('show archive_command;')
        LOG.info(c_msg)
        self.command_pv = c_msg.splitlines()[-2].strip()
        LOG.info('----------------------修改参数值-----------------------')
        mode_msg = self.comsh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'archive_mode = on')
        LOG.info(mode_msg)
        c_msg = self.comsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"archive_command = 'cp %p "
                                         f"{self.cluster_path}/"
                                         f"testdir/wal/pro1/%f'")
        LOG.info(c_msg)

        LOG.info('-------重启数据库------')
        self.comsh.restart_db_cluster()
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)

        LOG.info('-------校验其预期结果-------')
        mode_value = self.comsh.execut_db_sql('show archive_mode;')
        LOG.info(mode_value)
        res1 = mode_value.splitlines()[-2].strip()
        self.assertIn('on', res1)
        c_msg = self.comsh.execut_db_sql('show archive_command;')
        LOG.info(c_msg)
        res = c_msg.splitlines()[-2].strip()
        self.assertIn(f"cp %p {self.cluster_path}/testdir/wal/pro1/%f", res)

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

        LOG.info('-------------step4 执行备份---------------')
        fullback_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -b full  -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} --ttl=5 --archive-timeout=1200;"
        LOG.info(fullback_cmd)
        fullback_msg = self.PrimaryNode.sh(fullback_cmd).result()
        LOG.info(fullback_msg)
        self.assertIn('completed', fullback_msg)
        self.fullbackupmsg = fullback_msg.splitlines()[-1]
        LOG.info(self.fullbackupmsg)
        self.fullbackupid = self.fullbackupmsg.split()[2]
        LOG.info('增量备份ID为：' + self.fullbackupid)

        time.sleep(10)

        LOG.info('---------step5 查看wal目录下文件--------------')
        size_cmd1 = f"du -sh {self.cluster_path}/testdir/wal/pro1 ;"
        LOG.info(size_cmd1)
        size_msg1 = self.PrimaryNode.sh(size_cmd1).result()
        LOG.info(size_msg1)

        LOG.info('-----------step6.1 执行delete--------------')
        delete_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup delete -B {self.cluster_path}/testdir " \
            f" --instance=pro1 --delete-wal " \
            f"--delete-expired --retention-redundancy=1;"
        LOG.info(delete_cmd)
        delete_msg = self.PrimaryNode.sh(delete_cmd).result()
        LOG.info(delete_msg)

        LOG.info('-----------step6.2 查看删除后wal文件--------------')
        size_cmd2 = f"du -sh {self.cluster_path}/testdir/wal/pro1 ;"
        LOG.info(size_cmd2)
        size_msg2 = self.PrimaryNode.sh(size_cmd2).result()
        LOG.info(size_msg2)
        size_msg3 = size_msg1.split()[0]
        size_msg4 = size_msg2.split()[0]
        LOG.info(float(size_msg3[:-1]))
        LOG.info(float(size_msg4[:-1]))
        self.assertTrue(
            float(size_msg3[:-1]) > float(size_msg4[:-1]))

    def tearDown(self):
        LOG.info('------------------this is tearDown----------------------')
        LOG.info('-----------------step7.1 删除新建目录------------------')
        clear_cmd = f"rm -rf {self.cluster_path}/testdir;" \
            f"rm -rf {self.cluster_path}/prodir;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-----------------step7.2 还原参数------------------')
        msg1 = self.comsh.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'archive_mode = {self.mode_pv}')
        LOG.info(msg1)
        msg2 = self.comsh.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'archive_command = {self.command_pv}')
        LOG.info(msg2)
        stopmsg = self.comsh.stop_db_cluster()
        LOG.info(stopmsg)
        startmsg = self.comsh.start_db_cluster()
        LOG.info(startmsg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0096执行完成-')

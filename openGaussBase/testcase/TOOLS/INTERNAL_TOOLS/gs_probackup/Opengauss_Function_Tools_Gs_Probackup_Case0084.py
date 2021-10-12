"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : 指定-j、--progress参数执行merge
Description :
    1.设置参数enable_cbm_tracking=on
    2.新建目录
    3.进行初始化
    4.在备份路径内初始化一个新的备份实例
    5.进行全量备份与增量备份
    6.执行merge（使用增量备份的back-id）
    7.查看备份情况
    8.删除新建目录,恢复enable_cbm_tracking的参数值
Expect      :
    1.设置参数enable_cbm_tracking=on成功
    2.新建目录成功
    3.进行初始化成功
    4.在备份路径内初始化一个新的备份实例成功
    5.进行备份成功
    6.merge成功，有详细的进展信息，再次查看备份情况，增量备份的信息已删除，
    信息合并到全量备份中
    7.查看备份情况成功，备份被合并为1个
    8.删除新建目录成功，恢复enable_cbm_tracking的参数值成功
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
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0084开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('----------step1.1 设置相关参数---------------------')
        cmd1 = f"sed -i '$a\\enable_cbm_tracking=on' " \
            f"{macro.DB_INSTANCE_PATH}/postgresql.conf"
        LOG.info(cmd1)
        msg1 = self.PrimaryNode.sh(cmd1).result()
        LOG.info(msg1)
        LOG.info('---------step1.2 重启数据库-----------------------')
        self.sh_primary.restart_db_cluster()
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        LOG.info('---------step1.3 查看设置参数是否生效--------------')
        msg = self.sh_primary.execut_db_sql('show enable_cbm_tracking;')
        LOG.info(msg)
        value = msg.splitlines()[-2].strip()
        self.assertIn('on', value)

        LOG.info('---------step2 新建文件与备份目录--------------')
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

        LOG.info('----------step3 进行初始化------------------')
        init_cmd = f"source {macro.DB_ENV_PATH};gs_probackup init -B " \
            f"{self.cluster_path}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)

        LOG.info('-----step4 在备份路径内初始化一个新的备份实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance -B {self.cluster_path}/testdir " \
            f"-D {macro.DB_INSTANCE_PATH} --instance=pro1 ;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'pro1' " + self.constant.init_success, init_msg)

        LOG.info('-------------step5 执行备份---------------')
        fullback_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -b full  -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} ;"
        LOG.info(fullback_cmd)
        fullback_msg = self.PrimaryNode.sh(fullback_cmd).result()
        LOG.info(fullback_msg)
        self.assertIn('completed', fullback_msg)
        self.fullbackupmsg = fullback_msg.splitlines()[-1]
        LOG.info(self.fullbackupmsg)
        self.fullbackupid = self.fullbackupmsg.split()[2]
        LOG.info('全量备份ID为：' + self.fullbackupid)
        ptrackback_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -b ptrack  -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} ;"
        LOG.info(ptrackback_cmd)
        ptrackback_msg = self.PrimaryNode.sh(ptrackback_cmd).result()
        LOG.info(ptrackback_msg)
        self.assertIn('completed', ptrackback_msg)
        self.ptrackbackupmsg = ptrackback_msg.splitlines()[-1]
        LOG.info(self.ptrackbackupmsg)
        self.ptrackbackupid = self.ptrackbackupmsg.split()[2]
        LOG.info('增量备份ID为：' + self.ptrackbackupid)

        LOG.info('-----------step5 执行merge--------------')
        merge_cmd = f"source {macro.DB_ENV_PATH};" \
            f"cd {self.cluster_path} ;" \
            f"gs_probackup merge -B {self.cluster_path}/testdir " \
            f" --instance=pro1 -i {self.ptrackbackupid} -j 4 --progress;"
        LOG.info(merge_cmd)
        merge_msg = self.PrimaryNode.sh(merge_cmd).result()
        LOG.info(merge_msg)
        self.assertIn(f'Merge of backup {self.ptrackbackupid} completed',
                      merge_msg)

        LOG.info('-----------step6 查看备份情况--------------')
        show_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup show -B {self.cluster_path}/testdir " \
            f" --instance=pro1 ;"
        LOG.info(show_cmd)
        show_msg = self.PrimaryNode.sh(show_cmd).result()
        LOG.info(show_msg)
        self.assertIn(f'{self.ptrackbackupid}', show_msg)
        self.assertNotIn(f'{self.fullbackupid}', show_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown----------------------')
        LOG.info('-----------------step7.1 删除新建目录------------------')
        clear_cmd = f"rm -rf {self.cluster_path}/testdir;" \
            f"rm -rf {self.cluster_path}/prodir;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('--------------step7.2 恢复数据库参数--------------------')
        recover_cmd = f"sed -i '$d' {macro.DB_INSTANCE_PATH}/postgresql.conf;"
        LOG.info(recover_cmd)
        recover_msg = self.PrimaryNode.sh(recover_cmd).result()
        LOG.info(recover_msg)
        self.sh_primary.restart_db_cluster()
        status = self.sh_primary.get_db_cluster_status()
        LOG.info(status)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0084执行完成-')

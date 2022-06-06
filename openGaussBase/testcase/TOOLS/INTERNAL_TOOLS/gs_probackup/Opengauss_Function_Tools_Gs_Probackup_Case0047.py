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
Case Name   : 指定一个逻辑复制槽，指定-S、--backup-pg-log、-C选项进行备份
Description :
    1.新建目录
    2.创建逻辑复制槽
    3.确认逻辑复制槽创建成功：
    4.进行初始化
    5.在备份路径内初始化一个新的备份实例
    6.执行备份
    7.删除新建目录与复制槽
Expect      :
    1.新建目录成功
    2.创建逻辑复制槽成功
    3.确认成功
    4.进行初始化成功
    5.在备份路径内初始化一个新的备份实例成功
    6.执行备份失败，报错信息为：cannot use a logical replication slot for
    physical replication
    7.删除新建目录与复制槽成功
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
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0047开始执行-')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.pv = ''

    def test_system_internal_tools(self):
        LOG.info('---------step1 新建备份目录--------------')
        init_cmd = f"mkdir {macro.DB_BACKUP_PATH}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], init_msg)

        LOG.info('----------step2.1设置wal_level = logical-----------------')
        msg = self.sh_primary.execut_db_sql('show wal_level;')
        LOG.info(msg)
        self.pv = msg.splitlines()[-2].strip()
        msg = self.sh_primary.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'wal_level=logical')
        LOG.info(msg)
        LOG.info('----------------step2.2 重启数据库--------------------')
        self.sh_primary.restart_db_cluster()
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        msg1 = self.sh_primary.execut_db_sql('show wal_level;')
        LOG.info(msg1)
        self.new_value = msg1.splitlines()[-2].strip()
        self.assertIn('logical', self.new_value)

        LOG.info('---------step2.3 创建逻辑复制槽--------------')
        create_msg = self.sh_primary.execut_db_sql(
            "SELECT * FROM pg_create_logical_replication_slot"
            "('slot1', 'mppdb_decoding');")
        LOG.info(create_msg)
        self.assertIn('1 row', create_msg)

        LOG.info('----------step3 进行初始化------------------')
        init_cmd = f"source {macro.DB_ENV_PATH};gs_probackup init -B " \
            f"{macro.DB_BACKUP_PATH}/testdir;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg)

        LOG.info('-----step4 在备份路径内初始化一个新的备份实例---')
        init_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance -B {macro.DB_BACKUP_PATH}/testdir " \
            f"-D {macro.DB_INSTANCE_PATH} --instance=pro1;"
        LOG.info(init_cmd)
        init_msg = self.PrimaryNode.sh(init_cmd).result()
        LOG.info(init_msg)
        self.assertIn("'pro1' " + self.constant.init_success, init_msg)

        LOG.info('-------------step5 执行全量备份---------------')
        back_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup backup -B {macro.DB_BACKUP_PATH}/testdir " \
            f" --instance=pro1 -b full  -d {self.PrimaryNode.db_name} -p " \
            f"{self.PrimaryNode.db_port} -S slot1 --backup-pg-log -C ;"
        LOG.info(back_cmd)
        back_msg = self.PrimaryNode.sh(back_cmd).result()
        LOG.info(back_msg)
        self.assertIn(
            'cannot use a logical replication slot for physical replication',
            back_msg)

    def tearDown(self):
        LOG.info('------------------this is tearDown--------------------')
        LOG.info('------------step6.1 删除新建逻辑复制槽与表--------------')
        msg = self.sh_primary.execut_db_sql(
            "SELECT * FROM pg_drop_replication_slot('slot1');")
        LOG.info(msg)
        LOG.info('---------------step6.2 恢复参数------------------------')
        msg = self.sh_primary.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"wal_level={self.pv}")
        LOG.info(msg)
        stopmsg = self.sh_primary.stop_db_cluster()
        LOG.info(stopmsg)
        startmsg = self.sh_primary.start_db_cluster()
        LOG.info(startmsg)
        LOG.info('------------------step6.3 删除新建目录------------------')
        clear_cmd = f"rm -rf {macro.DB_BACKUP_PATH}/testdir;"
        LOG.info(clear_cmd)
        clear_msg = self.PrimaryNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-Opengauss_Function_Tools_Gs_Probackup_Case0047执行完成-')

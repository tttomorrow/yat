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
Case Name   : 备机执行gs_backup -l指定已存在文件进行恢复时，日志存放文件是否会
              将信息写入
Description :
    1.新建备份目录
    2.在非$GAUSSLOG路径下创建文件并写入内容查看
    3.主机执行gs_backup进行备份
    4.备机执行gs_backup进行恢复
    5.主机查询日志文件
    6.备机查询日志文件
    7.清理环境
Expect      :
    1.新建备份目录成功
    2.在非$GAUSSLOG路径下创建文件并写入内容成功
    3.执行gs_backup进行备份成功
    4.执行gs_backup进行恢复成功
    5.日志未写入指定文件
    6.产生了新的日志文件，未覆盖指定文件内容
    7.清理环境完成
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()
Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0029start---')
        self.constant = Constant()
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Standby1_User_Node = Node('Standby1DbUser')
        self.gs_backup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                               'gs_backup')
        self.file_name = "backupzh029.log"
        self.file_path = os.path.join(macro.DB_INSTANCE_PATH, self.file_name)

    def test_system_internal_tools(self):
        LOG.info('---步骤1:新建备份目录---')
        is_dir_exists_cmd = f'''if [ ! -d "{self.gs_backup_bak_path}" ]
                                       then
                                           mkdir {self.gs_backup_bak_path}
                                       fi'''
        LOG.info(is_dir_exists_cmd)
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        LOG.info(result)
        LOG.info('---步骤2:在非$GAUSSLOG路径下创建文件并写入内容---')
        excute_cmd = f'echo "hello opengausss" > {self.file_path}';
        LOG.info(excute_cmd)
        msg1 = self.Primary_User_Node.sh(excute_cmd).result()
        LOG.info(msg1)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg1)
        excute_cmd = f'cat {self.file_path}';
        LOG.info(excute_cmd)
        msg1 = self.Primary_User_Node.sh(excute_cmd).result()
        LOG.info(msg1)
        self.assertIn('hello opengausss', msg1)
        LOG.info('---步骤3:主机执行gs_backup进行备份---')
        gs_backup_cmd = f'''source {macro.DB_ENV_PATH};
            gs_backup -t backup --backup-dir={self.gs_backup_bak_path};
            '''
        LOG.info(gs_backup_cmd)
        backup_msg = self.Primary_User_Node.sh(gs_backup_cmd).result()
        LOG.info(backup_msg)
        self.assertIn(self.constant.gs_backup_success, backup_msg)
        LOG.info('---步骤4:备机执行gs_backup进行恢复---')
        gs_backup_cmd = f'''source {macro.DB_ENV_PATH};
            gs_backup -t restore --backup-dir={self.gs_backup_bak_path} \
            -l {self.file_path} ;
            '''
        LOG.info(gs_backup_cmd)
        backup_msg = self.Standby1_User_Node.sh(gs_backup_cmd).result()
        LOG.info(backup_msg)
        self.assertIn(self.constant.gs_backup_restore_success, backup_msg)
        LOG.info('---步骤5:主机查询日志文件---')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            cat {self.file_path};
            ls -tl {macro.DB_INSTANCE_PATH} |grep 'backupzh029-'|head -1;
            '''
        LOG.info(query_cmd)
        backup_msg = self.Primary_User_Node.sh(query_cmd).result()
        LOG.info(backup_msg)
        self.assertIn('hello opengausss', backup_msg)
        self.assertIn('', backup_msg)
        LOG.info('---步骤6:备机查询日志文件---')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            ls -tl {macro.DB_INSTANCE_PATH} |grep 'backupzh029-'|head -1;
             '''
        LOG.info(query_cmd)
        backup_msg = self.Standby1_User_Node.sh(query_cmd).result()
        LOG.info(backup_msg)
        self.assertIn('backupzh029-', backup_msg)

    def tearDown(self):
        LOG.info('---步骤6:清理环境----')
        clear_cmd = f"rm -rf {self.gs_backup_bak_path};" \
                    f"rm -rf {self.file_path};" \
                    f"rm -rf {macro.DB_ENV_PATH}/backupzh029.log;"
        LOG.info(clear_cmd)
        clear_msg = self.Primary_User_Node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        clear_msg = self.Standby1_User_Node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0029finish---')

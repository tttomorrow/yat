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
Case Name   : gs_backup不指定日志路径进行备份，日志是否生成在$GAUSSLOG/om下
Description :
    1.新建备份目录
    2.使用gs_backup脚本备份数据库主机
    3.在$GAUSSLOG/om下，查看日志
    4.删除备份文件
Expect      :
    1.新建备份目录成功
    2.备份成功
    3.日志生成在$GAUSSLOG/om下，并记录相关信息
    4.删除备份文件成功
History     :
"""

import os
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH

LOG = Logger()
Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0016start---')
        self.constant = Constant()
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Standby1_User_Node = Node('Standby1DbUser')
        self.gs_backup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                               'gs_backup016')

    def test_system_internal_tools(self):
        LOG.info('---步骤1:新建备份目录---')
        is_dir_exists_cmd = f'''if [ ! -d "{self.gs_backup_bak_path}" ]
                                       then
                                           mkdir {self.gs_backup_bak_path}
                                       fi'''
        LOG.info(is_dir_exists_cmd)
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        LOG.info(result)
        LOG.info('---步骤2:主机执行gs_backup进行备份---')
        gs_backup_cmd = f'''source {macro.DB_ENV_PATH};
            gs_backup -t backup --backup-dir={self.gs_backup_bak_path};
            '''
        LOG.info(gs_backup_cmd)
        backup_msg = self.Primary_User_Node.sh(gs_backup_cmd).result()
        LOG.info(backup_msg)
        self.assertIn(self.constant.gs_backup_success, backup_msg)
        LOG.info('---步骤3:主机查询日志是否生成在$GAUSSLOG/om下---')
        query_cmd = f'''source {macro.DB_ENV_PATH};
                    ls -tl $GAUSSLOG/om |grep 'gs_backup'|head -1;
                    '''
        LOG.info(query_cmd)
        backup_msg = self.Primary_User_Node.sh(query_cmd).result()
        LOG.info(backup_msg)
        self.assertIn('gs_backup', backup_msg)

    def tearDown(self):
        LOG.info('---步骤4:删除备份文件----')
        clear_cmd = f"rm -rf {self.gs_backup_bak_path};"
        LOG.info(clear_cmd)
        clear_msg = self.Primary_User_Node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        clear_msg = self.Standby1_User_Node.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0016finish---')

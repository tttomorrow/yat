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
Case Name   : 主备备份后指定主数据库hostname执行gs_backup进行恢复
Description :
    1.新建备份目录
    2.执行gs_backup对参数文件进行备份
    3.更改主备session_timeout参数的数值
    4.确认该参数是否已更改成功
    5.执行gs_backup对参数文件进行单节点恢复
    6.查看postgresql.conf文件，参数值是否恢复
Expect      :
    1.切换用户成功
    2.执行gs_backup成功，提示信息为：Successfully backed up cluster files.
    3.更改主备session_timeout参数的数值成功
    4.该参数已更改成功
    5.执行gs_backup对参数文件进行恢复成功
    6.参数已恢复
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0020开始执行---')
        self.constant = Constant()
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.nv = ''
        self.pv = ''

    def test_system_internal_tools(self):
        LOG.info('----------查看是否为主备环境------------------')
        query_cmd = f''' source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            LOG.info('----------单机环境，后续不执行，直接通过----------')
        else:
            self.StandbyNode = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')
            LOG.info('-----------------新建备份目录-----------------')
            mkdir_cmd = f"mkdir {macro.DB_BACKUP_PATH}/tesdir;"
            LOG.info(mkdir_cmd)
            mkdir_msg = self.PrimaryNode.sh(mkdir_cmd).result()
            LOG.info(mkdir_msg)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], mkdir_msg)

            LOG.info('--------------执行gs_backup进行备份-----------')
            backup_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_backup -t backup \
                    --backup-dir={macro.DB_BACKUP_PATH}/tesdir ;
                    '''
            LOG.info(backup_cmd)
            backup_msg = self.PrimaryNode.sh(backup_cmd).result()
            LOG.info(backup_msg)
            self.assertIn(self.constant.gs_backup_success, backup_msg)

            LOG.info('-------------修改参数,参数数值递增-------------')
            value_msg = self.sh_primary.execut_db_sql('show session_timeout;')
            LOG.info(value_msg)
            self.pv = value_msg.splitlines()[-2].strip()
            LOG.info('参数初始值为：' + self.pv)
            self.nv = self.pv
            for arg in ('s', 'min', 'h', 'd'):
                if arg in self.pv:
                    self.nv = str(
                        int(self.pv.strip(arg)) + 1) + arg
            LOG.info('参数新的值为：' + self.nv)
            sed_cmd = f'''sed -i \
                's/session_timeout = {self.pv}/session_timeout = {self.nv}/' \
                {macro.DB_INSTANCE_PATH}/postgresql.conf;
                '''
            LOG.info(sed_cmd)
            sed_msg = self.PrimaryNode.sh(sed_cmd).result()
            LOG.info(sed_msg)

            LOG.info('------------------校验文件参数值---------------')
            check_cmd = f"cat {macro.DB_INSTANCE_PATH}/postgresql.conf|" \
                f"grep session_timeout;"
            LOG.info(check_cmd)
            check_msg = self.PrimaryNode.sh(check_cmd).result()
            LOG.info(check_msg)
            self.assertIn(self.nv, check_msg)

            LOG.info('--------------执行gs_backup进行还原-----------')
            host_cmd = 'hostname'
            LOG.info(host_cmd)
            host_msg = self.PrimaryNode.sh(host_cmd).result()
            LOG.info('hostname为：' + host_msg)
            backup_cmd = f'''source {macro.DB_ENV_PATH};
                gs_backup -t restore \
                --backup-dir={macro.DB_BACKUP_PATH}/tesdir -h {host_msg};
                '''
            LOG.info(backup_cmd)
            backup_msg = self.PrimaryNode.sh(backup_cmd).result()
            LOG.info(backup_msg)
            self.assertIn(self.constant.gs_backup_restore_success, backup_msg)

            LOG.info('------------------校验文件参数值---------------')
            check_cmd = f"cat {macro.DB_INSTANCE_PATH}/postgresql.conf|" \
                f"grep session_timeout;"
            LOG.info(check_cmd)
            check_msg = self.PrimaryNode.sh(check_cmd).result()
            LOG.info(check_msg)
            self.assertIn(self.pv, check_msg)

    def tearDown(self):
        LOG.info('-----------------this is tearDown-------------------')
        LOG.info('----------------恢复文件参数值----------------')
        recover_cmd = f"sed -i " \
            f"'s/session_timeout = {self.nv}/session_timeout = {self.pv}/' " \
            f"{macro.DB_INSTANCE_PATH}/postgresql.conf;"
        LOG.info(recover_cmd)
        recover_msg = self.PrimaryNode.sh(recover_cmd).result()
        LOG.info(recover_msg)
        query_cmd = f''' source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            LOG.info('----------单机环境，后续不执行，直接通过----------')
        else:
            self.StandbyNode = Node('Standby1DbUser')
            clear_cmd = f"rm -rf {macro.DB_BACKUP_PATH}/tesdir"
            LOG.info(clear_cmd)
            clear_msg1 = self.PrimaryNode.sh(clear_cmd).result()
            LOG.info(clear_msg1)
            clear_msg2 = self.StandbyNode.sh(clear_cmd).result()
            LOG.info(clear_msg2)
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0020执行完成---')

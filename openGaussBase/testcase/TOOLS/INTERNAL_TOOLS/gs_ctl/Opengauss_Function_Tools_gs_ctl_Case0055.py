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
Case Name   : gs_ctl reload使用-D指定正确数据库实例目录主机是否reload成功
Description :
    1.手动修改主机配置文件session_timeout参数的值
    2.gs_ctl reload指定-D设置参数为正确的数据库实例目录
    3.查看该参数是否生效
Expect      :
    1.手动修改主机配置文件session_timeout参数的值
    2.执行gs_ctl reload指定-D设置参数为正确的数据库实例目录成功
    3.查看该参数的值为1h,该参数已生效
History     :
"""

import unittest
import time

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternelTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup-----------------------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0055开始执行-----')
        self.constant = Constant()
        self.env_path = macro.DB_ENV_PATH
        self.instance_path = macro.DB_INSTANCE_PATH
        self.user_node = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.nv = ''
        self.pv = ''

    def test_system_internal_tools(self):
        LOG.info('--------------------查看参数初始值-------------------')
        msg1 = self.sh_primary.execut_db_sql('show session_timeout;')
        LOG.info(msg1)
        self.pv = msg1.splitlines()[-2].strip()
        LOG.info(self.pv)
        LOG.info('--------------------更改文件参数值-------------------')
        self.nv = self.pv
        for arg in ('s', 'min', 'h', 'd'):
            if arg in self.pv:
                self.nv = str(
                    int(self.pv.strip(arg)) + 1) + arg
        excute_cmd1 = f'''
        sed -i 's/session_timeout = {self.pv}/session_timeout = {self.nv}/' \
        {self.instance_path}/postgresql.conf
                            '''
        LOG.info(excute_cmd1)
        msg2 = self.user_node.sh(excute_cmd1).result()
        LOG.info(msg2)
        LOG.info('-------------------校验文件参数值-------------------')
        excute_cmd2 = f'cat {self.instance_path}/postgresql.conf' \
            f'|grep session_timeout;'
        LOG.info(excute_cmd2)
        msg = self.user_node.sh(excute_cmd2).result()
        LOG.info(msg)
        self.assertIn(self.nv, msg)

        LOG.info('----执行reload-------')
        excute_cmd = f'''source {self.env_path};
            gs_ctl reload -D {self.instance_path} ;
            '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.gs_ctl_reload_success, msg)
        time.sleep(10)

        LOG.info('----------------------查看参数值------------------')
        msg = self.sh_primary.execut_db_sql('show session_timeout;')
        LOG.info(msg)
        self.assertIn(self.nv, msg)

    def tearDown(self):
        LOG.info('--------------------this is tearDown----------------')
        LOG.info('-----------------------恢复参数值-----------------------')
        LOG.info('----------------------更改文件参数值--------------------')
        excute_cmd1 = f'''
        sed -i 's/session_timeout = {self.nv}/session_timeout = {self.pv}/' \
        {self.instance_path}/postgresql.conf
                                    '''
        LOG.info(excute_cmd1)
        msg2 = self.user_node.sh(excute_cmd1).result()
        LOG.info(msg2)
        excute_cmd = f'''source {self.env_path};
            gs_ctl reload -D {self.instance_path} ;
            '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        time.sleep(10)
        LOG.info('----Opengauss_Function_Tools_gs_ctl_Case0055执行完成----')

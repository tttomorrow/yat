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
Case Name   : gs_ctl reload使用-D指定正确数据库实例目录备机是否reload成功
Description :
    1.手动修改备机配置文件session_timeout参数的值
    2.gs_ctl reload指定-D设置参数为正确的数据库实例目录
    3.查看该参数是否生效
Expect      :
    1.手动修改备机配置文件session_timeout参数的值成功
    2.执行gs_ctl reload指定-D设置参数为正确的数据库实例目录成功
    3.查看该参数的值,该参数已生效
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('--------------------this is setup--------------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0056开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('-------若为单机环境，后续不执行，直接通过-------')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.user_node = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')

        LOG.info('----------------查看参数初始值-----------------')
        value_msg = self.sh_standby.execut_db_sql('show session_timeout;')
        LOG.info(value_msg)
        self.pv = value_msg.splitlines()[-2].strip()
        LOG.info(self.pv)

        LOG.info('-----------------更改文件参数值-----------------')
        self.nv = self.pv
        for arg in ('s', 'min', 'h', 'd'):
            if arg in self.pv:
                self.nv = str(
                    int(self.pv.strip(arg)) + 1) + arg
        sed_cmd = f"sed -i 's/session_timeout = {self.pv}/session_timeout" \
            f" = {self.nv}/' {macro.DB_INSTANCE_PATH}/postgresql.conf"
        LOG.info(sed_cmd)
        sed_msg = self.user_node.sh(sed_cmd).result()
        LOG.info(sed_msg)
        LOG.info('----------------校验文件参数值-------------------')
        check_cmd = f"cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep " \
            f"session_timeout;"
        LOG.info(check_cmd)
        check_msg = self.user_node.sh(check_cmd).result()
        LOG.info(check_msg)
        self.assertIn(self.nv, check_msg)

        LOG.info('-------------------执行reload---------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl reload -D {macro.DB_INSTANCE_PATH} ;
            '''
        LOG.info(excute_cmd)
        excute_msg = self.user_node.sh(excute_cmd).result()
        LOG.info(excute_msg)
        self.assertIn(self.constant.gs_ctl_reload_success, excute_msg)

        LOG.info('-------------------查看参数值-------------------')
        value_msg = self.sh_standby.execut_db_sql('show session_timeout;')
        LOG.info(value_msg)
        self.assertIn(self.nv, value_msg)

    def tearDown(self):
        LOG.info('-------------------this is tearDown--------------')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.user_node = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')

        LOG.info('-------------------恢复参数值-------------------')
        value_cmd = f"sed -i 's/session_timeout = {self.nv}/" \
            f"session_timeout = {self.pv}/' " \
            f"{macro.DB_INSTANCE_PATH}/postgresql.conf"
        LOG.info(value_cmd)
        value_msg = self.user_node.sh(value_cmd).result()
        LOG.info(value_msg)
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl reload -D {macro.DB_INSTANCE_PATH} ;
            '''
        LOG.info(excute_cmd)
        excute_msg = self.user_node.sh(excute_cmd).result()
        LOG.info(excute_msg)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0056执行完成----')

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
Case Name   : gs_ctl restart指定-m的值为fast，重新启动主机后活跃事务是否回滚
Description :
    1.开启事务
    2.执行事务，不做提交
    3.指定-m设置参数为fast，restart启动主机
    4.查看事务是否回滚
Expect      :
    1.开启事务成功
    2.执行事务，不做提交成功
    3.指定-m设置参数为fast，restart启动主机成功
    4.查看事务，事务回滚
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


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0033开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('-----------------开启并执行事务事务---------------')
        transaction_msg = self.sh_primary.execut_db_sql('''drop table if \
            exists testzl; 
            start transaction; 
            create table testzl (a integer);''')
        LOG.info(transaction_msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, transaction_msg)

        LOG.info('--------------进行重启------------------')
        restart_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary -m fast ;
            '''
        LOG.info(restart_cmd)
        restart_msg = self.PrimaryNode.sh(restart_cmd).result()
        self.assertIn(self.constant.RESTART_SUCCESS_MSG, restart_msg)
        LOG.info(restart_msg)

        time.sleep(10)

        LOG.info('-----------校验主机状态并查询事务-------------------')
        status = self.sh_primary.get_db_instance_status()
        self.assertTrue(status)
        transaction_msg = self.sh_primary.execut_db_sql(
            'select count(*) from testzl')
        LOG.info(transaction_msg)
        self.assertIn(self.constant.NOT_EXIST, transaction_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        LOG.info('----------------恢复集群状态------------------')
        restart_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary ;
            '''
        LOG.info(restart_cmd)
        restart_msg = self.PrimaryNode.sh(restart_cmd).result()
        LOG.info(restart_msg)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0033执行完成---')

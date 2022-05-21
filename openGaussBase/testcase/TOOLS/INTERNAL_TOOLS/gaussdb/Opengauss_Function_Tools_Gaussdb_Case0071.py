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
Case Type   : tools
Case Name   : 使用gaussdb开启自启动模式,参数-r的指定文件为无权限的文件是否成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.创建新的信息记录文件并去除其权限
    touch /data/zhanglu/testzl.log
    chmod 000 /data/zhanglu/testzl.log
    3.使用gaussdb工具-r指定已存在的文件启动
    gaussdb --boot -D /opt/openGauss_zl/cluster/dn1  -d 5 -r
    /data/zhanglu/testzl.log
    4.恢复-重启数据库
    gs_ctl restart -D /opt/openGauss_zl/cluster/dn1 -M primary
Expect      :
    1.关闭正在运行的数据库成功
    2.创建新的信息记录文件成功
    3.使用gaussdb工具-r指定已存在的文件启动失败，提示没有权限
    4.启动数据库成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0071 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.log_path = os.path.join(self.DB_INSTANCE_PATH, 'wf.log')

    def test_systools(self):
        self.logger.info('--------关闭正在运行的数据库--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_ctl stop -D ' \
                      f'{self.DB_INSTANCE_PATH}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('--------创建新的信息记录文件--------')
        excute_cmd2 = f'touch {self.log_path}'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode2.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.logger.info('-------使用gaussdb工具后台运行进程--------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb --boot -D ' \
                      f'{self.DB_INSTANCE_PATH} -d 5 -r {self.log_path}'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find('Permission denied') > -1)
        self.logger.info('------------恢复数据库-----------')
        excute_cmd5 = f'source {self.DB_ENV_PATH};gs_ctl restart -D ' \
                      f'{self.DB_INSTANCE_PATH};'
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        sql_cmd6 = 'drop user if exists user006 cascade;'
        msg6 = self.sh_primy.execut_db_sql(sql_cmd6)
        self.logger.info(msg6)
        self.assertTrue(msg6.find('DROP ROLE') > -1)

    def tearDown(self):
        self.logger.info('---------清理环境------------')
        excute_cmd1 = f'rm -rf {self.log_path}'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        excute_cmd2 = f'ls -l {self.log_path}'
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find('No such file or directory'))
        self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0071 finish')

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
Case Name   : 启动gaussdb进程时，使用-S参数设置以MB为单位的值启动是否成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.查看work_mem参数的值
    show work_mem;
    3.使用gaussdb工具设置-S参数的值为50MB，启动数据库
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 -S 50MB -M primary &
    4.查看work_mem参数的值是否为-S指定值及指定单位
    show work_mem;
Expect      :
    1.关闭正在运行的数据库成功
    2.查看work_mem参数的值成功，显示当前值为64MB
    3.使用gaussdb工具设置-S参数的值为50MB，启动数据库成功
    4.查看work_mem参数的值成功，为-S指定值，且单位为MB，显示50MB
History     :
"""
import unittest
from multiprocessing import Process

from testcase.utils.ComThread import ComThread
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_Gaussdb_Case0040 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.process = Process()

    def test_systools(self):
        self.logger.info("--------关闭正在运行的数据库--------")
        excute_cmd1 = f'''source {self.DB_ENV_PATH};
                gs_ctl stop -D {self.DB_INSTANCE_PATH}'''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info("--------查看进程，确定关闭成功--------")
        excute_cmd2 = f'''ps -ef|grep {self.userNode.ssh_user}'''
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertFalse(self.DB_INSTANCE_PATH in msg2)
        self.logger.info("----使用gaussdb工具设置-p参数为不存在的端口号启动---")
        excute_cmd3 = f'''source {self.DB_ENV_PATH};
             gaussdb -D {self.DB_INSTANCE_PATH} -p {self.userNode.db_port} \
-S 50MB -M primary'''
        self.logger.info(excute_cmd3)
        thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        excute_cmd6 = '''show work_mem;'''
        msg6 = self.sh_primy.execut_db_sql(excute_cmd6)
        self.logger.info(msg6)
        self.common.equal_sql_mdg(msg6, 'work_mem', '50MB', '(1 row)',
                                flag='1')

    def tearDown(self):
        self.logger.info('-----------恢复配置-----------')
        excute_cmd1 = f'''source {self.DB_ENV_PATH};
                gs_guc reload -N all -I all -c "work_mem=64MB"
                gs_om -t stop && gs_om -t start'''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        excute_cmd2 = '''show work_mem;'''
        msg2 = self.sh_primy.execut_db_sql(excute_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'work_mem', '64MB', '(1 row)',
                                flag='1')
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0040 finish-')

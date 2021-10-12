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
Case Type   : tools
Case Name   : 单机数据库使用gaussdb工具指定-E参数启动进程时，是否可以回显命令成功
Description :
    1.关闭正在运行的数据库（单机节点）
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.使用gaussdb工具指定-E参数启动数据库
    gaussdb -D /opt/openGauss_luz/cluster/dn1 -p 19703 -E &
    3.连接数据库执行DDL或DML
    create table testzl(a int);
    select * from testzl;
    4.查看pg_log，是否有命令回显
Expect      :
    1.关闭正在运行的数据库成功
    2.使用gaussdb工具指定-E参数启动数据库成功
    3.执行DDL与DML成功
    4.pg_log回显命令信息成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0062 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.file_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')

    def test_systools(self):
        self.logger.info('-------若为主备环境，后续不执行-------')
        excute_cmd = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
        self.logger.info(excute_cmd)
        msg0 = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg0)
        if 'Standby' in msg0:
            return self.logger.info('主备环境，后续不执行!')
        else:
            self.logger.info('-------查看log_directory默认路径------')
            global path_return
            check_path_cmd = 'show log_directory;'
            check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
            self.logger.info(check_path_msg)
            path_return = check_path_msg.splitlines()[2].strip()
            self.logger.info(path_return)
            self.assertTrue(path_return.find(macro.PG_LOG_PATH) > -1)
            self.logger.info('-------配置log_directory合法路径------')
            excute_cmd0 = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                          f'{macro.DB_INSTANCE_PATH} -c "log_directory=\'' \
                          f'{self.file_path}\'"'
            execute_msg4 = self.userNode.sh(excute_cmd0).result()
            self.logger.info(execute_msg4)
            self.logger.info('----查看日志路径----')
            sql_execute = f'show log_directory;'
            msg_log = self.sh_primy.execut_db_sql(sql_execute)
            self.logger.info(msg_log)
            self.common.equal_sql_mdg(msg_log, 'log_directory', self.file_path,
                                    '(1 row)', flag='1')
            self.logger.info('--------关闭正在运行的数据库--------')
            excute_cmd1 = f'source {self.DB_ENV_PATH};gs_ctl stop -D ' \
                          f'{self.DB_INSTANCE_PATH}'
            self.logger.info(excute_cmd1)
            msg1 = self.userNode.sh(excute_cmd1).result()
            self.logger.info(msg1)
            self.logger.info('-------使用gaussdb工具后台运行进程--------')
            excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb -D ' \
                          f'{self.DB_INSTANCE_PATH} -p ' \
                          f'{self.userNode.db_port} -E'
            self.logger.info(excute_cmd3)
            thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            self.logger.info('------------连接数据库执行DDL或DML-----------')
            sql_cmd3 = 'drop user if exists user006;'
            msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
            self.logger.info(msg3)
            self.assertTrue(msg3.find('DROP ROLE') > -1)
            self.logger.info('------------查看日志-----------')
            log_name = os.path.join(self.file_path, 'postgres*')
            excute_cmd4 = f'cat {log_name} |grep "drop user if exists user006"'
            msg4 = self.userNode.sh(excute_cmd4).result()
            self.logger.info(msg4)
            self.assertTrue(
                'LOG:  statement: drop user if exists user006' in msg4)
            recover_cmd = f'source {self.DB_ENV_PATH};gs_guc reload -D ' \
                          f'{macro.DB_INSTANCE_PATH} -c ' \
                          f'"log_directory=\'{path_return}\'"'
            self.logger.info(recover_cmd)
            recover_msg = self.userNode.sh(recover_cmd).result()
            self.logger.info(recover_msg)
            self.logger.info('-------查看配置是否恢复-------')
            check_path_cmd = 'show log_directory;'
            check_path_msg = self.sh_primy.execut_db_sql(check_path_cmd)
            self.logger.info(check_path_msg)
            self.assertTrue(macro.PG_LOG_PATH in path_return)

    def tearDown(self):
        self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0062 finish')

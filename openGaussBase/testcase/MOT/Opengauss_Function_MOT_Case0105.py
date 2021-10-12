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
Case Type   : MOT
Case Name   : gs_dump/gs_restore备份恢复内存表数据(目录归档格式)
Description :
    1、修改配置文件增量检查点为off,
       gs_guc set -D cluster/dn1 -c "enable_incremental_checkpoint=off"
    2、重启数据库,gs_om -t stop && gs_om -t start;
    3、连接数据库，创建内存表，插入数据；
    4、gs_dump导出(备份)内存表（目录归档格式）；
    5、gs_restore导入(恢复)内存表（目录归档格式）；
    6、清理环境
Expect      :
    1、修改成功；
    2、重启数据库成功；
    3、连接数据库成功，创建内存表成功，插入数据成功；
    4、导出数据成功;
    5、导入数据成功；
    6、清理环境成功；
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class MotParamTest(unittest.TestCase):

    def setUp(self):
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.constant = Constant()

        LOG.info('======检查参数，修改配置，并重启数据库======')
        self.config_item = "enable_incremental_checkpoint=off"
        check_res = self.sh_primysh.execut_db_sql(
            f'''show enable_incremental_checkpoint;''')
        if 'off' not in check_res.split('\n')[-2].strip():
            self.sh_primysh.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG, self.config_item)
            self.sh_primysh.restart_db_cluster()
            result = self.sh_primysh.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)

    def test_mot_dump(self):
        LOG.info("======Opengauss_Function_MOT_Case0105开始执行======")
        LOG.info("======步骤1：创建内存表======")
        self.mot_table = 'test_dump'
        self.mot_path = os.path.join(macro.DB_INSTANCE_PATH, 'mot_test')
        sql_cmd = f'''drop foreign table if exists {self.mot_table};
            create foreign table {self.mot_table}(id int);
            insert into {self.mot_table} values(generate_series(1,2000000));
            '''
        msg = self.sh_primysh.execut_db_sql(sql_cmd)
        LOG.info(msg)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg)

        LOG.info("======步骤2：gs_dump以目录归档格式导出内存表======")
        sql_cmd = f'''source {macro.DB_ENV_PATH};
            gs_dump {self.user_node.db_name} \
            -f {self.mot_path} \
            -t {self.mot_table} \
            -p {self.user_node.db_port} \
            -F d
            '''
        msg = self.user_node.sh(sql_cmd).result()
        LOG.info(msg)
        self.assertIn('dump database {} successfully'.format(
            self.user_node.db_name), msg.splitlines()[-2].strip())

        LOG.info("======步骤3：gs_restore导入目录归档格式内存表======")
        sql_cmd = f'''source {macro.DB_ENV_PATH};
            gs_restore -d {self.user_node.db_name} \
            -p {self.user_node.db_port} \
            -c {self.mot_path}        
            '''
        msg = self.user_node.sh(sql_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.RESTORE_SUCCESS_MSG,
                      msg.split('\n')[-2].strip())

    def tearDown(self):
        LOG.info("======清理环境======")
        del_cmd = f'''source {macro.DB_ENV_PATH};
            gsql {self.user_node.db_name} \
            -p {self.user_node.db_port} \
            -c "drop foreign table {self.mot_table} cascade";
            rm -rf {self.mot_path}
            '''
        LOG.info(del_cmd)
        del_res = self.user_node.sh(del_cmd).result()
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, del_res)
        LOG.info('======Opengauss_Function_MOT_Case0105执行结束======')

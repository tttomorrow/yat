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
Case Name   : MOT设置high_reclaim_threshold=0KB进行SQL语句测试
Description :
    1、修改配置文件mot.conf中high_reclaim_threshold=0KB
    2、重启数据库,gs_om -t stop && gs_om -t start
    3、查看配置文件参数是否生效,cat cluster/dn1/mot.conf | grep high_reclaim_threshold
    4、查看pg_log日志信息,cat cluster/../pg_log/xxx.log
    5、连接数据库,创建内存表，执行DML语句;
    6、清理数据;
Expect      :
    1、修改成功；
    2、重启数据库成功；
    3、查看配置文件，参数修改生效；
    4、查看日志，存在参数WARNING信息；
    5、连接数据库成功，创建内存表成功；
    6、清理环境成功；
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
CONSTANT = Constant()
DB_ENV_PATH = macro.DB_ENV_PATH
MOT_CONF = os.path.join(macro.DB_INSTANCE_PATH, 'mot.conf')
MOT_LOG = os.path.join(macro.PG_LOG_PATH, macro.DN_NODE_NAME.split('/')[0])
CONFIG_PARAM = 'high_reclaim_threshold = 0KB'


class MotParamTest(unittest.TestCase):

    def setUp(self):
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.mot_table = 'mot_test'

        LOG.info('======检查参数，修改配置，并重启数据库======')
        self.config_item = "enable_incremental_checkpoint=off"
        check_res = self.sh_primysh.execut_db_sql(
            f'''show enable_incremental_checkpoint;''')
        if 'off' != check_res.split('\n')[-2].strip():
            self.sh_primysh.execute_gsguc(
                'set', CONSTANT.GSGUC_SUCCESS_MSG, self.config_item)
            self.sh_primysh.restart_db_cluster()
            result = self.sh_primysh.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)

    def test_mot_param(self):
        LOG.info("======Opengauss_Function_MOT_Case0251开始执行======")
        LOG.info("======步骤1：修改配置文件设置high_reclaim_threshold=0KB启动数据库======")
        add_cmd = f'''source {DB_ENV_PATH}
            gs_ssh -c "echo -e '{CONFIG_PARAM}' >> {MOT_CONF}" '''
        LOG.info(add_cmd)
        add_res = self.user_node.sh(add_cmd).result()
        LOG.info(add_res)
        self.assertIn('Successfully execute command on all nodes', add_res)
        self.sh_primysh.restart_db_cluster()
        result = self.sh_primysh.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

        LOG.info("======步骤2：查看mot.conf文件参数修改是否生效======")
        cat_cmd = f'''cat {MOT_CONF} | grep high_reclaim_threshold'''
        msg = self.user_node.sh(cat_cmd).result()
        LOG.info(msg)
        self.assertIn(CONFIG_PARAM, msg.split('\n')[-1].strip())

        LOG.info("======步骤3：查看pg_log日志，存在参数WARNING信息======")
        sql_cmd = f'''ls -t {MOT_LOG} | head -1'''
        LOG.info(sql_cmd)
        log_msg = self.user_node.sh(sql_cmd).result()
        LOG.info(log_msg)

        cat_cmd = f'''cd {MOT_LOG}
            cat {log_msg} | grep high_reclaim_threshold'''
        LOG.info(cat_cmd)
        cmd_msg = self.user_node.sh(cat_cmd).result()
        LOG.info(cmd_msg)
        self.assertIn('WARNING', cmd_msg)
        self.assertIn('Configuration of high_reclaim_threshold=0'
                      ' is out of bounds [1048576, 67108864]', cmd_msg)

        LOG.info("======步骤4：连接数据库，创建内存表，执行DML操作======")
        sql_cmd = f'''drop foreign table if exists {self.mot_table};
            create foreign table {self.mot_table}(id int);
            insert into {self.mot_table} 
            values(generate_series(1,2000000));
            select count(*) from {self.mot_table};                    
            '''
        sql_msg = self.sh_primysh.execut_db_sql(sql_cmd)
        LOG.info(sql_msg)
        self.assertTrue(CONSTANT.CREATE_FOREIGN_SUCCESS_MSG in sql_msg
                        and CONSTANT.INSERT_SUCCESS_MSG in sql_msg
                        and '2000000' in sql_msg)

    def tearDown(self):
        LOG.info("======步骤6：清理环境，删除参数======")
        del_cmd = f'''source {macro.DB_ENV_PATH};
            gsql {self.user_node.db_name} 
            -p {self.user_node.db_port} 
            -c "drop foreign table {self.mot_table} cascade"
            sed -i '$d' {MOT_CONF}
            '''
        LOG.info(del_cmd)
        self.user_node.sh(del_cmd)
        LOG.info('======Opengauss_Function_MOT_Case0251执行结束======')

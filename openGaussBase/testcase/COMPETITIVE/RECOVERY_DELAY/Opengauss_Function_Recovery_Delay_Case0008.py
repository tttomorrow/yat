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
Case Type   : 数据库系统
Case Name   : 1主2备事务同步方式local时备机备份延迟
Description :
    1. 创建表，并插入数据
    2. 设置synchronous_commit=on，设置synchronous_standby_names=dn_6002
    3.重启数据库
    4.备节点使用alter方式设置
    5.查询集群同步方式
    6.等待主备一致
    7.更新表，30s后再更新
    8.等待3s，查询备机
    9.等待80s,备机查询
    10.再等40s，备机查询
Expect      :
    1.配置成功
    2.重启数据库成功
    3.设置成功
    4.集群同步方式为1同步1异步
    5.主备一致
    6.创建表并插入数据成功
    7.备1同步，备2未同步
    8.所有备均同步
    9.更新成功
    10.数据未更新
    11.备1数据更新成功，备2未更新
    12.均更新成功
    13.删除成功
    14.配置成功
    15.备机查询不到该表
History     :
"""
import unittest
import os
import time
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class RecoveryDelay(unittest.TestCase):
    db_primary_user_node = Node(node='PrimaryDbUser')
    commshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0008 start---")
        self.constant = Constant()
        self.log.info("---------get number of node---------")
        self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
        result = self.commshpri.get_db_cluster_status('detail')
        self.log.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.comshsta = []
        self.log.info(self.node_num)
        self.conf_path = os.path.join(
            macro.DB_INSTANCE_PATH, macro.DB_PG_CONFIG_NAME)
        self.tb_name = 'tb_case0008'
        self.rootnodelist = ['Standby1Root', 'Standby2Root']

        self.log.info('------同步集群时间--------')
        current = self.db_primary_user_node.sh(
            "date \"+%m/%d/%Y %H:%M:%S\"").result()
        self.log.info(current)
        datecmd = f'date -s "{current}"'
        for i in range(int(self.node_num) - 1):
            db_standby_node = Node(node=self.rootnodelist[i])
            result = db_standby_node.sh(datecmd).result()
            self.log.info(datecmd)
            self.log.info(result)

    def test_recovery_delay(self):
        if self.node_num > 2:
            for i in range(int(self.node_num) - 1):
                self.comshsta.append(CommonSH(self.nodelist[i]))

            self.log.info('--------创建表，并插入数据-------')
            sql = f"drop table if exists {self.tb_name};" \
                f"create table {self.tb_name}(i int, s char(10));" \
                f"insert into {self.tb_name} values(5,'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)

            self.log.info('------备份postgres.conf文件----------')
            shell_cmd = f"cp {self.conf_path} {self.conf_path}_testbak"
            self.log.info(shell_cmd)
            result = self.db_primary_user_node.sh(shell_cmd).result()
            self.log.info(result)

            self.log.info('--------设置synchronous_commit=on-------')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'synchronous_commit=on')
            self.assertTrue(result)

            self.log.info('---设置synchronous_standby_names=dn_6002--')
            shell_cmd = f"cat {self.conf_path} | " \
                f"grep synchronous_standby_names"
            result = self.db_primary_user_node.sh(shell_cmd).result()
            self.log.info(result)
            shell_cmd = f"sed -i \"s/" \
                f"{result.split('#')[0]}/synchronous_standby_names='" \
                f"{macro.DN_NODE_NAME.split('/')[1]}'/g\" {self.conf_path}"
            self.log.info(shell_cmd)
            result_tmp = self.db_primary_user_node.sh(shell_cmd).result()
            self.log.info(result_tmp)

            self.log.info('----------重启数据库-----------')
            result = self.commshpri.stop_db_cluster()
            self.assertTrue(result)
            result = self.commshpri.start_db_cluster()
            self.assertTrue(result)

            self.log.info('-----备节点使用alter方式设置----')
            for i in range(int(self.node_num) - 1):
                sql = f"alter SYSTEM set " \
                    f"recovery_min_apply_delay to '2min' "
                result  = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn(self.constant.alter_system_success_msg, result)

            self.log.info('-----------查询参数-----------')
            result = self.commshpri.execut_db_sql('show synchronous_commit;')
            self.log.info(result)
            self.assertIn('on', result)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(
                    'show recovery_min_apply_delay;')
                self.log.info(result)
                self.assertIn(f'2min', result)
            result = self.commshpri.execut_db_sql(
                'show synchronous_standby_names;')
            self.log.info(result)
            self.assertIn(f"{macro.DN_NODE_NAME.split('/')[1]}", result)

            self.log.info('--------查询集群同步方式-----')
            sql = "select * from pg_stat_replication;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('Sync', result)
            self.assertIn('Async', result)

            self.log.info('--------等待主备一致------------')
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].check_data_consistency()
                self.assertTrue(result)

            self.log.info('--------更新表，40s后再更新------')
            sql = f"insert into {self.tb_name} values(3, 'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertTrue(self.constant.INSERT_SUCCESS_MSG, result)
            time.sleep(40)
            sql = f"delete from {self.tb_name} where i=5;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertTrue(self.constant.INSERT_SUCCESS_MSG, result)

            self.log.info('-------等待3s，查询备机------------')
            time.sleep(3)
            sql = f"select * from {self.tb_name};" \
                f"select count(*) from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertNotIn('3 | test', result)
                self.assertIn('1', result)
                self.assertIn('5 | test', result)

            self.log.info('-------等待120s,备机查询------------')
            time.sleep(130-40)
            sql = f"select * from {self.tb_name};" \
                f"select count(*) from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('3 | test', result)
                self.assertIn('2', result)
                self.assertIn('5 | test', result)

            self.log.info('-------再等待40s，查询备机------------')
            time.sleep(40)
            sql = f"select * from {self.tb_name};" \
                f"select count(*) from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('3 | test', result)
                self.assertIn('1', result)
                self.assertNotIn('5 | test', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('--------删除表-------')
        sql = f"drop table if exists {self.tb_name};"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)

        self.log.info('--------------还原配置文件-------------')
        shell_cmd = f"rm -rf {self.conf_path};" \
            f"cp {self.conf_path}_testbak {self.conf_path};" \
            f"rm -rf {self.conf_path}_testbak"
        self.log.info(shell_cmd)
        result = self.db_primary_user_node.sh(shell_cmd).result()
        self.log.info(result)

        self.log.info('-------------还原recovery_min_apply_delay----------')
        result = self.commshpri.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'recovery_min_apply_delay=0')
        self.log.info(result)

        self.log.info('-----------重启数据库-----------')
        result = self.commshpri.stop_db_cluster()
        self.log.info(result)
        result = self.commshpri.start_db_cluster()
        self.log.info(result)

        self.log.info("---Opengauss_Function_Recovery_Delay_Case0008 end--")
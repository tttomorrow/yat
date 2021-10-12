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
Case Name   : 1主2备事务同步方式remote_apply时备机备份延迟
Description :
    1.创建表
    2.设置synchronous_commit=remote_apply,synchronous_standby_names=dn_6002,dn_6003
    3.重启数据库
    4.备节点1/备节点2使用alter方式设置recovery_min_apply_delay
    5.查询集群同步方式
    6.等待主备一致
    7.插入数据
    8.备机查询
    9.修改synchronous_standby_names为dn_6002,dn_6003
    10.重启集群
    11.更新数据
    12.查询数据
Expect      :
    1.创建成功
    2.配置成功
    3.重启数据库成功
    4.设置成功
    5.集群同步方式为1同步1异步
    6.主备一致
    7.创建表并插入数据成功，且等待时间大于1min
    8.备1同步，备2未同步
    9.修改成功
    10.重启成功
    11.更新成功，且等待时间大于1min
    12.备1同步，备2未同步
History     :
"""
import unittest
import os
import datetime
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
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0006 start---")
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
        self.tb_name = 'tb_case0006'
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
                f"create table {self.tb_name}(i int, s char(10));"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)

            self.log.info('------备份postgres.conf文件----------')
            shell_cmd = f"cp {self.conf_path} {self.conf_path}_testbak"
            self.log.info(shell_cmd)
            result = self.db_primary_user_node.sh(shell_cmd).result()
            self.log.info(result)

            self.log.info('--------设置synchronous_commit=remote_apply-------')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'synchronous_commit=remote_apply')
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
                    f"recovery_min_apply_delay to '{str(i+1)}min' "
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
                self.assertIn(f'{str(i+1)}min', result)
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

            self.log.info('--------插入数据-------')
            start = datetime.datetime.now()
            sql = f"insert into {self.tb_name} values(5,'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
            end = datetime.datetime.now()
            execute_time = (end - start).seconds
            self.log.info(execute_time)
            self.assertLessEqual(55, int(execute_time))

            self.log.info('---查询数据-----')
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 0 == i:
                    self.assertIn('5 | test', result)
                else:
                    self.assertIn('(0 rows)', result)

            self.log.info('---等待60s,查询数据-----')
            time.sleep(60)
            sql = f"select * from {self.tb_name};"
            flg = 0
            for exc_i in range(60):
                flg = 0
                for i in range(int(self.node_num) - 1):
                    result = self.comshsta[i].execut_db_sql(sql)
                    self.log.info(result)
                    if '5 | test' in result:
                        flg = flg + 1
                if 2 == flg:
                    break
                time.sleep(10)
            self.assertEqual(flg, 2)

            self.log.info('---设置synchronous_standby_names=dn_6002,dn_6003--')
            shell_cmd = f"cat {self.conf_path} | " \
                f"grep synchronous_standby_names"
            result = self.db_primary_user_node.sh(shell_cmd).result()
            self.log.info(result)
            shell_cmd = f"sed -i \"s/" \
                f"{result.split('#')[0]}/synchronous_standby_names='" \
                f"{macro.DN_NODE_NAME.split('/')[1]}," \
                f"{macro.DN_NODE_NAME.split('/')[2]}'/g\" {self.conf_path}"
            self.log.info(shell_cmd)
            result_tmp = self.db_primary_user_node.sh(shell_cmd).result()
            self.log.info(result_tmp)

            self.log.info('----------重启数据库-----------')
            result = self.commshpri.stop_db_cluster()
            self.assertTrue(result)
            result = self.commshpri.start_db_cluster()
            self.assertTrue(result)

            self.log.info('--------查询集群同步方式-----')
            sql = "select * from pg_stat_replication;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('Sync', result)

            self.log.info('--------等待主备一致------------')
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].check_data_consistency()
                self.assertTrue(result)

            self.log.info('--------插入数据-------')
            start = datetime.datetime.now()
            sql = f"insert into {self.tb_name} values(5,'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
            end = datetime.datetime.now()
            execute_time = (end - start).seconds
            self.log.info(execute_time)
            self.assertLessEqual(55, int(execute_time))
            start = datetime.datetime.now()
            sql = f"update {self.tb_name} set i=7;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('UPDATE', result)
            end = datetime.datetime.now()
            update_execute_time = (end - start).seconds
            self.log.info(execute_time)
            self.assertLessEqual(55, int(update_execute_time))
            time.sleep(5)

            self.log.info('---查询数据-----')
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('2 rows', result)
                if 0 == i:
                    self.assertIn('7 | test', result)
                else:
                    self.assertIn('5 | test', result)

            self.log.info('---等待150s,查询数据-----')
            time.sleep(150)
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('7 | test', result)
                self.assertIn('2 rows', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
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

        self.log.info('--------删除表-------')
        sql = f"drop table if exists {self.tb_name};"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0006 end--")
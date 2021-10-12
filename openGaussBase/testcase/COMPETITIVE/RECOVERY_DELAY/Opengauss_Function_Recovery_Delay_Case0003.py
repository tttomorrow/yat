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
    1.设置synchronous_commit=local,synchronous_standby_names=dn_6002,dn_6003
    2.重启数据库
    3.备节点1使用alter方式设置recovery_min_apply_delay
    4.查询集群同步方式
    5.等待主备一致
    6.创建数据库test,并创建表插入数据
    7.postgres数据库创建表，并插入数据
    8.等待10秒,备机查询，分别查询postgres及test数据库下数据
    9.等待2min，查询备机，分别查询postgres
    10.更新postgres表
    11.设置recovery_min_apply_delay=0
    12.查询备机
    13.更新postgres表
    14.查询备机
Expect      :
    1.设置成功
    2.重启数据库成功
    3.设置成功
    4.两个备机状态为Async
    5.主备同步
    6.创建模式及表并插入数据成功
    7.创建数据成功
    8.备1未同步，备2同步
    9.两个备机均同步
    10.更新成功
    11.设置成功
    12.备机依旧2min后更新
    13.更新成功
    14.备机立即同步
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
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0003 start---")
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
        self.tb_name = 'tb_case0003'
        self.db_name = 'db_case0003'
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

            self.log.info('------备份postgres.conf文件----------')
            shell_cmd = f"cp {self.conf_path} {self.conf_path}_testbak"
            self.log.info(shell_cmd)
            result = self.db_primary_user_node.sh(shell_cmd).result()
            self.log.info(result)

            self.log.info('--------设置synchronous_commit=local-------')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'synchronous_commit=local')
            self.assertTrue(result)

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

            self.log.info('-----备节点1使用alter方式设置----')
            sql = f"alter SYSTEM set recovery_min_apply_delay to '2min' "
            result  = self.comshsta[0].execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.alter_system_success_msg, result)

            self.log.info('-----------查询参数-----------')
            result = self.commshpri.execut_db_sql('show synchronous_commit;')
            self.log.info(result)
            self.assertIn('on', result)
            result = self.commshpri.execut_db_sql(
                'show recovery_min_apply_delay;')
            self.log.info(result)
            self.assertIn('0', result)
            result = self.comshsta[0].execut_db_sql(
                'show recovery_min_apply_delay;')
            self.log.info(result)
            self.assertIn('2min', result)
            result = self.commshpri.execut_db_sql(
                'show synchronous_standby_names;')
            self.log.info(result)
            self.assertIn(f"{macro.DN_NODE_NAME.split('/')[1]},"
                          f"{macro.DN_NODE_NAME.split('/')[2]}", result)

            self.log.info('--------查询集群同步方式-----')
            sql = "select * from pg_stat_replication;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('Async', result)

            self.log.info('--------等待主备一致------------')
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].check_data_consistency()
                self.assertTrue(result)

            self.log.info('--------创建数据库test,并创建表插入数据-------')
            time.sleep(5)
            sql = f"create database {self.db_name};"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, result)
            sql = f"drop table if exists {self.tb_name};" \
                f"create table {self.tb_name}(i int, s char(10));" \
                f"insert into {self.tb_name} values(2,'test2');"
            result = self.commshpri.execut_db_sql(sql, dbname=self.db_name)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)

            self.log.info('--------创建表，并插入数据-------')
            sql = f"drop table if exists {self.tb_name};" \
                f"create table {self.tb_name}(i int, s char(10));" \
                f"insert into {self.tb_name} values(1,'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)

            self.log.info('---等待10秒,备机查询，分别查询tpcc及test数据库下数据-----')
            time.sleep(10)
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 0 == i:
                    self.assertIn(self.constant.NOT_EXIST, result)
                else:
                    self.assertIn('1 | test', result)
                result = self.comshsta[i].execut_db_sql(
                    sql, dbname=self.db_name)
                self.log.info(result)
                if 0 == i:
                    self.assertIn(self.constant.NOT_EXIST, result)
                else:
                    self.assertIn('2 | test2', result)

            self.log.info('-------等待2min，查询备机------------')
            time.sleep(120)
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('1 | test', result)
                result = self.comshsta[i].execut_db_sql(
                    sql, dbname=self.db_name)
                self.log.info(result)
                self.assertIn('test2', result)

            self.log.info('--------更新表-------')
            sql = f"update {self.tb_name} set s='update';"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertTrue(self.constant.UPDATE_SUCCESS_MSG, result)

            self.log.info('-----使用alter方式设置----')
            sql = f"alter SYSTEM set recovery_min_apply_delay to '0';" \
                f"select pg_sleep(5);show recovery_min_apply_delay;"
            result = self.comshsta[0].execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('ALTER', result)

            self.log.info('-------查询备机------------')
            time.sleep(120)
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('1 | update', result)

            self.log.info('--------更新表--------------')
            sql = f"update {self.tb_name} set s='etadpu';"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertTrue(self.constant.UPDATE_SUCCESS_MSG, result)

            self.log.info('-------查询备机------------')
            time.sleep(5)
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('1 | etadpu', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('--------删除表-------')
        sql = f"drop table if exists {self.tb_name};"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)

        self.log.info('--------------删除数据库----------------')
        sql = f"drop database if exists {self.db_name};"
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

        self.log.info("---Opengauss_Function_Recovery_Delay_Case0003 end--")
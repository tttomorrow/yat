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
Case Name   : 1主2备事务同步方式remote_receive时备机备份延迟
Description :
    1.设置synchronous_commit=remote_receive，synchronous_standby_names
    2.重启数据库
    3.使用gs_guc reload方式设置recovery_min_apply_delay
    4.查询集群同步方式
    5.等待主备一致
    6.创建表并插入数据，创建物化视图
    7.等待3秒,备机查询
    8.等待2min，查询备机
    9.删除表
    10.备机查询
    11.2min后设置recovery_min_apply_delay=0
    12.备机查询
Expect      :
    1.设置成功
    2.重启数据库成功
    3.设置成功
    4.两个备机状态为Async
    5.主备同步
    6.创建模式及表并插入数据成功
    7.数据未同步
    8.数据同步
    9.删除表成功
    10.备机可查询到数据
    11.设置成功
    12.无法查到该表
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
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0005 start---")
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
        self.tb_name = 'tb_case0005'
        self.mv_name = 'mv_case005'
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

            self.log.info('------设置synchronous_commit=remote_receive----')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'synchronous_commit=remote_receive')
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

            self.log.info('-----设置recovery_min_apply_delay=2min----')
            result = self.commshpri.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                'recovery_min_apply_delay=2min')
            self.assertTrue(result)

            self.log.info('-----------查询参数-----------')
            result = self.commshpri.execut_db_sql('show synchronous_commit;')
            self.log.info(result)
            self.assertIn('remote_receive', result)
            result = self.commshpri.execut_db_sql(
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
            self.assertIn('Sync', result)
            self.assertIn('Potential', result)

            self.log.info('--------等待主备一致------------')
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].check_data_consistency()
                self.assertTrue(result)

            self.log.info('--------创建表并插入数据，创建物化视图-------')
            sql = f"drop table if exists {self.tb_name};" \
                f"create table {self.tb_name}(i int, s char(10));" \
                f"insert into {self.tb_name} values(1,'test');" \
                f"create MATERIALIZED view {self.mv_name} " \
                f"as select * from {self.tb_name};"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)

            self.log.info('-------等待3秒,备机查询------------')
            time.sleep(3)
            sql = [f"select sysdate;select * from {self.tb_name};",
                   f"select sysdate;select * from {self.mv_name};"]
            for i in range(int(self.node_num) - 1):
                for j in range(2):
                    result = self.comshsta[i].execut_db_sql(sql[j])
                    self.log.info(result)
                    self.assertIn(self.constant.NOT_EXIST, result)

            self.log.info('-------等待2min，查询备机------------')
            time.sleep(120)
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('1 | test', result)
            sql = f"select sysdate;select * from {self.mv_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('1 | test', result)

            self.log.info('--------删除表-------')
            sql = f"drop table if exists {self.tb_name} CASCADE;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertTrue(self.constant.DROP_TABLE_SUCCESS, result)

            self.log.info('-------查询备机------------')
            time.sleep(120)
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn(self.constant.NOT_EXIST, result)

            self.log.info('----等待2min设置recovery_min_apply_delay=0----')
            time.sleep(120)
            result = self.commshpri.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                'recovery_min_apply_delay=0')
            self.assertTrue(result)

            self.log.info('-------查询备机------------')
            time.sleep(5)
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn(self.constant.NOT_EXIST, result)
            sql = f"select sysdate;select * from {self.mv_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn(self.constant.NOT_EXIST, result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('--------删除物化视图-------')
        sql = f"drop MATERIALIZED view if exists {self.mv_name};"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)

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

        self.log.info("---Opengauss_Function_Recovery_Delay_Case0005 end--")
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
Case Type   : 数据库系统
Case Name   : 1主1备1级联，备节点事务提交方式为on
Description :
    1.将备节点1切换为级联备
    2.设置事务同步方式为on
    3.配置所有节点备份延迟为2min
    4.重启集群
    5.查询集群同步方式
    6.创建表并插入数据
    7.等待5s查询备机
    8.等待2min查询备机
    9.插入数据30s后再删除数据
    10.等待5s查询备机
    11.等待2min查询备机，再等待40s查询备机
    12.延迟参数修改为0
    13.重启集群
    14.更新表
    15.查询集群
Expect      :
    1.切换成功
    2.设置成功
    3.设置成功
    4.重启成功
    5.级联备为异步，备节点为同步
    6.创建并插入成功
    7.查询不到
    8.数据同步
    9.数据更新成功
    10.备节点未同步
    11.2min后查询备机可查询到新插入数据，再40s后查询原数据才被删除
    12.配置成功
    13.重启成功
    14.更新成功
    15.备节点同步
History     :
"""
import unittest
import time
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class RecoveryDelay(unittest.TestCase):
    db_primary_user_node = Node(node='PrimaryDbUser')
    commshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0009 start---")
        self.constant = Constant()
        self.log.info("---------get number of node---------")
        self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
        result = self.commshpri.get_db_cluster_status('detail')
        self.log.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.comshsta = []
        self.log.info(self.node_num)
        self.tb_name = 'tb_case0009'

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

            self.log.info('-------将备节点1切换为级联备---------')
            result = self.comshsta[0].build_standby('-M cascade_standby')
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result)
            result = self.comshsta[0].exec_refresh_conf()
            self.assertTrue(result)

            self.log.info('--------设置synchronous_commit=on-------')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'synchronous_commit=on')
            self.assertTrue(result)

            self.log.info('-----设置recovery_min_apply_delay=2min----')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'recovery_min_apply_delay=2min')
            self.assertTrue(result)

            self.log.info('----------重启数据库-----------')
            result = self.commshpri.stop_db_cluster()
            self.assertTrue(result)
            result = self.commshpri.start_db_cluster()
            self.assertTrue(result)

            self.log.info('-----------查询参数-----------')
            result = self.commshpri.execut_db_sql('show synchronous_commit;')
            self.log.info(result)
            self.assertIn('on', result)
            result = self.commshpri.execut_db_sql(
                'show recovery_min_apply_delay;')
            self.log.info(result)
            self.assertIn('2min', result)

            self.log.info('--------查询集群同步方式-----')
            sql = "select * from pg_stat_replication;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('Quorum', result)
            result = self.comshsta[1].execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('Async', result)

            self.log.info('--------等待主备一致------------')
            result = self.comshsta[1].check_data_consistency()
            self.assertTrue(result)
            for i in range(90):
                result = self.commshpri.check_cascade_standby_consistency()
                if result:
                    break
                time.sleep(20)
            self.assertTrue(result)

            self.log.info('--------创建表，并插入数据-------')
            sql = f"drop table if exists {self.tb_name};" \
                f"create table {self.tb_name}(i int, s char(10));" \
                f"insert into {self.tb_name} values(5,'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)

            self.log.info('-------等待5秒,备机查询------------')
            time.sleep(5)
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn(self.constant.NOT_EXIST, result)

            self.log.info('-------等待135，查询备机------------')
            time.sleep(135)
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('5 | test', result)

            self.log.info('--------插入数据30s后再删除数据------')
            sql = f"insert into {self.tb_name} values(3, 'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertTrue(self.constant.INSERT_SUCCESS_MSG, result)
            time.sleep(30)
            sql = f"delete from {self.tb_name} where i=5;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertTrue(self.constant.INSERT_SUCCESS_MSG, result)

            self.log.info('-------等待5s，查询备机------------')
            time.sleep(5)
            sql = f"select * from {self.tb_name};" \
                f"select count(*) from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertNotIn('3 | test', result)
                self.assertIn('1', result)
                self.assertIn('5 | test', result)

            self.log.info('-------等待2min查询备机，再等待30s查询备机------------')
            time.sleep(130-30)
            sql = f"select * from {self.tb_name};" \
                f"select count(*) from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('3 | test', result)
                self.assertIn('2', result)
                self.assertIn('5 | test', result)
            time.sleep(30)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('3 | test', result)
                self.assertIn('1', result)
                self.assertNotIn('5 | test', result)

            self.log.info('----设置recovery_min_apply_delay=0----')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'recovery_min_apply_delay=0')
            self.assertTrue(result)

            self.log.info('-----------重启数据库-----------')
            result = self.commshpri.stop_db_cluster()
            self.assertTrue(result)
            result = self.commshpri.start_db_cluster()
            self.assertTrue(result)

            self.log.info('--------更新表------')
            sql = f'update {self.tb_name} set i=100;'
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('UPDATE', result)

            self.log.info('-------查询备机------------')
            sql = f"select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('100 | test', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('--------删除表-------')
        sql = f"drop table if exists {self.tb_name};"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)

        self.log.info('--------还原集群-------')
        if self.node_num > 2:
            self.comshsta[0].build_standby('-M standby')
            result = self.comshsta[0].exec_refresh_conf()
            self.log.info(result)

        self.log.info('-------------还原参数----------')
        result = self.commshpri.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'recovery_min_apply_delay=0')
        self.log.info(result)

        self.log.info('-----------重启数据库-----------')
        result = self.commshpri.stop_db_cluster()
        self.log.info(result)
        result = self.commshpri.start_db_cluster()
        self.log.info(result)

        self.log.info("---Opengauss_Function_Recovery_Delay_Case0009 end--")
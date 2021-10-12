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
Case Name   : 1主1备1级联，备节点事务提交方式为remote_apply
Description :
    1.将备节点1切换为级联备
    2.设置事务同步方式为remote_receive
    3.重启集群
    4.配置级联节点备份延迟为1min
    5.查询集群同步方式
    6.创建表并插入数据
    7.等待5s查询备机
    8.等待1min查询备机
    9.修改备节点延迟为1min
    10.插入数据
    11.等待5秒,备机查询
    12.修改延迟为0
    13.删除表
    14.备机查询
Expect      :
    1.切换成功
    2.设置成功
    3.重启成功
    4.设置成功
    5.级联备为异步，备节点为异步
    6.创建并插入成功
    7.备节点同步，级联备未同步
    8.均可查询到
    9.修改成功
    10.插入成功，耗时大于等于60s
    11.数据同步
    12.设置成功
    13.删除成功
    14.数据同步
History     :
"""
import unittest
import datetime
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
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0014 start---")
        self.constant = Constant()
        self.log.info("---------get number of node---------")
        self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
        self.rootnodelist = ['Standby1Root', 'Standby2Root']
        result = self.commshpri.get_db_cluster_status('detail')
        self.log.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.comshsta = []
        self.log.info(self.node_num)
        self.tb_name = 'tb_case0013'

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
            result = self.comshsta[1].build_standby('-M cascade_standby')
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result)
            result = self.comshsta[1].exec_refresh_conf()
            self.assertTrue(result)

            self.log.info('--------设置synchronous_commit=remote_receive-------')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'synchronous_commit=remote_apply')
            self.assertTrue(result)

            self.log.info('----------重启数据库-----------')
            result = self.commshpri.stop_db_cluster()
            self.assertTrue(result)
            result = self.commshpri.start_db_cluster()
            self.assertTrue(result)

            self.log.info('----设置recovery_min_apply_delay=1min----')
            sql = f"alter SYSTEM set " \
                f"recovery_min_apply_delay to '1min' "
            result = self.comshsta[1].execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.alter_system_success_msg, result)

            self.log.info('-----------查询参数-----------')
            result = self.commshpri.execut_db_sql('show synchronous_commit;')
            self.log.info(result)
            self.assertIn('remote_apply', result)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(
                    'show recovery_min_apply_delay;')
                self.log.info(result)
                if 1 == i:
                    self.assertIn('1min', result)
                else:
                    self.assertIn('0', result)

            self.log.info('--------查询集群同步方式-----')
            sql = "select * from pg_stat_replication;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('Quorum', result)
            result = self.comshsta[0].execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('Async', result)

            self.log.info('--------等待主备一致------------')
            result = self.comshsta[0].check_data_consistency()
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
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 1 == i:
                    self.assertIn(self.constant.NOT_EXIST, result)
                else:
                    self.assertIn('5 | test', result)

            self.log.info('-------等待1min，查询备机------------')
            time.sleep(60)
            sql = f"select sysdate;select * from {self.tb_name};"
            for exec_time in range(5):
                flag = 0
                for i in range(int(self.node_num) - 1):
                    result = self.comshsta[i].execut_db_sql(sql)
                    self.log.info(result)
                    if '5 | test' in result:
                        flag += 1
                if flag > 1:
                    break
                time.sleep(10)
            self.assertEqual(2, flag)

            self.log.info('----设置备节点recovery_min_apply_delay=1min----')
            sql = f"alter SYSTEM set " \
                f"recovery_min_apply_delay to '1min' "
            result = self.comshsta[0].execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.alter_system_success_msg, result)

            self.log.info('----------插入数据---------')
            sql = f"insert into {self.tb_name} values (4,'test');"
            start = datetime.datetime.now()
            result = self.commshpri.execut_db_sql(sql)
            end = datetime.datetime.now()
            self.log.info(result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
            execute_time = (end - start).seconds
            self.log.info(execute_time)
            self.assertLessEqual(60, int(execute_time))

            self.log.info('-------等待5秒,备机查询------------')
            time.sleep(5)
            sql = f"select sysdate;select * from {self.tb_name};"
            for exec_time in range(5):
                flag = 0
                for i in range(int(self.node_num) - 1):
                    result = self.comshsta[i].execut_db_sql(sql)
                    self.log.info(result)
                    if '5 | test' in result and '4 | test' in result:
                        flag += 1
                if flag > 1:
                    break
                time.sleep(10)
            self.assertEqual(2, flag)

            self.log.info('--------等待主备一致------------')
            result = self.comshsta[0].check_data_consistency()
            self.assertTrue(result)
            for i in range(90):
                result = self.commshpri.check_cascade_standby_consistency()
                if result:
                    break
                time.sleep(20)
            self.assertTrue(result)

            self.log.info('----设置recovery_min_apply_delay=0----')
            result = self.commshpri.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                'recovery_min_apply_delay=0')
            self.assertTrue(result)

            self.log.info('--------删除表-------')
            time.sleep(5)
            sql = f"drop table if exists {self.tb_name};"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.DROP_TABLE_SUCCESS, result)

            self.log.info('-------备机查询------------')
            time.sleep(1)
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn(self.constant.NOT_EXIST, result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info('--------删除表-------')
        sql = f"drop table if exists {self.tb_name};"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)

        self.log.info('--------还原集群-------')
        if self.node_num > 2:
            self.comshsta[1].build_standby('-M standby')
            result = self.comshsta[1].exec_refresh_conf()
            self.log.info(result)

        self.log.info('-------------还原参数----------')
        result = self.commshpri.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'recovery_min_apply_delay=0')
        self.log.info(result)
        result = self.commshpri.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'synchronous_commit=on')
        self.log.info(result)

        self.log.info('-----------重启数据库-----------')
        result = self.commshpri.stop_db_cluster()
        self.log.info(result)
        result = self.commshpri.start_db_cluster()
        self.log.info(result)

        self.log.info("---Opengauss_Function_Recovery_Delay_Case0014 end--")
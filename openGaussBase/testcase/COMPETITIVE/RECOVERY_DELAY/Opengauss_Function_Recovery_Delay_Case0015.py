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
Case Name   : 1主1备1级联，备节点与级联备延迟时间不同
Description :
    见云龙，脚本过大无法写入
Expect      :
    见云龙，脚本过大无法写入
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
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0015 start---")
        self.constant = Constant()
        self.log.info("---------get number of node---------")
        self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
        self.rootnodelist = ['Standby1Root', 'Standby2Root']
        result = self.commshpri.get_db_cluster_status('detail')
        self.log.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.comshsta = []
        self.log.info(self.node_num)
        self.tb_name = 'tb_case0015'

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

            self.log.info('--------设置synchronous_commit=remote_apply-------')
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
            sql = f"alter SYSTEM set " \
                f"recovery_min_apply_delay to '2min' "
            result = self.comshsta[0].execut_db_sql(sql)
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
                    self.assertIn('2min', result)

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
            start = datetime.datetime.now()
            result = self.commshpri.execut_db_sql(sql)
            end = datetime.datetime.now()
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)
            execute_time = (end - start).seconds
            self.log.info(execute_time)
            self.assertLessEqual(120, int(execute_time))

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 1 == i:
                    if int(execute_time) > 180:
                        self.assertIn('5 | test', result)
                    else:
                        self.assertIn(self.constant.NOT_EXIST, result)
                else:
                    self.assertIn('5 | test', result)

            self.log.info('-------等待2min，查询备机------------')
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

            self.log.info('----设置备节点recovery_min_apply_delay=30s----')
            sql = f"alter SYSTEM set " \
                f"recovery_min_apply_delay to '30s' "
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
            self.assertLessEqual(30, int(execute_time))

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 0 == i:
                    self.assertIn('5 | test', result)
                    self.assertIn('4 | test', result)
                else:
                    self.assertIn('5 | test', result)
                    if int(execute_time) > 60:
                        self.assertIn('4 | test', result)
                    else:
                        self.assertNotIn('4 | test', result)
            time.sleep(60)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('5 | test', result)
                self.assertIn('4 | test', result)

            self.log.info('--------设置synchronous_commit=off-------')
            result = self.commshpri.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                'synchronous_commit=off')
            self.assertTrue(result)

            self.log.info('----------重启数据库-----------')
            result = self.commshpri.stop_db_cluster()
            self.assertTrue(result)
            result = self.commshpri.start_db_cluster()
            self.assertTrue(result)

            self.log.info('--------删除数据-------')
            time.sleep(5)
            sql = f"delete from {self.tb_name} where i=5;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('DELETE', result)

            self.log.info('----------------查询备机----------------')
            time.sleep(5)
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('5 | test', result)
            time.sleep(30)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 0 == i:
                    self.assertNotIn('5 | test', result)
                else:
                    self.assertIn('5 | test', result)
            time.sleep(30)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertNotIn('5 | test', result)

            self.log.info('----设置备节点recovery_min_apply_delay=2min----')
            sql = f"alter SYSTEM set " \
                f"recovery_min_apply_delay to '2min' "
            result = self.comshsta[0].execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.alter_system_success_msg, result)

            self.log.info('---------删除数据----------')
            sql = f"delete from {self.tb_name};"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('DELETE', result)

            self.log.info('----------------查询备机----------------')
            time.sleep(5)
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('4 | test', result)
            time.sleep(60)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 1 == i:
                    self.assertNotIn('4 | test', result)
                else:
                    self.assertIn('4 | test', result)
            time.sleep(60)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertNotIn('4 | test', result)

            self.log.info('----级联备recovery_min_apply_delay=0----')
            sql = f"alter SYSTEM set " \
                f"recovery_min_apply_delay to '0' "
            result = self.comshsta[1].execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.alter_system_success_msg, result)

            self.log.info('----------插入数据---------')
            sql = f"insert into {self.tb_name} values (6,'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG, result)

            self.log.info('----------------查询备机----------------')
            time.sleep(5)
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 1 == i:
                    self.assertIn('6 | test', result)
                else:
                    self.assertNotIn('6 | test', result)
            time.sleep(120)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('6 | test', result)

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

        self.log.info("---Opengauss_Function_Recovery_Delay_Case0015 end--")
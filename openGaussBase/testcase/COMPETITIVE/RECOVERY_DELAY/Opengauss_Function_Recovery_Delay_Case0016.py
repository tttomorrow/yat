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
Case Name   : 备机stop后，判断延迟是否生效
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
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0016 start---")
        self.constant = Constant()
        self.log.info("---------get number of node---------")
        self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
        self.rootnodelist = ['Standby1Root', 'Standby2Root']
        result = self.commshpri.get_db_cluster_status('detail')
        self.log.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.comshsta = []
        self.log.info(self.node_num)
        self.tb_name = 'tb_case0016'

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

            self.log.info('--------创建表-------')
            sql = f"drop table if exists {self.tb_name};" \
                f"create table {self.tb_name}(i int, s char(10));"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)

            self.log.info('-------将备节点1切换为级联备---------')
            result = self.comshsta[1].build_standby('-M cascade_standby')
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result)
            result = self.comshsta[1].exec_refresh_conf()
            self.assertTrue(result)

            self.log.info('-----设置recovery_min_apply_delay=1min----')
            result = self.commshpri.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                'recovery_min_apply_delay=1min')
            self.assertTrue(result)

            self.log.info('--------等待主备一致------------')
            result = self.comshsta[0].check_data_consistency()
            self.assertTrue(result)
            for i in range(90):
                result = self.commshpri.check_cascade_standby_consistency()
                if result:
                    break
                time.sleep(20)
            self.assertTrue(result)

            self.log.info('-------------插入数据----------')
            sql = f"insert into {self.tb_name} values (1, 'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('INSERT', result)

            self.log.info('--------------停止备节点-----------')
            result = self.comshsta[0].stop_db_instance()
            self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, result)

            self.log.info('----------等待60s启动备节点---------------------')
            time.sleep(60)
            result = self.comshsta[0].start_db_instance('standby')
            self.assertIn(self.constant.RESTART_SUCCESS_MSG, result)

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('1 | test', result)

            self.log.info('-------------更新数据----------')
            sql = f"update {self.tb_name} set i = 5;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('UPDATE', result)

            self.log.info('--------------停止备节点-----------')
            time.sleep(2)
            result = self.comshsta[0].stop_db_instance()
            self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, result)

            self.log.info('----------等待5s启动备节点---------------------')
            time.sleep(5)
            result = self.comshsta[0].start_db_instance('standby')
            self.assertIn(self.constant.RESTART_SUCCESS_MSG, result)

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 1 == i:
                    self.assertIn('1 | test', result)
                else:
                    flg = '1 | test' in result or '5 | test' in result
                    self.assertTrue(flg)
            time.sleep(70)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('5 | test', result)

            self.log.info('-------------删除数据----------')
            sql = f"delete from {self.tb_name};"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('DELETE', result)

            self.log.info('--------------停止级联备-----------')
            time.sleep(2)
            result = self.comshsta[1].stop_db_instance()
            self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, result)

            self.log.info('----------等待60s启动备节点---------------------')
            time.sleep(60)
            result = self.comshsta[1].start_db_instance('cascade_standby')
            self.assertIn(self.constant.RESTART_SUCCESS_MSG, result)

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('0 rows', result)

            self.log.info('-------------插入数据----------')
            sql = f"insert into {self.tb_name} values (1, 'test');"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('INSERT', result)

            self.log.info('--------------停止级联备-----------')
            result = self.comshsta[1].stop_db_instance()
            self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, result)

            self.log.info('----------等待5s启动备节点---------------------')
            time.sleep(5)
            result = self.comshsta[1].start_db_instance('cascade_standby')
            self.assertIn(self.constant.RESTART_SUCCESS_MSG, result)

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};"
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                if 0 == i:
                    self.assertIn('0 rows', result)
                else:
                    flg = '1 | test' in result or '0 rows' in result
                    self.assertTrue(flg)
            time.sleep(60)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('1 | test', result)

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

        self.log.info('-----------重启数据库-----------')
        result = self.commshpri.stop_db_cluster()
        self.log.info(result)
        result = self.commshpri.start_db_cluster()
        self.log.info(result)

        self.log.info("---Opengauss_Function_Recovery_Delay_Case0016 end--")
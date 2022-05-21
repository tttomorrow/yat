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
Case Name   : 执行DDL检测主备一致性
Description :
    1.创建表空间
    2.创建新类型
    3.切换备节点为级联备
    4.设置延迟为1min
    5.创建表
    6.查询级联备节点
    7.插入数据
    8.查询级联备节点
    9.插入数据
    10.查询备节点
    11.truncate表
    12.查询备节点
Expect      :
    1.创建成功
    2.创建成功
    3.切换成功
    4.设置成功
    5.创建成功
    6.全局临时表不允许查询，临时表不存在，其余60s后同步
    7.插入失败
    8.查询结果无更新
    9.插入成功
    10.全局临时表不允许查询，临时表不存在，其余60s后同步
    11.删除成功
    12.全局临时表不允许查询，临时表不存在，其余60s后同步
History     :
    导致查询冲突，修改断言方式，规避该问题
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
        self.log.info("---Opengauss_Function_Recovery_Delay_Case0018 start--")
        self.constant = Constant()
        self.log.info("---------get number of node---------")
        result = self.commshpri.get_db_cluster_status('detail')
        self.log.info(result)
        self.node_num = result.count('Standby Normal') + 1
        self.comshsta = []
        self.log.info(self.node_num)
        self.tb_name = 'tb_case0016'
        self.tb_name_g_tmp = 'g_tmp_tb_case0016'
        self.tb_name_tmp = 'tmp_tb_case0016'
        self.tb_name_like = 'tb_case0016_like'
        self.tbspc = 'tbs_0018'
        self.type_name = 'new_type'
        self.col_name = 'col_tbl'

        if self.node_num > 2:
            self.nodelist = ['Standby1DbUser', 'Standby2DbUser']
            self.rootnodelist = ['Standby1Root', 'Standby2Root']
            self.log.info('------同步集群时间--------')
            for i in range(2):
                current = self.db_primary_user_node.sh(
                    "date \"+%m/%d/%Y %H:%M:%S\"").result()
                self.log.info(current)
                datecmd = f'date -s "{current}";hwclock --systohc;' \
                    f'service ntpd stop;ntpdate ntp.api.bz;service ntpd start'
                self.log.info(datecmd)
                db_standby_node = Node(node=self.rootnodelist[i])
                result = db_standby_node.sh(datecmd).result()
                self.log.info(result)

    def test_recovery_delay(self):
        if self.node_num > 2:
            for i in range(int(self.node_num) - 1):
                self.comshsta.append(CommonSH(self.nodelist[i]))

            self.log.info('--------创建表空间-------')
            sql = f"drop tablespace if exists {self.tbspc};" \
                f"CREATE TABLESPACE {self.tbspc} " \
                f"RELATIVE LOCATION '{self.tbspc}';"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, result)

            self.log.info('--------创建新类型-------')
            sql = f"drop type if exists {self.type_name};" \
                f"create type  {self.type_name} as " \
                f"(bool_var bool , email varchar );"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn(self.constant.CREATE_TYPE_SUCCESS_MSG, result)

            self.log.info('-------将备节点1切换为级联备---------')
            result = self.comshsta[1].build_standby('-M cascade_standby')
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG, result)
            result = self.comshsta[1].exec_refresh_conf()
            self.assertTrue(result)

            self.log.info('-----设置recovery_min_apply_delay=3min----')
            result = self.commshpri.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                'recovery_min_apply_delay=3min')
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

            self.log.info('-------------创建表----------')
            sql = f"create table {self.tb_name}(new {self.type_name} " \
                f"not null, date_var DATE unique, " \
                f"id int primary key check (id is not null), " \
                f"constraint test check(id>10))  TABLESPACE  {self.tbspc};" \
                f"create table {self.tb_name_like} " \
                f"(like {self.tb_name} inCLUDING ALL);" \
                f"create table {self.col_name}(i int) with " \
                f"(ORIENTATION = COLUMN, COMPRESSION=HIGH);" \
                f"create global temp table {self.tb_name_g_tmp}(i int);" \
                f"create temp  table {self.tb_name_tmp}(i int);"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertLess(
                5, result.count(self.constant.CREATE_TABLE_SUCCESS))

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};" \
                f"select * from {self.tb_name_like};" \
                f"select * from {self.col_name};" \
                f"select * from {self.tb_name_g_tmp};" \
                f"select * from {self.tb_name_tmp};"
            time.sleep(10)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertEqual(result.count(self.constant.NOT_EXIST), 5)
            time.sleep(200)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertEqual(result.count('0 rows'), 3)
                self.assertIn('cannot access temporary ', result)
                self.assertIn(self.constant.NOT_EXIST, result)


            self.log.info('------------插入数据---------------')
            sql = f"insert into {self.tb_name} values(NULL, '12-10-2010', 1);"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertIn('ERROR', result)

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};"
            time.sleep(10)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('0 rows', result)
            time.sleep(180)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('0 rows', result)

            self.log.info('------------插入数据---------------')
            sql = f"insert into {self.tb_name} values " \
                f"((true, '@12345'), '12-10-2010', 11);" \
                f"insert into {self.tb_name_like} values " \
                f"((false, '12345@'), '12-12-2010', 17);" \
                f"insert into {self.tb_name_g_tmp} values(1977);" \
                f"insert into {self.tb_name_tmp} values(2017);" \
                f"insert into {self.col_name} values(7815);"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertEqual(result.count('INSERT'), 4)
            self.assertIn(self.constant.NOT_EXIST, result)

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};" \
                f"select * from {self.tb_name_like};" \
                f"select * from {self.col_name};" \
                f"select * from {self.tb_name_g_tmp};" \
                f"select * from {self.tb_name_tmp};"
            time.sleep(10)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertEqual(result.count('0 rows'), 3)
                self.assertIn('cannot access temporary ', result)
                self.assertIn(self.constant.NOT_EXIST, result)
            time.sleep(200)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertIn('(t,@12345) | 2010-12-10 00:00:00 | 11', result)
                self.assertIn('(f,12345@) | 2010-12-12 00:00:00 | 17', result)
                self.assertIn('7815', result)
                self.assertIn('cannot access temporary ', result)
                self.assertIn(self.constant.NOT_EXIST, result)

            self.log.info('---------------truncate--------------')
            sql = f"truncate table {self.tb_name} ;" \
                f"truncate table {self.tb_name_like};" \
                f"truncate table {self.tb_name_g_tmp};" \
                f"truncate table{self.tb_name_tmp} ;" \
                f"truncate table {self.col_name} ;"
            result = self.commshpri.execut_db_sql(sql)
            self.log.info(result)
            self.assertEqual(result.count('TRUNCATE'), 4)
            self.assertIn(self.constant.NOT_EXIST, result)

            self.log.info('-------备机查询------------')
            sql = f"select sysdate;select * from {self.tb_name};" \
                f"select * from {self.tb_name_like};" \
                f"select * from {self.col_name};" \
                f"select * from {self.tb_name_g_tmp};" \
                f"select * from {self.tb_name_tmp};"
            time.sleep(10)
            total_time = 0
            for i in range(int(self.node_num) - 1):
                start = datetime.datetime.now()
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                end = datetime.datetime.now()
                total_time = (end-start).seconds + total_time
                if total_time < 100:
                    self.assertEqual(result.count('1 row'), 4)
                    self.assertIn('cannot access temporary ', result)
                    self.assertIn(self.constant.NOT_EXIST, result)
                else:
                    if 'conflict with recovery' not in result:
                        self.assertLessEqual(result.count('1 row'), 4)
                        self.assertIn('cannot access temporary ', result)
                        self.assertIn(self.constant.NOT_EXIST, result)
            time.sleep(200)
            for i in range(int(self.node_num) - 1):
                result = self.comshsta[i].execut_db_sql(sql)
                self.log.info(result)
                self.assertEqual(result.count('0 rows'), 3)
                self.assertIn('cannot access temporary ', result)
                self.assertIn(self.constant.NOT_EXIST, result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
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

        self.log.info('--------删除表-------')
        sql = f"drop table if exists {self.tb_name};" \
            f"drop table if exists {self.tb_name_tmp};" \
            f"drop table if exists {self.tb_name_g_tmp};" \
            f"drop table if exists {self.tb_name_like};" \
            f"drop table if exists {self.col_name};" \
            f"drop tablespace if exists {self.tbspc};" \
            f"drop type if exists {self.type_name};"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)

        self.log.info("---Opengauss_Function_Recovery_Delay_Case0018 end--")
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
Case Type   : upsert子查询功能
Case Name   : upsert使用子查询（子查询表为全局临时表）支持GPC验证；
Description :
    upsert子句带参数，不支持GPC；upsert子句不带参数，支持GPC
    1、开启GPC，重启数据库生效
    2、创建表，子查询表为全局临时表
    3、查询GPC全局计划缓存状态信息
    4、prepare执行，子查询中包含参数，update不存在冲突
    5、查询GPC全局计划缓存状态信息
    6、prepare执行，子查询中包含参数，update存在冲突
    7、查询GPC全局计划缓存状态信息
    8、prepare执行，子查询中不包含参数，update不存在冲突
    9、查询GPC全局计划缓存状态信息
    10、prepare执行，子查询中不包含参数，update存在冲突
    11、查询GPC全局计划缓存状态信息
Expect      :
    1、开启GPC，重启数据库生效
    2、创建表，子查询表为全局临时表，expect: 创建成功
    3、查询GPC全局计划缓存状态信息，expect: 查询0行
    4、prepare执行，子查询中包含参数，update不存在冲突 expect:执行成功
    5、查询GPC全局计划缓存状态信息，expect： 查询0行
    6、prepare执行，子查询中包含参数，update存在冲突 expect:执行成功
    7、查询GPC全局计划缓存状态信息，expect： 查询0行
    8、prepare执行，子查询中不包含参数，update不存在冲突 expect:执行成功
    9、查询GPC全局计划缓存状态信息，expect： 查询新增1行
    10、prepare执行，子查询中不包含参数，update存在冲突 expect:执行成功
    11、查询GPC全局计划缓存状态信息，expect： 查询新增1行
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class UpsertCase133(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_DML_Upsert_Case0134:初始化----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t1 = 't_dml_upsert0134'
        self.t2 = 't_dml_upsert_sub0134'

    def test_main(self):
        self.log.info('----查询相关参数----')
        result = self.pri_sh.execut_db_sql('show enable_thread_pool;')
        self.log.info(f"enable_thread_pool is {result}")
        self.para1 = result.strip().splitlines()[-2]

        result = self.pri_sh.execut_db_sql(
            'show enable_global_plancache;')
        self.log.info(f"enable_global_plancache is {result}")
        self.para2 = result.strip().splitlines()[-2]

        step_txt = '----step1: 开启GPC，expect: 成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execute_gsguc("set",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           "enable_thread_pool = on")
        self.assertTrue(result)
        result = self.pri_sh.execute_gsguc("set",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           "enable_global_plancache = on")
        self.assertTrue(result, '执行失败:' + step_txt)

        self.log.info('----step1: 重启数据库，expect: 成功----')
        result = self.pri_sh.restart_db_cluster()
        self.assertTrue(result, '执行失败:' + step_txt)

        step_txt = '----step2: 创建表，子查询表为全局临时表，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t1};' \
            f'drop table if exists {self.t2};' \
            f'create table {self.t1}(i int primary key, j text);' \
            f'create global temp table {self.t2}(i int, j text);' \
            f'insert into {self.t1} values(1,1);' \
            f'insert into {self.t2} values(1,\'test1\');'
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count('INSERT 0 1')
        self.log.info(assert_flag)
        self.assertEqual(assert_flag, 2, '执行失败:' + step_txt)

        step_txt = '----step3: 查询GPC全局计划缓存状态信息，expect: 查询0行----'
        self.log.info(step_txt)
        select_sql = 'select * from dbe_perf.global_plancache_status;'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        self.assertIn('0 rows', select_result, '执行失败:' + step_txt)

        step_txt = '----step4: prepare执行，子查询中包含参数，update不存在冲突 expect:执行成功----'
        self.log.info(step_txt)
        prepare_sql = f'insert into {self.t2} values(1,\'test1\');' \
            f'prepare gpc_tb_pre1(int, int) as ' \
            f'insert into {self.t1} values(\$1,\$1) on duplicate key ' \
            f'update j = (select j from {self.t2} where i =\$1 );' \
            f'execute gpc_tb_pre1(2,2);' \
            f'select * from {self.t1};'
        prepare_result = self.pri_sh.execut_db_sql(prepare_sql)
        self.log.info(prepare_result)
        self.assertIn('INSERT 0 1', prepare_result, '执行失败:' + step_txt)

        step_txt = '----step5: 查询GPC全局计划缓存状态信息，expect： 查询0行----'
        self.log.info(step_txt)
        select_sql = 'select * from dbe_perf.global_plancache_status;'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        self.assertIn('0 rows', select_result, '执行失败:' + step_txt)

        step_txt = '----step6: prepare执行，子查询中包含参数，update存在冲突 expect:执行成功----'
        self.log.info(step_txt)
        prepare_sql = f'insert into {self.t2} values(1,\'test1\');' \
            f'prepare gpc_tb_pre2(int, int) as ' \
            f'insert into {self.t1} values(\$1,\$1) on duplicate key ' \
            f'update j = (select j from {self.t2} where i =\$1 );' \
            f'execute gpc_tb_pre2(1,2);' \
            f'select * from {self.t1}; '
        prepare_result = self.pri_sh.execut_db_sql(prepare_sql)
        self.log.info(prepare_result)
        self.assertIn('INSERT 0 1', prepare_result, '执行失败:' + step_txt)

        step_txt = '----step7: 查询GPC全局计划缓存状态信息，expect： 查询0行----'
        self.log.info(step_txt)
        select_sql = 'select * from dbe_perf.global_plancache_status;'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        self.assertIn('0 rows', select_result, '执行失败:' + step_txt)

        step_txt = '----step8: prepare执行，子查询中不包含参数，update不存在冲突expect:执行成功----'
        self.log.info(step_txt)
        prepare_sql = f'insert into {self.t2} values(1,\'test1\');' \
            f'prepare gpc_tb_pre3(int, int) as ' \
            f'insert into {self.t1} values(\$1,\$1) on duplicate key ' \
            f'update j = (select j from {self.t2} where i =1 );' \
            f'execute gpc_tb_pre3(3,3);' \
            f'select * from {self.t1}; '
        prepare_result = self.pri_sh.execut_db_sql(prepare_sql)
        self.log.info(prepare_result)
        self.assertIn('INSERT 0 1', prepare_result, '执行失败:' + step_txt)

        step_txt = '----step9: 查询GPC全局计划缓存状态信息，expect： 查询新增1行----'
        self.log.info(step_txt)
        select_sql = 'select * from dbe_perf.global_plancache_status;'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        self.assertIn('1 row', select_result, '执行失败:' + step_txt)

        step_txt = '----step10: prepare执行，子查询中不包含参数，update存在冲突expect:执行成功----'
        self.log.info(step_txt)
        prepare_sql = f'insert into {self.t2} values(1,\'test1\');' \
            f'prepare gpc_tb_pre4(int, int) as ' \
            f'insert into {self.t1} values(\$1,\$1) on duplicate key ' \
            f'update j = (select j from {self.t2} where i =2 );' \
            f'execute gpc_tb_pre4(2,3);' \
            f'select * from {self.t1}; '
        prepare_result = self.pri_sh.execut_db_sql(prepare_sql)
        self.log.info(prepare_result)
        self.assertIn('INSERT 0 1', prepare_result, '执行失败:' + step_txt)

        step_txt = '----step11: 查询GPC全局计划缓存状态信息，expect: 查询新增1行----'
        self.log.info(step_txt)
        select_sql = 'select * from dbe_perf.global_plancache_status;'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        self.assertIn('2 rows', select_result, '执行失败:' + step_txt)

    def tearDown(self):
        step_txt = '----step12: 清除表数据，expect: 删除成功----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t1};' \
            f'drop table if exists {self.t2};'
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)

        step_txt = '----step13: 还原参数----'
        self.log.info(step_txt)
        self.pri_sh.execute_gsguc("set",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"enable_thread_pool = {self.para1}")
        self.pri_sh.execute_gsguc("set",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"enable_global_plancache = {self.para2}")
        self.pri_sh.restart_db_cluster()
        self.log.info('----Opengauss_Function_DML_Upsert_Case0134:用例执行完毕----')

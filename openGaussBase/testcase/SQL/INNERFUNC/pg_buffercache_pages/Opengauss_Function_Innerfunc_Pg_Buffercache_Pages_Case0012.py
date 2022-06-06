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
Case Type   : pg_buffercache_pages验证
Case Name   : pg_buffercache_pages函数，自动checkpoint，表对象isdirty字段验证
Description :
    1、设置辅助参数log_checkpoints参数值为on
      设置辅助参数log_statement参数值为all
      设置辅助参数log_min_duration_statement参数值为0
      设置辅助参数log_duration参数值为on
      设置enable_incremental_checkpoint参数值为off
      设置checkpoint_timeout参数值为30s
    2、gsql连接数据库，创建表
    3、初始查询表的缓存信息
    4、表中插入一定量数据
    5、再次查询表的缓存信息
    6、等待checkpoint_timeout时间，再次查询表的缓存信息
    7、环境清理
Expect      :
    1、参数值修改成功
    2、gsql连接数据库，创建表成功
    3、初始查询表的缓存信息，为空（查询出的缓存记录为0行）;
    4、表中插入一定量数据成功
    5、再次查询表的缓存信息，isdirty字段为t
    6、等待checkpoint_timeout时间，再次查询表的缓存信息，isdirty字段为f
    7、环境清理成功
History     :
        log_min_duration_statement参数值修改，方便定位用例执行失败原因
        修改参数设置替换冗余代码、修改step5断言逻辑
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class PgBuffercachePagesCase0012(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----- {os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t_name1 = 't_pg_buffercache_pages_case0012_1'

    def test_main(self):
        step_txt = '----step1:修改参数值，expect: 参数值修改成功----'
        self.log.info(step_txt)
        self.param_dict = {'log_checkpoints': '',
                           'log_statement': '',
                           'log_duration': '',
                           'log_min_duration_statement': '',
                           'enable_incremental_checkpoint': '',
                           'checkpoint_timeout': ''}
        self.log.info('---------------获取并打印参数初始值------------------')
        for key in self.param_dict:
            cmd = f'show {key};'
            self.log.info(cmd)
            cmd_result = self.pri_sh.execut_db_sql(cmd)
            self.log.info(cmd_result)
            cmd_result_value = cmd_result.strip().splitlines()[-2].strip()
            self.param_dict[key] = cmd_result_value
        self.change_pram_list = ['on', 'all', 'on', '0', 'off', '30s']
        self.log.info('---------------开始修改参数值------------------')
        for i in range(0, 6):
            self.pri_sh.execute_gsguc("set", self.constant.GSGUC_SUCCESS_MSG,
                            f"{[j for j in self.param_dict.keys()][i]}"
                            f"={self.change_pram_list[i]}")
        self.log.info('--------------------重启数据库---------------------')
        restart_flag1 = self.pri_sh.restart_db_cluster()
        self.assertTrue(restart_flag1, '重启数据库失败')
        cmd = f'select pg_sleep(60);'
        self.log.info(cmd)
        self.pri_sh.execut_db_sql(cmd)

        self.log.info('---------------检查参数是否修改成功------------------')
        self.check_pram_list = []
        for key in self.param_dict:
            cmd = f'show {key};'
            self.log.info(cmd)
            cmd_result = self.pri_sh.execut_db_sql(cmd)
            self.log.info(cmd_result)
            cmd_result_value = cmd_result.strip().splitlines()[-2].strip()
            self.check_pram_list.append(cmd_result_value)
        for i in range(0, 6):
            self.assertEqual(self.change_pram_list[i],
                             self.check_pram_list[i],
                f"参数{[j for j in self.param_dict.keys()][i]}修改失败！"
                    + step_txt)

        step_txt = '----step2:创建一张表，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.t_name1};' \
            f'create table {self.t_name1}(id int,content text);'
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      '执行失败:' + step_txt)

        step_txt = '----step3: 初始查询表的缓存信息，expect: 为0行----'
        self.log.info(step_txt)
        select_sql = f"select count(*) from pg_buffercache_pages() where " \
            f"relfilenode in (select relfilenode from pg_class " \
            f"where relname='{self.t_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_count1 = int(select_result.strip().splitlines()[-2])
        self.assertEqual(tmp_count1, 0, '执行失败：' + step_txt)

        step_txt = '----step4:表中插入一定量的数据，expect: 插入成功----'
        self.log.info(step_txt)
        insert_sql = f"insert into {self.t_name1} " \
            f"values(generate_series(1, 1000), 'testtext');"
        self.log.info(insert_sql)
        insert_result = self.pri_sh.execut_db_sql(insert_sql)
        self.log.info(insert_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_result,
                      '执行失败:' + step_txt)

        step_txt = f'----step5: 再次查询表的缓存信息，expect: isdirty字段为t'
        self.log.info(step_txt)
        select_sql = f"select * from pg_buffercache_pages() where " \
            f"relfilenode in (select relfilenode from pg_class " \
            f"where relname='{self.t_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        select_sql = f"select distinct isdirty as chk " \
            f"from pg_buffercache_pages() " \
            f"where relfilenode in (select relfilenode from pg_class " \
            f"where relname='{self.t_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        self.assertIn('t', select_result, '执行失败：' + step_txt)

        step_txt = f'----step6: 等待checkpoint_timeout时间，再次查询表的缓存信息' \
            f'，expect: isdirty字段为f'
        checkpoint_sql = f'select pg_sleep(40);'
        self.log.info(checkpoint_sql)
        checkpoint_sql_result = self.pri_sh.execut_db_sql(checkpoint_sql)
        self.log.info(checkpoint_sql_result)
        tmp_count1 = checkpoint_sql_result.strip().splitlines()[-2].strip()
        self.assertEqual(tmp_count1, '', '执行失败：' + step_txt)
        select_sql = f"select distinct isdirty from pg_buffercache_pages() " \
            f"where relfilenode in (select relfilenode from pg_class " \
            f"where relname='{self.t_name1}');"
        self.log.info(select_sql)
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        isdirty_flag = select_result.strip().splitlines()[-2].strip()
        self.assertEqual(isdirty_flag, 'f', '执行失败：' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step7: 环境清理，expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f'drop table if exists {self.t_name1};'
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.log.info('---------------还原参数的初始值------------------')
        for i in range(0, 6):
            self.pri_sh.execute_gsguc("set", self.constant.GSGUC_SUCCESS_MSG,
                        f"{[j for j in self.param_dict.keys()][i]}"
                        f"={[j for j in self.param_dict.values()][i]}")
        self.log.info('--------------------重启数据库---------------------')
        restart_flag = self.pri_sh.restart_db_cluster()
        self.log.info(restart_flag)
        self.log.info('---------------获取并打印参数还原后的值----------------')
        self.check_pram_list2 = []
        for key in self.param_dict:
            cmd = f'show {key};'
            self.log.info(cmd)
            cmd_result = self.pri_sh.execut_db_sql(cmd)
            self.log.info(cmd_result)
            cmd_result_value = cmd_result.strip().splitlines()[-2].strip()
            self.check_pram_list2.append(cmd_result_value)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_result,
                      '表删除失败:' + step_txt)
        self.assertTrue(restart_flag, '重启数据库失败')
        for i in range(0, 6):
            self.assertEqual([j for j in self.param_dict.values()][i],
                             self.check_pram_list2[i],
                f"参数{[j for j in self.param_dict.keys()][i]}还原失败！"
                             + step_txt)
        self.log.info(f'----- {os.path.basename(__file__)} end-----')

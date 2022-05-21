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
Case Type   : 功能测试-表空间
Case Name   : 表空间与数据库应用不在同一磁盘，修改空间限额-表空间实际占用空间与修改后限额大小关系验证
Description :
    1、创建tablespace设置限额3M，表空间绝对路径与dn不在同一磁盘
    2、循环插入一定量数据，小于3M
    3、查询表空间实际占用空间，修改表空间限额小于实际占用空间
    4、继续插入数据至表空间满
    5、进行表空间内对象操作（建立索引）
    6、修改表空间限额，大于实际占用空间
    7、继续插入数据
    8、新建索引
Expect      :
    1、创建tablespace设置限额3M，表空间绝对路径与dn不在同一磁盘; 创建成功
    2、循环插入一定量数据，小于3M; 插入成功
    3、查询表空间实际占用空间，修改表空间限额小于实际占用空间; 修改成功
    4、继续插入数据至表空间满; 无法插入
    5、进行表空间内对象操作（建立索引）; 操作失败
    6、修改表空间限额，大于实际占用空间； 修改成功
    7、继续插入数据； 插入成功
    8、进行表空间内对象操作（建立索引）； 操作成功
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

pri_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(pri_sh.get_node_num() < 3, '非1+2环境不执行')
class Tablespace(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_root = Node(node='PrimaryRoot')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.sta1_dbuser = Node(node='Standby1DbUser')
        self.sta2_dbuser = Node(node='Standby2DbUser')
        self.constant = Constant()
        self.tbspc_name1 = 'tsp_tbspc0040'
        self.tbspc_location1 = os.path.join(macro.DB_BACKUP_PATH, 'tbspc0040')
        self.maxsize = 3
        self.max_num = 10000
        self.loop_num1 = 5
        self.loop_num2 = 2000
        self.table_name = 't_tbspc0040'
        self.index_name = 'idx_tbspc0040'
        self.create_sql = f'drop table if exists {self.table_name};' \
            f'create table {self.table_name}(id int) ' \
            f'tablespace {self.tbspc_name1};'
        self.insert_sql = f'''begin 
            for i in 1..{self.max_num} loop
            insert into {self.table_name} values(i);
            end loop;
            end;'''
        self.insert_one_sql = f'insert into {self.table_name} values(1);'
        self.create_index_sql = f'create index {self.index_name} on ' \
            f'{self.table_name}(id) tablespace {self.tbspc_name1};'
        self.err_flag = f'ERROR:  Insufficient storage space for ' \
            f'tablespace "{self.tbspc_name1}"'

    def test_main(self):
        step_txt = '----step1:创建tablespace设置限额3M，表空间绝对路径与dn不在同一磁盘; ' \
                   'expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"location '{self.tbspc_location1}' " \
            f"maxsize '{self.maxsize}M';"
        create_result = pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置限额大小--')
        check_max = f'select spcmaxsize from pg_tablespace where ' \
            f'spcname = \'{self.tbspc_name1}\';'
        size = pri_sh.execut_db_sql(check_max).splitlines()[-2]
        self.log.info(size)
        self.assertIn(str(self.maxsize * 1024), size, "执行失败" + step_txt)

        step_txt = '----step2:循环插入一定量数据，小于3M; expect:插入成功----'
        self.log.info(step_txt)
        self.log.info('--在tablespace上创建表--')
        create_result = pri_sh.execut_db_sql(self.create_sql)
        self.log.info(create_result)
        self.log.info('--在tablespace上创建的表循环插入数据--')
        for i in range(self.loop_num1):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = pri_sh.execut_db_sql(self.insert_sql)
            self.log.info(insert_result)
            self.assertIn(self.constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                          insert_result, "执行失败" + step_txt)

        step_txt = '----step3:查询表空间实际占用空间，修改表空间限额小于实际占用空间; expect:修改成功----'
        self.log.info(step_txt)
        check_rel = f"select pg_tablespace_size('{self.tbspc_name1}');"
        size0 = pri_sh.execut_db_sql(check_rel).splitlines()[-2].strip()
        self.log.info(size0)
        self.log.info('--修改表空间限额小于实际占用空间--')
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"resize maxsize '{int(int(size0) / 2 / 1024)} K';"
        alter_result = pri_sh.execut_db_sql(alter_sql)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置限额大小--')
        size = pri_sh.execut_db_sql(check_max).splitlines()[-2]
        self.log.info(size)
        self.assertIn(str(int(int(size.split()[0]) / 2 / 1024)), size,
                      "执行失败" + step_txt)

        step_txt = '----step4:继续插入数据至表空间满; expect:无法插入----'
        self.log.info(step_txt)
        self.log.info('--在tablespace上创建的表循环插入数据--')
        for i in range(self.loop_num2):
            insert_result = pri_sh.execut_db_sql(self.insert_one_sql)
            if self.err_flag in insert_result:
                self.log.info('循环第 ' + str(i) + '次')
                self.log.info(insert_result)
                break
        self.log.info('--查看表空间大小--')
        size = pri_sh.execut_db_sql(check_rel).splitlines()[-2].strip()
        self.log.info(size)
        self.assertIn(size0, size, "执行失败" + step_txt)

        step_txt = '----step5:进行表空间内对象操作（建立索引）; expect:操作失败----'
        self.log.info(step_txt)
        create_index = pri_sh.execut_db_sql(self.create_index_sql)
        self.log.info(create_index)
        self.assertIn(self.err_flag, create_index, "执行失败" + step_txt)

        step_txt = '----step6:修改表空间限额，大于实际占用空间； expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name1} " \
            f"resize maxsize '{self.maxsize * 2}M';"
        alter_result = pri_sh.execut_db_sql(alter_sql)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置限额大小--')
        size = pri_sh.execut_db_sql(check_max).splitlines()[-2]
        self.log.info(size)
        self.assertIn(str(self.maxsize * 2 * 1024), size, "执行失败" + step_txt)

        step_txt = '----step7:继续插入数据； expect:插入成功----'
        self.log.info(step_txt)
        for i in range(self.loop_num1):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = pri_sh.execut_db_sql(self.insert_sql)
            self.log.info(insert_result)
            self.assertIn(self.constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                          insert_result, "执行失败" + step_txt)

        step_txt = '----step8:进行表空间内对象操作（建立索引）； expect:操作成功----'
        self.log.info(step_txt)
        create_index = pri_sh.execut_db_sql(self.create_index_sql)
        self.log.info(create_index)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, create_index,
                      "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop table if exists {self.table_name};" \
            f"drop tablespace if exists {self.tbspc_name1}; "
        clean_result = pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)
        step2_txt = '----删除表空间路径; expect:成功----'
        self.log.info(step2_txt)
        del_cmd = f"rm -rf {self.tbspc_location1}; " \
            f"if [ -d {self.tbspc_location1} ]; then echo 'exists'; " \
            f"else echo 'not exists'; fi;"
        self.log.info(del_cmd)
        del_result1 = self.pri_dbuser.sh(del_cmd).result()
        del_result2 = self.sta1_dbuser.sh(del_cmd).result()
        del_result3 = self.sta2_dbuser.sh(del_cmd).result()
        self.log.info(del_result1)
        self.log.info(del_result2)
        self.log.info(del_result3)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, clean_result,
                      "执行失败" + step1_txt)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, clean_result,
                      "执行失败" + step1_txt)
        self.assertEqual(1, del_result1.count('not exists'),
                         "执行失败" + step1_txt)
        self.assertEqual(1, del_result2.count('not exists'),
                         "执行失败" + step1_txt)
        self.assertEqual(1, del_result3.count('not exists'),
                         "执行失败" + step1_txt)

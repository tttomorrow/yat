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
Case Name   : 存在存量数据的表变更表空间--实际表文件所占空间大于变更后的表空间限额
Description :
    1、创建tablespace1指定相对路径为location1;
    2、在tablespace1上创建表;
    3、查询表文件实际路径及占用空间;
    4、在tablespace1上创建的表循环插入数据;
    5、查询表文件实际路径及占用空间;
    6、创建tablespace2指定相对路径为location2,限额小于表实际占用空间;
    7、变更表的表空间为tablespace2;
    8、查询表对应的物理位置表数据是否变更;
    9、继续往表循环插入数据;
    10、查询表文件实际路径及占用空间;
Expect      :
    1、创建tablespace1指定相对路径为location1; 创建成功
    2、在tablespace1上创建表; 创建成功
    3、查询表文件实际路径及占用空间; 表空间正确，占用大小为0
    4、在tablespace1上创建的表循环插入数据; 插入成功
    5、查询表文件实际路径及占用空间; 路径为tablespace1，表文件大小大于0
    6、创建tablespace2指定相对路径为location2,限额小于表实际占用空间;创建成功
    7、变更表的表空间为tablespace2; 变更失败
    8、查询表对应的物理位置表数据是否变更; 未进行变更
    9、继续往表循环插入数据; 插入成功
    10、查询表文件实际路径及占用空间; 路径为tablespace1，表文件大小增加
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tablespace(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.sh = CommonSH('PrimaryDbUser')
        self.pri_root = Node(node='PrimaryRoot')
        self.constant = Constant()
        self.tbspc_name1 = 'tsp_tbspc0035_1'
        self.tbspc_location1 = 'tbspc0035_1'
        self.tbspc_name2 = 'tsp_tbspc0035_2'
        self.tbspc_location2 = 'tbspc0035_2'

        self.max_num = 10000
        self.loop_num = 10
        self.table_name = 't_tbspc0035'
        self.create_sql = f'drop table if exists {self.table_name};' \
            f'create table {self.table_name}(id int) ' \
            f'tablespace {self.tbspc_name1};'
        self.insert_sql = f'''begin 
            for i in 1..{self.max_num} loop
            insert into {self.table_name} values(i);
            end loop;
            end;'''
        self.insert_one_sql = f'insert into {self.table_name} values(1);'
        self.create_index_sql = f'create index id_index on ' \
            f'{self.table_name}(id) tablespace {self.tbspc_name1};'
        self.count_sql = f"select count(*) from {self.table_name};"
        self.err_flag = 'ERROR:  Insufficient storage space for tablespace'

    def test_main(self):
        step_txt = '----step1:创建tablespace1指定相对路径为location1; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}' ;"
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result)

        step_txt = '----step2:在tablespace1上创建表; expect:创建成功----'
        self.log.info(step_txt)
        create_result = self.sh.execut_db_sql(self.create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:查询表文件实际路径及占用空间; expect:表空间正确，占用大小为0----'
        self.log.info(step_txt)
        check_result0 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_result0[0],
                      "执行失败" + step_txt)
        self.log.info('--表文件大小等于0--')
        self.assertEqual(int(check_result0[1]), 0, "执行失败" + step_txt)

        step_txt = '----step4:在tablespace1上创建的表循环插入数据; expect:插入成功----'
        self.log.info(step_txt)
        for i in range(self.loop_num):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = self.sh.execut_db_sql(self.insert_sql)
            self.log.info(insert_result)
            self.assertIn(self.constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                          insert_result, "执行失败" + step_txt)

        step_txt = '----step5:查询表文件实际路径及占用空间; ' \
                   'expect:路径为tablespace1，表文件大小大于0----'
        self.log.info(step_txt)
        check_result1 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_result1[0],
                      "执行失败" + step_txt)
        self.log.info('--插入数据，表文件所占的大小大于0--')
        self.assertGreater(int(check_result1[1]), 0, "执行失败" + step_txt)

        step_txt = '----step6:创建tablespace2指定相对路径为location2,限额小于表实际占用空间;' \
                   'expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name2}; " \
            f"create tablespace {self.tbspc_name2} " \
            f"relative location '{self.tbspc_location2}' " \
            f"maxsize '{int(int(check_result1[1]) / 1024 / 2)}k' ;"
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step7:变更表的表空间为tablespace2; expect:变更失败----'
        self.log.info(step_txt)
        alter_sql = f"alter table {self.table_name} " \
            f"set tablespace {self.tbspc_name2};"
        alter_result = self.sh.execut_db_sql(alter_sql)
        self.log.info(alter_result)
        self.assertIn(self.err_flag, alter_result, "执行失败" + step_txt)

        step_txt = '----step8:查询表对应的物理位置表数据是否变更; expect:未进行变更----'
        self.log.info(step_txt)
        check_result2 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_result2[0],
                      "执行失败" + step_txt)

        step_txt = '----step9:继续往表循环插入数据; expect:插入成功----'
        self.log.info(step_txt)
        for i in range(self.loop_num):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = self.sh.execut_db_sql(self.insert_sql)
            self.log.info(insert_result)
            self.assertIn(self.constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                          insert_result, "执行失败" + step_txt)

        step_txt = '----step10:查询表文件实际路径及占用空间; ' \
                   'expect:路径为tablespace1，表文件大小增加----'
        self.log.info(step_txt)
        check_result3 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_result3[0],
                      "执行失败" + step_txt)
        self.log.info('--插入数据，表文件大小增加--')
        self.assertGreater(int(check_result3[1]), int(check_result2[1]),
                           "执行失败" + step_txt)

    def check_ob_tbspc(self, object_name):
        """
        :param object_name: 数据库对象名称，例如表名、索引名
        :return: 数据库对象文件实际位置及占用空间
        """
        location_sql = f"select pg_relation_filepath(" \
            f"(select oid from pg_class where relname = '{object_name}')" \
            f"::regclass);"
        t_link = self.sh.execut_db_sql(location_sql).splitlines()[-2].strip()
        self.log.info('数据库对象文件链接路径：' + t_link)
        t_link_dir = os.path.dirname(
            os.path.join(macro.DB_INSTANCE_PATH, t_link))
        t_file_name = os.path.basename(t_link)
        ls_cmd = f'cd $(readlink -f {t_link_dir}) && ' \
            f'pwd && ' \
            f'ls -al . && ' \
            f'du -b {t_file_name}'
        self.log.info(ls_cmd)
        ls_result = self.pri_root.sh(ls_cmd).result()
        self.log.info(ls_result)
        self.log.info('--数据库对象文件所在的路径--')
        file_location = ls_result.splitlines()[0].strip()
        self.log.info(file_location)
        rel_file = os.path.join(file_location, t_file_name)
        self.log.info(rel_file)
        self.log.info('--数据库对象文件所占的大小--')
        file_size = ls_result.splitlines()[-1].split()[0].strip()
        self.log.info(file_size)
        return rel_file, file_size

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop table if exists {self.table_name};" \
            f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop tablespace if exists {self.tbspc_name2};"
        clean_result = self.sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(2, drop_tbspc, "执行失败" + step1_txt)

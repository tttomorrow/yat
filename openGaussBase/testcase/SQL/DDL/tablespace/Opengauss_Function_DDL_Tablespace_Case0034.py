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
Case Name   : 存在存量数据的表变更表空间--正常场景
Description :
    1、创建tablespace1指定相对路径为location1;
    创建tablespace2指定相对路径为location2;
    创建tablespace3指定绝对路径为location3;
    2、在tablespace1上创建表;
    3、查询表文件实际路径及占用空间;
    4、在tablespace1上创建的表循环插入数据;
    5、查询表文件实际路径及占用空间;
    6、变更表的表空间为tablespace2;
    7、查询表文件实际路径及占用空间;
    8、查询表原物理位置下表数据是否清空;
    9、删除原表空间tablespace1;
    10、继续在变更为tablespace2的表循环插入数据;
    11、查询表文件实际路径及占用空间;
    12、变更表的表空间为绝对路径tablespace3;
    13、查询表文件实际路径及占用空间;
    14、查询表原物理位置下表数据是否清空;
    15、删除原表空间;
    16、继续在变更为tablespace3的表循环插入数据;
    17、查询表文件实际路径及占用空间;
Expect      :
    1、创建tablespace1指定相对路径为location1;
    创建tablespace2指定相对路径为location2;
    创建tablespace3指定绝对路径为location3; 创建成功
    2、在tablespace1上创建表; 创建成功
    3、查询表文件实际路径及占用空间; 路径为tablespace1，表文件大小等于0
    4、在tablespace1上创建的表循环插入数据; 插入成功
    5、查询表文件实际路径及占用空间; 路径为tablespace1，表文件大小大于0
    6、变更表的表空间为tablespace2; expect：变更成功
    7、查询表文件实际路径及占用空间; 路径为tablespace2，表文件大小等于步骤5查询结果
    8、查询表原物理位置下表数据是否清空; 原物理路径下表文件清零
    9、删除原表空间tablespace1; 删除成功
    10、继续在变更为tablespace2的表循环插入数据; 插入成功
    11、查询表文件实际路径及占用空间; 路径为tablespace2，表文件大小大于步骤7查询结果
    12、变更表的表空间为绝对路径tablespace3; 变更成功
    13、查询表文件实际路径及占用空间; 路径为tablespace3，表文件大小等于步骤11查询结果
    14、查询表原物理位置下表数据是否清空; 原物理路径下表文件清零
    15、删除原表空间; 删除成功
    16、继续在变更为tablespace3的表循环插入数据; 插入成功
    17、查询表文件实际路径及占用空间; 路径为tablespace3，表文件大小大于步骤13查询结果
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
        self.tbspc_name1 = 'tsp_tbspc0034_1'
        self.tbspc_location1 = 'tbspc0034_1'
        self.tbspc_name2 = 'tsp_tbspc0034_2'
        self.tbspc_location2 = 'tbspc0034_2'
        self.tbspc_name3 = 'tsp_tbspc0034_3'
        self.tbspc_location3 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'tbspc0034_3')

        self.max_num = 10000
        self.loop_num = 5
        self.table_name = 't_tbspc0034'
        self.create_sql = f'drop table if exists {self.table_name};' \
            f'create table {self.table_name}(id int) ' \
            f'tablespace {self.tbspc_name1};'
        self.insert_sql = f'''begin 
            for i in 1..{self.max_num} loop
            insert into {self.table_name} values(i);
            end loop;
            end;'''
        self.count_sql = f"select count(*) from {self.table_name};"

    def test_main(self):
        step_txt = '----step1:创建tablespace1指定相对路径为location1;' \
                   '创建tablespace2指定相对路径为location2;' \
                   '创建tablespace3指定绝对路径为location3; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}' ;" \
            f"drop tablespace if exists {self.tbspc_name2}; " \
            f"create tablespace {self.tbspc_name2} " \
            f"relative location '{self.tbspc_location2}';" \
            f"drop tablespace if exists {self.tbspc_name3}; " \
            f"create tablespace {self.tbspc_name3} " \
            f"location '{self.tbspc_location3}';"
        create_result = pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertEqual(3, create_result.count(
            self.constant.TABLESPCE_DROP_SUCCESS), "执行失败" + step_txt)

        step_txt = '----step2:在tablespace1上创建表; expect:创建成功----'
        self.log.info(step_txt)
        create_result = pri_sh.execut_db_sql(self.create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:查询表文件实际路径及占用空间; ' \
                   'expect:路径为tablespace1，表文件大小等于0----'
        self.log.info(step_txt)
        check_result0 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_result0[0],
                      "执行失败" + step_txt)
        self.log.info('--未插入数据时，表文件所占的大小为0--')
        self.assertEqual(int(check_result0[1]), 0, "执行失败" + step_txt)

        step_txt = '----step4:在tablespace1上创建的表循环插入数据; expect:插入成功----'
        self.log.info(step_txt)
        for i in range(self.loop_num):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = pri_sh.execut_db_sql(self.insert_sql)
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

        step_txt = '----step6:变更表的表空间为tablespace2; expect：变更成功----'
        self.log.info(step_txt)
        alter_sql = f"alter table {self.table_name} " \
            f"set tablespace {self.tbspc_name2};"
        alter_result = pri_sh.execut_db_sql(alter_sql)
        self.log.info(alter_result)
        self.assertIn(self.constant.ALTER_TABLE_MSG, alter_result,
                      "执行失败" + step_txt)

        step_txt = '----step7:查询表文件实际路径及占用空间; ' \
                   'expect:路径为tablespace2，表文件大小等于步骤5查询结果----'
        self.log.info(step_txt)
        check_result2 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace2相对路径--')
        self.assertIn(self.tbspc_location2, check_result2[0],
                      "执行失败" + step_txt)
        self.log.info('--表文件大小等于步骤5查询结果--')
        self.assertEqual(int(check_result2[1]), int(check_result1[1]),
                         "执行失败" + step_txt)

        step_txt = '----step8:查询表原物理位置下表数据是否清空; expect:原物理路径下表文件清零----'
        self.log.info(step_txt)
        ls_cmd = f'du -b {check_result1[0]}'
        ls_result = self.pri_root.sh(ls_cmd).result()
        self.log.info(ls_result)
        before_size = ls_result.splitlines()[-1].split()[0].strip()
        self.log.info(before_size)
        self.assertEqual(int(before_size), 0, "执行失败" + step_txt)

        step_txt = '----step9:删除原表空间tablespace1; expect:删除成功----'
        self.log.info(step_txt)
        drop_sql = f"drop tablespace {self.tbspc_name1} ;"
        drop_result = pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, drop_result,
                      "执行失败" + step_txt)

        step_txt = '----step10:继续在变更为tablespace2的表循环插入数据; expect:插入成功----'
        self.log.info(step_txt)
        for i in range(self.loop_num):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = pri_sh.execut_db_sql(self.insert_sql)
            self.log.info(insert_result)
            self.assertIn(self.constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                          insert_result, "执行失败" + step_txt)

        step_txt = '----step11:查询表文件实际路径及占用空间; ' \
                   'expect:路径为tablespace2，表文件大小大于步骤7查询结果----'
        self.log.info(step_txt)
        check_result3 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace2相对路径--')
        self.assertIn(self.tbspc_location2, check_result3[0],
                      "执行失败" + step_txt)
        self.log.info('--未插入数据时，表文件所占的空间大于0--')
        self.assertGreater(int(check_result3[1]), int(check_result2[1]),
                           "执行失败" + step_txt)

        step_txt = '----step12:变更表的表空间为绝对路径tablespace3; expect:变更成功----'
        self.log.info(step_txt)
        alter_sql = f"alter table {self.table_name} " \
            f"set tablespace {self.tbspc_name3};"
        alter_result = pri_sh.execut_db_sql(alter_sql)
        self.log.info(alter_result)
        self.assertIn(self.constant.ALTER_TABLE_MSG, alter_result,
                      "执行失败" + step_txt)

        step_txt = '----step13:查询表文件实际路径及占用空间; ' \
                   'expect:路径为tablespace3，表文件大小等于步骤11查询结果----'
        self.log.info(step_txt)
        check_result4 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace3相对路径--')
        self.assertIn(self.tbspc_location3, check_result4[0],
                      "执行失败" + step_txt)
        self.log.info('--表文件大小等于步骤11查询结果--')
        self.assertEqual(int(check_result3[1]), int(check_result4[1]),
                         "执行失败" + step_txt)

        step_txt = '----step14:查询表原物理位置下表数据是否清空; expect:原物理路径下表文件清零----'
        self.log.info(step_txt)
        ls_cmd = f'du -b {check_result3[0]}'
        ls_result = self.pri_root.sh(ls_cmd).result()
        self.log.info(ls_result)
        before_size = ls_result.splitlines()[-1].split()[0].strip()
        self.log.info(before_size)
        self.assertEqual(int(before_size), 0, "执行失败" + step_txt)

        step_txt = '----step15:删除原表空间; expect:删除成功----'
        self.log.info(step_txt)
        drop_sql = f"drop tablespace {self.tbspc_name2} ;"
        drop_result = pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, drop_result,
                      "执行失败" + step_txt)

        step_txt = '----step16:继续在变更为tablespace3的表循环插入数据; expect:插入成功----'
        self.log.info(step_txt)
        for i in range(self.loop_num):
            self.log.info('循环第 ' + str(i) + '次')
            insert_result = pri_sh.execut_db_sql(self.insert_sql)
            self.log.info(insert_result)
            self.assertIn(self.constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                          insert_result, "执行失败" + step_txt)

        step_txt = '----step17:查询表文件实际路径及占用空间; ' \
                   'expect:路径为tablespace3，表文件大小大于步骤13查询结果----'
        self.log.info(step_txt)
        check_result5 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace3相对路径--')
        self.assertIn(self.tbspc_location3, check_result5[0],
                      "执行失败" + step_txt)
        self.log.info('--表文件大小等于步骤13查询结果--')
        self.assertGreater(int(check_result5[1]), int(check_result4[1]),
                           "执行失败" + step_txt)

    def check_ob_tbspc(self, object_name):
        """
        :param object_name: 数据库对象名称，例如表名、索引名
        :return: 数据库对象文件实际位置及占用空间
        """
        location_sql = f"select pg_relation_filepath(" \
            f"(select oid from pg_class where relname = '{object_name}')" \
            f"::regclass);"
        t_link = pri_sh.execut_db_sql(location_sql).splitlines()[-2].strip()
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
            f"drop tablespace if exists {self.tbspc_name2};" \
            f"drop tablespace if exists {self.tbspc_name3};"
        clean_result = pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        step2_txt = '----删除表空间路径; expect:成功----'
        self.log.info(step2_txt)
        del_cmd = f"rm -rf {self.tbspc_location3}; " \
            f"if [ -d {self.tbspc_location3} ]; then echo 'exists'; " \
            f"else echo 'not exists'; fi;"
        self.log.info(del_cmd)
        del_result1 = self.pri_dbuser.sh(del_cmd).result()
        del_result2 = self.sta1_dbuser.sh(del_cmd).result()
        del_result3 = self.sta2_dbuser.sh(del_cmd).result()
        self.log.info(del_result1)
        self.log.info(del_result2)
        self.log.info(del_result3)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(3, drop_tbspc, "执行失败" + step1_txt)
        self.assertEqual(1, del_result1.count('not exists'),
                         "执行失败" + step1_txt)
        self.assertEqual(1, del_result2.count('not exists'),
                         "执行失败" + step1_txt)
        self.assertEqual(1, del_result3.count('not exists'),
                         "执行失败" + step1_txt)

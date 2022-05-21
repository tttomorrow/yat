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
Case Name   : 索引变更表空间，使表与索引不在一个表空间，变更表空间后索引功能正常
Description :
    1、创建tablespace1指定相对路径为location1;创建tablespace2指定相对路径为location2
    2、在tablespace1上创建表及索引;
    3、在tablespace1上创建的表插入数据;
    4、查询表对应的表空间及表文件物理位置;
    5、查询索引对应的表空间及索引文件物理位置;
    6、查询数据;
    7、变更索引的表空间为tablespace2;
    8、在tablespace1上创建的表插入数据;
    9、查询表对应的表空间及表文件物理位置;
    10、查询索引对应的表空间及索引文件物理位置;
    11、查询数据;
Expect      :
    1、创建tablespace1指定相对路径为location1;创建tablespace2指定相对路径为location2 创建成功
    2、在tablespace1上创建表及索引; 创建成功
    3、在tablespace1上创建的表插入数据; 插入成功
    4、查询表对应的表空间及表文件物理位置; 查询结果正确
    5、查询索引对应的表空间及索引文件物理位置; 查询结果正确
    6、查询数据; 正常使用索引
    7、变更索引的表空间为tablespace2; 变更成功
    8、在tablespace1上创建的表插入数据; 插入成功
    9、查询表对应的表空间及表文件物理位置; 查询结果不变
    10、查询索引对应的表空间及索引文件物理位置; 表空间变更
    11、查询数据; 正常使用索引
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
        self.tbspc_name1 = 'tsp_tbspc0036_1'
        self.tbspc_location1 = 'tbspc0036_1'
        self.tbspc_name2 = 'tsp_tbspc0036_2'
        self.tbspc_location2 = 'tbspc0036_2'
        self.table_name = 't_tbspc0036'
        self.index_name = 'idx_tbspc0036'
        self.create_sql = f"drop table if exists {self.table_name};" \
            f"create table {self.table_name} (id int,name varchar(100)) " \
            f"tablespace {self.tbspc_name1};" \
            f"create index {self.index_name} on {self.table_name}(id) " \
            f"tablespace {self.tbspc_name1};"
        self.insert_sql = f"insert into {self.table_name} " \
            f"select generate_series(1, 100000)," \
            f"'name-'||generate_series(1, 100000);" \
            f"analyze {self.table_name};"
        self.select_sql = f"set enable_indexscan=on;" \
            f"set enable_bitmapscan=off;" \
            f"explain select * from {self.table_name} " \
            f"where id=80000;"

    def test_main(self):
        step_txt = '----step1:创建tablespace1指定相对路径为location1;' \
                   '创建tablespace2指定相对路径为location2 expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}' ;" \
            f"drop tablespace if exists {self.tbspc_name2}; " \
            f"create tablespace {self.tbspc_name2} " \
            f"relative location '{self.tbspc_location2}' ;"
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.TABLESPCE_CREATE_SUCCESS)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)
        self.log.info('--查询tablespace1 oid--')
        select_sql = f"select oid from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        tbspc1_oid = self.sh.execut_db_sql(select_sql).splitlines()[
            -2].strip()
        self.log.info(tbspc1_oid)
        self.log.info('--查询tablespace2 oid--')
        select_sql = f"select oid from pg_tablespace where " \
            f"spcname = '{self.tbspc_name2}';"
        tbspc2_oid = self.sh.execut_db_sql(select_sql).splitlines()[
            -2].strip()
        self.log.info(tbspc2_oid)

        step_txt = '----step2:在tablespace1上创建表及索引; expect:创建成功----'
        self.log.info(step_txt)
        create_result = self.sh.execut_db_sql(self.create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:在tablespace1上创建的表插入数据; expect:插入成功----'
        self.log.info(step_txt)
        insert_result = self.sh.execut_db_sql(self.insert_sql)
        self.log.info(insert_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_result,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.ANALYZE_SUCCESS_MSG, insert_result,
                      "执行失败" + step_txt)

        step_txt = '----step4:查询表对应的表空间及表文件物理位置; expect:查询结果正确----'
        self.log.info(step_txt)
        self.log.info('--查询pg_class系统表中表对应的tablespace--')
        table_info_sql = f"select oid,reltablespace from pg_class where " \
            f"relname = '{self.table_name}';"
        tmp_result = self.sh.execut_db_sql(table_info_sql).splitlines()[
            -2].split('|')
        self.log.info(tmp_result)
        tb_tbspc_oid = tmp_result[1].strip()
        self.assertEqual(tb_tbspc_oid, tbspc1_oid, "执行失败" + step_txt)
        self.log.info('--查询表对应的tablespace位置--')
        check_tb_1 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_tb_1[0],
                      "执行失败" + step_txt)

        step_txt = '----step5:查询索引对应的表空间及索引文件物理位置; expect:查询结果正确----'
        self.log.info(step_txt)
        self.log.info('--查询pg_class系统表中索引对应的tablespace--')
        index_info_sql = f"select oid,reltablespace from pg_class where " \
            f"relname = '{self.index_name}';"
        tmp_result = self.sh.execut_db_sql(index_info_sql).splitlines()[
            -2].split('|')
        self.log.info(tmp_result)
        idx_tbspc_oid = tmp_result[1].strip()
        self.assertEqual(idx_tbspc_oid, tbspc1_oid, "执行失败" + step_txt)
        self.log.info('--查询索引对应的tablespace位置--')
        check_idx_1 = self.check_ob_tbspc(self.index_name)
        self.log.info('--索引文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_idx_1[0],
                      "执行失败" + step_txt)

        step_txt = '----step6:查询数据; expect:正常使用索引----'
        self.log.info(step_txt)
        select_result = self.sh.execut_db_sql(self.select_sql)
        self.log.info(select_result)
        self.assertIn('Index Scan using', select_result, "执行失败" + step_txt)

        step_txt = '----step7:变更索引的表空间为tablespace2; expect:变更成功----'
        self.log.info(step_txt)
        alter_sql = f"alter index {self.index_name} " \
            f"set tablespace {self.tbspc_name2};"
        alter_result = self.sh.execut_db_sql(alter_sql)
        self.log.info(alter_result)
        self.assertIn(self.constant.ALTER_INDEX_SUCCESS_MSG, alter_result,
                      "执行失败" + step_txt)

        step_txt = '----step8:在tablespace1上创建的表插入数据; expect:插入成功----'
        self.log.info(step_txt)
        insert_result = self.sh.execut_db_sql(self.insert_sql)
        self.log.info(insert_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_result,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.ANALYZE_SUCCESS_MSG, insert_result,
                      "执行失败" + step_txt)

        step_txt = '----step9:查询表对应的表空间及表文件物理位置; expect:查询结果不变----'
        self.log.info(step_txt)
        self.log.info('--查询pg_class系统表中表对应的tablespace--')
        tmp_result = self.sh.execut_db_sql(table_info_sql).splitlines()[
            -2].split('|')
        self.log.info(tmp_result)
        tb_tbspc_oid = tmp_result[1].strip()
        self.assertEqual(tb_tbspc_oid, tbspc1_oid, "执行失败" + step_txt)
        self.log.info('--查询表对应的tablespace位置--')
        check_tb_1 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_tb_1[0],
                      "执行失败" + step_txt)

        step_txt = '----step10:查询索引对应的表空间及索引文件物理位置; expect:表空间变更----'
        self.log.info(step_txt)
        self.log.info('--查询pg_class系统表中索引对应的tablespace--')
        tmp_result = self.sh.execut_db_sql(index_info_sql).splitlines()[
            -2].split('|')
        self.log.info(tmp_result)
        idx_tbspc_oid = tmp_result[1].strip()
        self.assertEqual(idx_tbspc_oid, tbspc2_oid, "执行失败" + step_txt)
        self.log.info('--查询索引对应的tablespace位置--')
        check_idx_1 = self.check_ob_tbspc(self.index_name)
        self.log.info('--索引文件所在的路径为tablespace2相对路径--')
        self.assertIn(self.tbspc_location2, check_idx_1[0],
                      "执行失败" + step_txt)

        step_txt = '----step11:查询数据; expect:正常使用索引----'
        self.log.info(step_txt)
        select_result = self.sh.execut_db_sql(self.select_sql)
        self.log.info(select_result)
        self.assertIn('Index Scan using', select_result, "执行失败" + step_txt)

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

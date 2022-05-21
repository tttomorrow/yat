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
Case Name   : 指定数据库使用表空间后，在该数据库上表空间缺省建立表及索引
Description :
    1、创建tablespace1指定相对路径为location1;
    2、在tablespace1上创建数据库;
    3、查询数据库对应的表空间;
    4、数据库创建表及索引，不指定表空间;
    5、查询表对应的表空间及表文件物理位置;
    6、查询索引对应的表空间及索引文件物理位置;
Expect      :
    1、创建tablespace1指定相对路径为location1;创建成功
    2、在tablespace1上创建数据库;创建成功
    3、查询数据库对应的表空间;对应的表空间为tablespace1
    4、数据库创建表及索引，不指定表空间;创建成功
    5、查询表对应的表空间及表文件物理位置;pg_class表空间默认为0，物理位置为tablespace1路径
    6、查询索引对应的表空间及索引文件物理位置;pg_class表空间默认为0，物理位置为tablespace1路径
    备注，为零，则意味着使用该数据库的缺省表空间
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
        self.tbspc_name1 = 'tsp_tbspc0038_1'
        self.tbspc_location1 = 'tbspc0038_1'
        self.table_name = 't_tbspc0038'
        self.db_name = 'db_tbspc0038'
        self.index_name = 'idx_tbspc0038'
        self.create_db_sql = f'drop database if exists {self.db_name};' \
            f'create database {self.db_name} ' \
            f'tablespace {self.tbspc_name1};'
        self.create_object_sql = f'drop table if exists {self.table_name};' \
            f'create table {self.table_name}(id int,name varchar(100)); ' \
            f'create index {self.index_name} on {self.table_name}(id) ;'

    def test_main(self):
        step_txt = '----step1:创建tablespace1指定相对路径为location1;expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}' ;"
        create_result = self.sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--查询tablespace1 oid--')
        select_sql = f"select oid from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        tbspc1_oid = self.sh.execut_db_sql(select_sql).splitlines()[
            -2].strip()
        self.log.info(tbspc1_oid)

        step_txt = '----step2:在tablespace1上创建数据库;expect:创建成功----'
        self.log.info(step_txt)
        create_result = self.sh.execut_db_sql(self.create_db_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:查询数据库对应的表空间;expect:对应的表空间为tablespace1----'
        self.log.info(step_txt)
        db_info_sql = f"select dattablespace from PG_DATABASE " \
            f"where datname = '{self.db_name}';"
        tblspace_oid = self.sh.execut_db_sql(db_info_sql).splitlines()[
            -2].strip()
        self.log.info(tblspace_oid)
        self.assertEqual(tblspace_oid, tbspc1_oid, "执行失败" + step_txt)

        step_txt = '----step4:数据库创建表及索引，不指定表空间;expect:创建成功----'
        self.log.info(step_txt)
        create_result = self.sh.execut_db_sql(self.create_object_sql,
                                              dbname=f'{self.db_name}')
        self.log.info(create_result)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step5:查询表对应的表空间及表文件物理位置;' \
                   'expect:pg_class表空间默认为0，物理位置为tablespace1路径----'
        self.log.info(step_txt)
        table_info_sql = f"select oid,reltablespace from pg_class where " \
            f"relname = '{self.table_name}';"
        tmp_result = self.sh.execut_db_sql(table_info_sql,
                                           dbname=f'{self.db_name}')
        self.log.info(tmp_result)
        tblspace_oid = tmp_result.splitlines()[-2].split('|')[1].strip()
        self.assertEqual(tblspace_oid, '0', "执行失败" + step_txt)
        self.log.info('--查询表对应的tablespace位置--')
        check_tb_1 = self.check_ob_tbspc(self.table_name)
        self.log.info('--表文件所在的路径为tablespace1相对路径--')
        self.assertIn(self.tbspc_location1, check_tb_1[0],
                      "执行失败" + step_txt)

        step_txt = '----step6:查询索引对应的表空间及索引文件物理位置;' \
                   'expect:pg_class表空间默认为0，物理位置为tablespace1路径----'
        self.log.info(step_txt)
        index_info_sql = f"select oid,reltablespace from pg_class where " \
            f"relname = '{self.index_name}';"
        tmp_result = self.sh.execut_db_sql(index_info_sql,
                                           dbname=f'{self.db_name}')
        self.log.info(tmp_result)
        tblspace_oid = tmp_result.splitlines()[-2].split('|')[1].strip()
        self.assertEqual(tblspace_oid, '0', "执行失败" + step_txt)
        self.log.info('--查询索引对应的tablespace位置--')
        check_idx_1 = self.check_ob_tbspc(self.index_name)
        self.log.info('--索引文件所在的路径为tablespace2相对路径--')
        self.assertIn(self.tbspc_location1, check_idx_1[0],
                      "执行失败" + step_txt)

    def check_ob_tbspc(self, object_name):
        """
        :param object_name: 数据库对象名称，例如表名、索引名
        :return: 数据库对象文件实际位置及占用空间
        """
        location_sql = f"select pg_relation_filepath(" \
            f"(select oid from pg_class where relname = '{object_name}')" \
            f"::regclass);"
        tmp = self.sh.execut_db_sql(location_sql, dbname=f'{self.db_name}')
        t_link = tmp.splitlines()[-2].strip()
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
            f"drop database if exists {self.db_name};" \
            f"drop tablespace if exists {self.tbspc_name1};"
        clean_result = self.sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, clean_result,
                      "执行失败" + step1_txt)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, clean_result,
                      "执行失败" + step1_txt)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, clean_result,
                      "执行失败" + step1_txt)

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
Case Type   : file_fdw功能
Case Name   : file_fdw外表基础查询、explain、prepare功能验证
Description :
    1、新建文件1：
        1,test1,
        2,,test2
        3,NULL,NULL
        4,test4,test4
        5,test5,test5
    新建文件2：
        1 newtest1 newtest1
        1 newtest2 newtest2
        2 newtest1 newtest1
        2 newtest2 newtest2
        2 newtest3 newtest3
    2、创建服务
    3、创建外表1,创建外表2,创建普通表
    4、外表与外表、外表与普通表关联查询，explain功能验证
    5、外表prepare功能验证
Expect      :
    1、新建文件成功；
    2、创建服务成功
    3、创建外表1,创建外表2,创建普通表成功
    4、外表与外表、外表与普通表关联查询，explain功能验证成功
    5、外表prepare功能验证成功
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Filefdw0011(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_FDW_Filefdw_Case0011:初始化----')
        self.dbUserNode = Node(node='dbuser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.file_name1 = 'file_fdwCase0011_1.csv'
        self.file_path1 = os.path.join(macro.DB_BACKUP_PATH, self.file_name1)
        self.file_name2 = 'file_fdwCase0011_2.csv'
        self.file_path2 = os.path.join(macro.DB_BACKUP_PATH, self.file_name2)
        self.tb_name1 = 't_filefdw0011_1'
        self.tb_name2 = 't_filefdw0011_2'
        self.tb_name3 = 't_filefdw0011_3'
        self.svc_name = 'svc_filefdw_0011'
        self.suc_flag = 'QUERY PLAN'

    def test_main(self):
        step_txt = '----step1: 数据库用户创建文件; expect:创建成功----'
        self.log.info(step_txt)
        file_content = "1,test1,\n" \
                       "2,,test2\n" \
                       "3,NULL,NULL\n" \
                       "4,test4,test4\n" \
                       "5,test5,test5"
        write_cmd = f'echo -e "{file_content}" > {self.file_path1}'
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd).result()
        file_exist = f'cat {self.file_path1}'
        self.log.info(file_exist)
        file_cat = self.pri_dbuser.sh(file_exist).result()
        self.log.info(file_cat)
        self.log.info(file_content)
        self.assertEqual(file_content, file_cat, '执行失败:' + step_txt)

        file_content = "1 newtest1 newtest1\n" \
                       "1 newtest2 newtest2\n" \
                       "2 newtest1 newtest1\n" \
                       "2 newtest2 newtest2\n" \
                       "2 newtest3 newtest3"
        write_cmd = f'echo -e "{file_content}" > {self.file_path2}'
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd).result()
        file_exist = f'cat {self.file_path2}'
        self.log.info(file_exist)
        file_cat = self.pri_dbuser.sh(file_exist).result()
        self.log.info(file_cat)
        self.log.info(file_content)
        self.assertEqual(file_content, file_cat, '执行失败:' + step_txt)

        step_txt = '----step2: 创建服务; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop server {self.svc_name} cascade;" \
            f"create server {self.svc_name} foreign data wrapper file_fdw;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn("CREATE SERVER", result, "执行失败" + step_txt)

        step_txt = r'----step3: 创建外表1; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"create foreign table {self.tb_name1} " \
            f"(column1 int,column2 char(20) ,column3 char(20)) " \
            f"server {self.svc_name} options (filename '{self.file_path1}'," \
            f"format 'csv');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = r'----step3: 查询外表数据; expect:查询成功----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name1};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('5 rows', result, "执行失败" + step_txt)

        step_txt = r'----step3: 创建外表2; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"create foreign table {self.tb_name2} " \
            f"(column1 int,column2 char(20) ,column3 char(20)) " \
            f"server {self.svc_name} options (filename '{self.file_path2}'," \
            f"format 'csv',delimiter ' ');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = r'----step3: 查询外表数据; expect:查询成功----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name2};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('5 rows', result, "执行失败" + step_txt)

        step_txt = r'----step3: 创建普通表; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"create table {self.tb_name3} (id int, context text);" \
            f"insert into {self.tb_name3} values" \
            f"(1,'普通表内容1'),(2,'普通表内容2'),(3,'普通表内容3')," \
            f"(4,'普通表内容4'),(5,'普通表内容5');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, result,
                      "执行失败" + step_txt)
        self.assertIn('INSERT 0 5', result, "执行失败" + step_txt)
        step_txt = r'----step3: 查询普通表数据; expect:查询成功----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name3};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('5 rows', result, "执行失败" + step_txt)

        step_txt = r'----step4: 外表与外表、外表与普通表关联查询，explain功能验证; expect:成功----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name1} where column1 in(1,3,5) " \
            f"order by column1 desc;" \
            f"explain performance select * from {self.tb_name1} where " \
            f"column1 in(1,3,5) order by column1 desc;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)
        self.assertIn('3 rows', result, "执行失败" + step_txt)

        sql = f"select * from {self.tb_name1} a left join " \
            f"{self.tb_name2} b on (a.column1 = b.column1) " \
            f"order by a.column1;" \
            f"explain select * from {self.tb_name1} a left join " \
            f"{self.tb_name2} b on (a.column1 = b.column1) " \
            f"order by a.column1;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)
        self.assertIn('8 rows', result, "执行失败" + step_txt)

        sql = f"select a.*,b.column2,b.column3 from {self.tb_name3} a," \
            f"{self.tb_name1} b where a.id = b.column1;" \
            f"explain select a.*,b.column2,b.column3 from {self.tb_name3} a" \
            f",{self.tb_name1} b where a.id = b.column1;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)
        self.assertIn('5 rows', result, "执行失败" + step_txt)

        sql = f"select a.*,b.context from {self.tb_name1} a left join " \
            f"{self.tb_name3} b on (a.column1 = b.id) where column1 >=5;" \
            f"explain select a.*,b.context from {self.tb_name1} a left join" \
            f" {self.tb_name3} b on (a.column1 = b.id) where column1 >=5;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)
        self.assertIn('1 row', result, "执行失败" + step_txt)

        step_txt = r'----step5: 外表prepare功能验证成功; expect:成功----'
        self.log.info(step_txt)
        sql = f"prepare st(int) as select * from {self.tb_name1} where " \
            f"column1 = \$1;" \
            f"execute st(1);" \
            f"execute st(100);" \
            f"deallocate st;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.PREPARE_SUCCESS_MSG,
                      result, "执行失败" + step_txt)
        self.assertIn('1 row', result, "执行失败" + step_txt)
        self.assertIn('0 rows', result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step5:清理数据----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_name1};" \
            f"drop foreign table if exists {self.tb_name2};" \
            f"drop table if exists {self.tb_name3};" \
            f"drop server {self.svc_name} cascade;"
        result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result)

        step_txt = '----step6:删除文件----'
        self.log.info(step_txt)
        file_rm_cmd = f'rm -rf  {self.file_path1};ls -al {self.file_path1}'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_dbuser.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)
        file_rm_cmd = f'rm -rf  {self.file_path2};ls -al {self.file_path2}'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_dbuser.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        self.log.info('----Opengauss_Function_FDW_Filefdw_Case0011:执行完毕----')

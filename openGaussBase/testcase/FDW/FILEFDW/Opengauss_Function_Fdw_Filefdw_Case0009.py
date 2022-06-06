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
Case Name   : file_fdw外表option参数encoding功能验证
Description :
    1、新建文件/home/peilq_src0525/file_fdw.csv，文件编码为utf-8（locale查看默认编码）：
        1,test1,中文
        2,test2,zhognwen
    2、创建utf8编码的数据库
    3、创建服务
    4、创建外表(不指定encoding) ,查询外表数据
    5、修改外表(指定encoding为GBK),查询外表数据
    6、修改外表(指定encoding为Latin1),查询外表数据
    7、修改外表(指定encoding为utf-8),查询外表数据
Expect      :
    1、新建文件/home/peilq_src0525/file_fdw.csv，文件编码默认为utf-8；
    2、创建utf8编码的数据库成功
    3、创建服务成功
    4、创建外表(不指定encoding)成功
    查询外表数据，中文正常展示
    5、修改外表(指定encoding为GBK)成功
    查询外表数据，中文字符乱码
    6、修改外表(指定encoding为Latin1)成功
    查询外表数据，中文字符乱码
    7、修改外表(指定encoding为utf-8)成功
    查询外表数据，中文恢复正常
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Filefdw0009(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Fdw_Filefdw_Case0009:初始化----')
        self.dbUserNode = Node(node='dbuser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.file_name = 'file_fdwCase0009.csv'
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, self.file_name)
        self.db_name = 'db_filefdw0009'
        self.tb_name = 't_filefdw0009'
        self.svc_name = 'svc_filefdw_0009'
        self.suc_flag = '中文'

    def test_main(self):
        step_txt = '----step1: 数据库用户创建文件; expect:创建成功----'
        self.log.info(step_txt)
        file_content = "1,test1,中文\n" \
                       "2,test2,zhognwen"
        write_cmd = f'echo -e "{file_content}" > {self.file_path}'
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd).result()
        file_exist = f'cat {self.file_path}'
        self.log.info(file_exist)
        file_cat = self.pri_dbuser.sh(file_exist).result()
        self.log.info(file_cat)
        self.log.info(file_content)
        self.assertEqual(file_content, file_cat, '执行失败:' + step_txt)

        step_txt = '----step2: 创建utf8编码的数据库; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop database if exists {self.db_name};" \
            f"create database {self.db_name} " \
            f"ENCODING 'utf-8' template = template0;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS,
                      result, "执行失败" + step_txt)

        step_txt = '----step3: 创建服务; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop server {self.svc_name} cascade;" \
            f"create server {self.svc_name} foreign data wrapper file_fdw;"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertIn("CREATE SERVER", result, "执行失败" + step_txt)

        step_txt = r'----step4: 创建外表(不指定encoding); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"create foreign table {self.tb_name} " \
            f"(column1 int,column2 char(20),column3 char(20)) " \
            f"server {self.svc_name} options (filename '{self.file_path}'," \
            f"format 'csv');"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = r'----step4: 查询外表数据; expect:中文正常展示----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)

        step_txt = '----step5: 修改外表(指定encoding为GBK)成功;expect:成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} " \
            f"options (add encoding 'GBK');"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)
        step_txt = '----step5: 查询外表数据; expect:中文字符乱码;----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertNotIn(self.suc_flag, result, "执行失败" + step_txt)

        step_txt = '----step6: 修改外表(指定encoding为Latin1)成功;expect:成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} " \
            f"options (set encoding 'Latin1');"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)
        step_txt = '----step6: 查询外表数据; expect:中文字符乱码;----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertNotIn(self.suc_flag, result, "执行失败" + step_txt)

        step_txt = '----step7: 修改外表(指定encoding为utf-8)成功;expect:成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} " \
            f"options (set encoding 'utf-8');"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)
        step_txt = '----step7: 查询外表数据; expect:中文字符正常;----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql, dbname=self.db_name)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step8:清理数据----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_name};" \
            f"drop server {self.svc_name} cascade;"
        result = self.pri_sh.execut_db_sql(drop_sql, dbname=self.db_name)
        self.log.info(result)
        drop_sql = f"drop database if exists {self.db_name};"
        result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result)

        step_txt = '----step9:删除文件----'
        self.log.info(step_txt)
        file_rm_cmd = f'rm -rf  {self.file_path};ls -al {self.file_path}'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_dbuser.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        self.log.info('----Opengauss_Function_Fdw_Filefdw_Case0009:执行完毕----')

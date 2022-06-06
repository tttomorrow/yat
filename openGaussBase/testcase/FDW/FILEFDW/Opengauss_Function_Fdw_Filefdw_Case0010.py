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
Case Name   : file_fdw外表option参数force_not_null功能验证
Description :
    1、新建文件：
        1,test1,
        2,,test2
        3,NULL,NULL
    2、创建服务
    3、创建外表(force_not_null第二列为true，第三列为off),查询外表数据
    4、创建外表(force_not_null第二列为false，第三列为on),查询外表数据
Expect      :
    1、新建文件成功
    2、创建服务成功
    3、创建外表(force_not_null第二列为true，第三列为off)成功
    查询外表数据第二列为空或者NULL的字段展示为NULL
    4、创建外表(force_not_null第二列为false，第三列为on)成功
    查询外表数据第三列为空或者NULL的字段展示为NULL
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Filefdw0010(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_FDW_Filefdw_Case0010:初始化----')
        self.dbUserNode = Node(node='dbuser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.file_name = 'file_fdwCase0010.csv'
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, self.file_name)
        self.tb_name = 't_filefdw0010'
        self.svc_name = 'svc_filefdw_0010'
        self.suc_flag = 'NULL'

    def test_main(self):
        step_txt = '----step1: 数据库用户创建文件; expect:创建成功----'
        self.log.info(step_txt)
        file_content = "1,test1,\n" \
                       "2,,test2\n" \
                       "3,NULL,NULL"
        write_cmd = f'echo -e "{file_content}" > {self.file_path}'
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd).result()
        file_exist = f'cat {self.file_path}'
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

        step_txt = r'----step3: 创建外表(force_not_null不同列设置不同); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"create foreign table {self.tb_name} (column1 int," \
            f"column2 char(20) OPTIONS (force_not_null 'true')," \
            f"column3 char(20) OPTIONS (force_not_null 'off'))  " \
            f"server {self.svc_name} options (filename '{self.file_path}'," \
            f"format 'csv' ,null 'NULL');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = r'----step3: 查询外表数据; expect:第二列为空或者NULL的字段展示为NULL----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        sql = f"select column2 from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)
        sql = f"select column3 from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.suc_flag, result, "执行失败" + step_txt)

        step_txt = r'----step4: 创建外表(force_not_null不同列设置不同); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} (column1 int," \
            f"column2 char(20) OPTIONS (force_not_null 'false')," \
            f"column3 char(20) OPTIONS (force_not_null 'on'))" \
            f"server {self.svc_name} options (filename '{self.file_path}'," \
            f"format 'csv' ,null 'NULL');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = r'----step4: 查询外表数据; expect:第三列为空或者NULL的字段展示为NULL----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        sql = f"select column2 from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.suc_flag, result, "执行失败" + step_txt)
        sql = f"select column3 from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step5:清理数据----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_name};" \
            f"drop server {self.svc_name} cascade;"
        result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result)

        step_txt = '----step6:删除文件----'
        self.log.info(step_txt)
        file_rm_cmd = f'rm -rf  {self.file_path};ls -al {self.file_path}'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_dbuser.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        self.log.info('----Opengauss_Function_FDW_Filefdw_Case0010:执行完毕----')

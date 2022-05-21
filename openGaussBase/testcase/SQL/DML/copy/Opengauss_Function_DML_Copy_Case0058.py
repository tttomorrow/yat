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
Case Type   : 拷贝数据
Case Name   : delimiter 'delimiters'包含\.,e,5中的任何一个字符进行copy to/from
Description :
    1.创建测试表并插入数据
    2.构造数据文件
    3.delimiters包含\.进行copy to
    4.delimiters包含\.进行copy from
    5.delimiters包含e进行copy to
    6.delimiters包含e进行copy from
    7.delimiters包含5进行copy to
    8.delimiters包含5进行copy from
    9.清理环境
Expect      :
    1.创建测试表并插入数据成功
    2.构造数据文件成功
    3.copy失败
    4.copy失败
    5.copy失败
    6.copy失败
    7.copy失败
    8.copy失败
    9.清理环境成功
History     :
"""

import unittest
import os

from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
logger = Logger()


class CopyFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_Dml_Copy_Case0058开始执行')
        self.commonsh = CommonSH('PrimaryDbUser')
        self.userNode = Node(node='PrimaryDbUser')
        self.Constant = Constant()
        self.tb_name = 't_copy_58'
        self.file_name = 'testcopy58.dat'
        self.copy_dir_path = os.path.join(macro.DB_INSTANCE_PATH,
                                          'pg_copydir')

    def test_copy_file(self):
        text = 'step1:创建测试表并对测试表插入数据 '\
               'Expect:创建测试表并插入数据成功'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"drop table if exists {self.tb_name};"
            f"create table {self.tb_name} (sk integer,id varchar(16),"
            f"name varchar(20),sq_ft integer);"
            f"insert into {self.tb_name} values (001,'sk1','tt1',3331);"
            f"insert into {self.tb_name} values (002,'sk2','tt2',3332);"
            f"insert into {self.tb_name} values (003,'sk3','tt3',3333);")
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = 'step2:构造数据文件 Expect:构造数据文件成功'
        self.log.info(text)
        excute_cmd = f'''mkdir {self.copy_dir_path};
            touch {os.path.join(self.copy_dir_path, self.file_name)};'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        text = 'step3:delimiters包含\.进行copy to Expect:copy失败'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"copy {self.tb_name} to '"
            f"{os.path.join(self.copy_dir_path, self.file_name)}'"
            f"delimiters '\.';")
        self.log.info(sql_cmd)
        self.assertIn('cannot contain any characters', sql_cmd,
                      '执行失败:' + text)

        text = 'step4:delimiters包含\.进行copy from Expect:copy失败'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"copy {self.tb_name} from '"
            f"{os.path.join(self.copy_dir_path, self.file_name)}'"
            f"delimiters '\.';")
        self.log.info(sql_cmd)
        self.assertIn('cannot contain any characters', sql_cmd,
                      '执行失败:' + text)

        text = 'step5:delimiters包含e进行copy to Expect:copy失败'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"copy {self.tb_name} to '"
            f"{os.path.join(self.copy_dir_path, self.file_name)}'"
            f"delimiters '/e';")
        self.log.info(sql_cmd)
        self.assertIn('cannot contain any characters', sql_cmd,
                      '执行失败:' + text)

        text = 'step6:delimiters包含e进行copy from Expect:copy失败'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"copy {self.tb_name} from '"
            f"{os.path.join(self.copy_dir_path, self.file_name)}'"
            f"delimiters '/e';")
        self.log.info(sql_cmd)
        self.assertIn('cannot contain any characters', sql_cmd,
                      '执行失败:' + text)

        text = 'step7:delimiters包含5进行copy to Expect:copy失败'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"copy {self.tb_name} to '"
            f"{os.path.join(self.copy_dir_path, self.file_name)}'"
            f"delimiters '/5';")
        self.log.info(sql_cmd)
        self.assertIn('cannot contain any characters', sql_cmd,
                      '执行失败:' + text)

        text = 'step8:delimiters包含5进行copy from Expect:copy失败'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"copy {self.tb_name} from '"
            f"{os.path.join(self.copy_dir_path, self.file_name)}'"
            f"delimiters '/5';")
        self.log.info(sql_cmd)
        self.assertIn('cannot contain any characters', sql_cmd,
                      '执行失败:' + text)

    def tearDown(self):
        text = 'step9:清理环境 清理环境成功'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f"drop table if exists {self.tb_name};")
        self.log.info(sql_cmd)
        excute_cmd = f'''rm -rf {self.copy_dir_path}'''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, sql_cmd)
        self.log.info('Opengauss_Function_Dml_Copy_Case0058执行完成')





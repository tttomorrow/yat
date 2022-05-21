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
Case Name   : /copy from 对非法字符无容错能力
Description :
    1.创建测试表并插入数据
    DROP TABLE IF EXISTS TESTZL;
    CREATE TABLE TESTZL(
        SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
    INSERT INTO TESTZL VALUES (001,'SK1','TT',3332);
    INSERT INTO TESTZL VALUES (001,'SK1','TT',3332);
    INSERT INTO TESTZL VALUES (001,'SK1','TT',3332);
    2.构造步骤1表的数据文件,使用copy to把表数据拷贝到文件
    touch /opt/openGauss/cluster/dn1/testzl.dat;
    COPY TESTZL TO '/opt/openGauss/cluster/dn1/testzl.dat';
    3.将步骤2文件部分数据修改为非法字符\0
    sed -i 's/SK1/\\0/g' "/opt/openGauss/cluster/dn1/testzl.dat";
    4.使用\copy from将步骤3修改后的数据文件导入到表中
    \COPY TESTZL FROM '/opt/openGauss/cluster/dn1/pg_copydir/testzl.dat';
    5.清理环境
    DROP TABLE IF EXISTS TESTZL;
    rm -rf /opt/openGauss/cluster/dn1/testzl.dat
Expect      :
    1.成功
    2.构造成功
    3.修改成功
    4.拷贝失败
        invalid byte sequence for encoding "SQL_ASCII"
    5.清理环境成功
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class CopyFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_DML_Copy_Case0047开始执行----')
        self.pri_node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.invalid_char = r'\\0'
        self.t_name = 't_dml_copy_case0047'
        self.copy_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      'dir_dml_copy_case0047')
        self.copy_file = os.path.join(self.copy_path, 'dml_copy_case0047.dat')

    def test_copy_file(self):
        step_txt = '----step1：创建测试表并插入数据 expect:成功----'
        self.log.info(step_txt)
        sql_cmd = f"DROP TABLE IF EXISTS {self.t_name};" \
            f"CREATE TABLE {self.t_name}(" \
            f"SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);" \
            f"INSERT INTO {self.t_name} VALUES (001,'SK1','TT',3332);" \
            f"INSERT INTO {self.t_name} VALUES (001,'SK1','TT',3332);" \
            f"INSERT INTO {self.t_name} VALUES (001,'SK1','TT',3332);"
        msg = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(msg)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg,
                      '执行失败:' + step_txt)

        step_txt = '----step2：构造步骤1表的数据文件,使用copy to把表数据拷贝到文件 expect:构造成功----'
        self.log.info(step_txt)
        execute_cmd = f'mkdir {self.copy_path};' \
            f'touch {self.copy_file};'
        self.log.info(execute_cmd)
        msg = self.pri_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertEqual(msg, '', '执行失败:' + step_txt)
        copy_to_sql = f"COPY {self.t_name} TO '{self.copy_file}';"
        copy_to_msg = self.pri_sh.execut_db_sql(copy_to_sql)
        self.log.info(copy_to_msg)
        self.assertIn('COPY 3', copy_to_msg, '执行失败:' + step_txt)

        step_txt = '----step3：将步骤2文件部分数据修改为非法字符\0 expect:修改成功----'
        self.log.info(step_txt)
        execute_cmd = f"sed -i 's/SK1/{self.invalid_char}/g' " \
            f"{self.copy_file};" \
            f"cat {self.copy_file};"
        self.log.info(execute_cmd)
        msg = self.pri_node.sh(execute_cmd).result()
        self.log.info(msg)
        self.assertIn('1\t\\0', msg, '执行失败:' + step_txt)

        step_txt = '----step4：使用\copy from将步骤3修改后的数据文件导入到表中 expect:拷贝失败----'
        self.log.info(step_txt)
        copy_from_sql = f"\COPY {self.t_name} FROM '{self.copy_file}';"
        copy_from_msg = self.pri_sh.execut_db_sql(copy_from_sql)
        self.log.info(copy_from_msg)
        self.assertIn(self.constant.COPY_ENCODING_ERROR_MSG, copy_from_msg,
                      '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----step5：清理环境----')
        text_1 = '----删除数据文件 expect:成功----'
        self.log.info(text_1)
        rm_cmd = f'rm -rf {self.copy_path}; '
        self.log.info(rm_cmd)
        rm_msg = self.pri_node.sh(rm_cmd).result()
        self.log.info(rm_msg)

        text_2 = '----删除表 expect:成功----'
        self.log.info(text_2)
        drop_sql = f'DROP TABLE IF EXISTS {self.t_name};'
        drop_msg = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_msg)
        self.log.info('----Opengauss_Function_DML_Copy_Case0047执行完成----')

        self.log.info('----断言tearDown执行成功----')
        self.assertEqual(rm_msg, '', '执行失败:' + text_1)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text_2)

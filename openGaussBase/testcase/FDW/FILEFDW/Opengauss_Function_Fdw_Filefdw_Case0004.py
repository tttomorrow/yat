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
Case Name   : file_fdw外表option参数delimiter功能验证
Description :
    1、数据库用户创建文件（tab进行字段分隔）：
    2、创建服务
    3、创建外表，指定format为csv（默认,分隔）
    4、查询外表数据
    5、修改外表format为text，（默认用tab分隔）
    6、查询外表数据
    7、修改外表format为csv，指定delimiter为tab
    8、查询外表数据
    9、数据库用户创建文件（,进行字段分隔）
    10、创建外表，指定format 为csv（默认,分隔）
    11、查询外表数据
    12、修改外表format为text,（默认用tab分隔）
    13、查询外表数据
    14、执行建表delimiter为\r建表语句
    15、执行建表delimiter为\n建表语句
Expect      :
    1、数据库用户创建文件成功
    2、创建服务成功
    3、创建外表，指定format为csv（默认,分隔）成功
    4、查询外表数据失败
    5、修改外表format为text，（默认用tab分隔）成功
    6、查询外表数据成功
    7、修改外表format为csv，指定delimiter为tab成功
    8、查询外表数据成功
    9、数据库用户创建文件（,进行字段分隔）成功
    10、创建外表，指定format 为csv（默认,分隔）成功
    11、查询外表数据成功
    12、修改外表format为text,（默认用tab分隔）成功
    13、查询外表数据失败
    14、执行建表delimiter为\r建表语句失败
    15、执行建表delimiter为\n建表语句失败
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Filefdw0004(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Fdw_Filefdw_Case0004:初始化----')
        self.dbUserNode = Node(node='dbuser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.file_name = 'file_fdwCase0004.csv'
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, self.file_name)
        self.tb_name = 't_filefdw0004'
        self.svc_name = 'svc_filefdw_0004'
        self.err_flag1 = 'ERROR:  missing data for column'
        self.err_flag2 = 'ERROR:  COPY delimiter cannot be newline ' \
                         'or carriage return'
        self.suc_flag = '4 rows'

    def test_main(self):
        step_txt = '----step1:数据库用户创建文件成功; expect:创建成功----'
        self.log.info(step_txt)
        file_content = '0\tcolumn2\tcolumn3\n' \
                       '1\ttest1\ttest1\n' \
                       '2\ttest2\ttest2\n' \
                       '3\ttest3\ttest3'
        write_cmd = f"echo -e '{file_content}' > {self.file_path}"
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd)
        file_cat_cmd = f'cat {self.file_path}'
        self.log.info(file_cat_cmd)
        file_cat_result = self.pri_dbuser.sh(file_cat_cmd).result()
        self.log.info(file_cat_result)
        self.assertEqual(file_content, file_cat_result, '执行失败:' + step_txt)

        step_txt = '----step2:创建服务; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop server {self.svc_name} cascade;" \
            f"create server {self.svc_name} foreign data wrapper file_fdw;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn("CREATE SERVER", result, "执行失败" + step_txt)

        step_txt = '----step3:创建外表，指定format为csv（默认,分隔）; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 text,colum3 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',format 'csv');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step4:查询外表数据; expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step5:修改外表format为text，（默认用tab分隔）; expect:修改成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} options" \
            f"(set format 'text');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)

        step_txt = '----step6:查询外表数据; expect:查询成功----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)

        step_txt = '----step7:修改外表format为csv，指定delimiter为tab; expect:修改成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} options" \
            f"(set format 'csv',add delimiter '\t');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)

        step_txt = '----step8:查询外表数据成功; expect:查询成功----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)

        step_txt = '----step9:数据库用户创建文件（,进行字段分隔）; expect:创建成功----'
        self.log.info(step_txt)
        file_content = '0,column2,column3\n' \
                       '1,test1,test1\n' \
                       '2,test2,test2\n' \
                       '3,test3,test3'
        write_cmd = f"echo -e '{file_content}' > {self.file_path}"
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd)
        file_cat_cmd = f'cat {self.file_path}'
        self.log.info(file_cat_cmd)
        file_cat_result = self.pri_dbuser.sh(file_cat_cmd).result()
        self.log.info(file_cat_result)
        self.assertEqual(file_content, file_cat_result, '执行失败:' + step_txt)

        step_txt = '----step10:创建外表，指定format 为csv（默认,分隔）; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 text,colum3 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',format 'csv');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step11:查询外表数据; expect:查询成功----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result, "执行失败" + step_txt)

        step_txt = '----step12:修改外表format为text,（默认用tab分隔）; expect:修改成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} options" \
            f"(set format 'text');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)

        step_txt = '----step13:查询外表数据; expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step14:执行建表delimiter为\\r建表语句; expect:创建失败----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 text,colum3 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',delimiter '\r');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag2, result, "执行失败" + step_txt)

        step_txt = '----step15:执行建表delimiter为\\n建表语句; expect:创建失败----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 text,colum3 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',delimiter '\n');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag2, result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step16:清理数据----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_name};" \
            f"drop server {self.svc_name} cascade;"
        result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result)

        step_txt = '----step17:删除文件----'
        self.log.info(step_txt)
        file_rm_cmd = f'rm -rf  {self.file_path};ls -al {self.file_path}'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_dbuser.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        self.log.info('----Opengauss_Function_Fdw_Filefdw_Case0004:执行完毕----')

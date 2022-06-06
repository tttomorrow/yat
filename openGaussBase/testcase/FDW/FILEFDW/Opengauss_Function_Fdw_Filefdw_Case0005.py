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
Case Name   : file_fdw外表option参数filename及文件内容与外表字段匹配验证
Description :
    1、新建文件
    2、创建服务
    3、创建外表(指定filename为空),查询外表数据
    4、修改外表(指定filename为相对路径),查询外表数据
    5、创建外表(文件字段比外表多，文件3个字段，外表2个字段),查询外表数据
    6、创建外表(文件字段比外表多，文件3个字段，外表4个字段),查询外表数据
    7、创建外表(文件第二列是字符串类型，外表第二列指定int类型),查询外表数据
    8、创建外表(文件第二列长度为5，外表第二列指定长度为4),查询外表数据
    9、修改数据文件无读权限成功，创建外表,查询外表数据
    10、恢复数据文件读权限成功,查询外表数据
Expect      :
    1、新建文件成功
    2、创建服务成功
    3、创建外表(指定filename为空)成功，查询外表数据失败
    4、修改外表(指定filename为相对路径)成功，查询外表数据失败
    5、创建外表(文件字段比外表多，文件3个字段，外表2个字段)成功,查询外表数据失败
    6、创建外表(文件字段比外表多，文件3个字段，外表4个字段)成功,查询外表数据失败
    7、创建外表(文件第二列是字符串类型，外表第二列指定int类型)成功,查询外表数据失败
    8、创建外表(文件第二列长度为5，外表第二列指定长度为4)成功;查询外表数据失败
    9、修改数据文件无读权限成功，创建外表成功;查询外表数据失败
    10、恢复数据文件读权限成功;查询外表数据成功
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Filefdw0005(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Fdw_Filefdw_Case0005:初始化----')
        self.dbUserNode = Node(node='dbuser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.file_name = 'file_fdwCase0005.csv'
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, self.file_name)
        self.tb_name = 't_filefdw0005'
        self.svc_name = 'svc_filefdw_0005'
        self.err_flag1 = 'No such file or directory'
        self.err_flag2 = 'ERROR:  extra data after last expected column'
        self.err_flag3 = 'ERROR:  missing data for column'
        self.err_flag4 = 'ERROR:  invalid input syntax for integer'
        self.err_flag5 = 'ERROR:  value too long for type '
        self.suc_flag = '4 rows'

    def test_main(self):
        step_txt = '----step1:数据库用户创建文件成功; expect:创建成功----'
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

        step_txt = '----step2:创建服务; expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop server {self.svc_name} cascade;" \
            f"create server {self.svc_name} foreign data wrapper file_fdw;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn("CREATE SERVER", result, "执行失败" + step_txt)

        step_txt = '----step3:创建外表(指定filename为空); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 int,column2 char(20),column3 char(20)) " \
            f"server {self.svc_name} " \
            f"options (filename '',format 'csv', header 'true');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = '----step3:查询外表数据(指定filename为空); expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step4:修改外表(指定filename为相对路径); expect:修改成功----'
        self.log.info(step_txt)
        sql = f"alter foreign table {self.tb_name} " \
            f"options (set filename '{self.file_name}');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertEqual("ALTER FOREIGN TABLE", result, "执行失败" + step_txt)
        step_txt = '----step4:查询外表数据(指定filename为相对路径); expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step5:创建外表(文件字段比外表多，文件3个字段，外表2个字段); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',format 'csv');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = '----step5:查询外表数据(文件字段比外表多); expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag2, result, "执行失败" + step_txt)

        step_txt = '----step6:创建外表(文件字段比外表多，文件3个字段，外表4个字段); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 text,colum3 text,column4 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',format 'csv');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = '----step6:查询外表数据(文件字段比外表少); expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag3, result, "执行失败" + step_txt)

        step_txt = '----step7:创建外表(文件第二列是字符串类型，外表第二列指定int类型); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 int,colum3 text,column4 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',format 'csv');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = '----step7:查询外表数据(文件与外表列数据类型不符); expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag4, result, "执行失败" + step_txt)

        step_txt = '----step8:创建外表(文件第二列长度为5，外表第二列指定长度为4); expect:创建成功----'
        self.log.info(step_txt)
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 char(5),colum3 text,column4 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',format 'csv');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = '----step8:查询外表数据(文件第二列长度为5，外表第二列指定长度为4); expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.err_flag5, result, "执行失败" + step_txt)

        step_txt = '----step9:修改数据文件无读权限; expect:修改成功----'
        self.log.info(step_txt)
        chmod_cmd = f"chmod 333 {self.file_path}"
        self.log.info(chmod_cmd)
        self.pri_dbuser.sh(chmod_cmd)
        file_cat_cmd = f'ls -al {self.file_path}'
        self.log.info(file_cat_cmd)
        self.log.info(self.pri_dbuser.sh(file_cat_cmd).result())
        sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign table {self.tb_name} " \
            f"(column1 text,column2 text,colum3 text) " \
            f"server {self.svc_name} " \
            f"options (filename '{self.file_path}',format 'csv');"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        step_txt = '----step9:查询外表数据(文件无权限); expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENY_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step10:恢复数据文件读权限; expect:修改成功----'
        self.log.info(step_txt)
        chmod_cmd = f"chmod 777 {self.file_path}"
        self.log.info(chmod_cmd)
        self.pri_dbuser.sh(chmod_cmd)
        file_cat_cmd = f'ls -al {self.file_path}'
        self.log.info(file_cat_cmd)
        self.log.info(self.pri_dbuser.sh(file_cat_cmd).result())
        step_txt = '----step10:查询外表数据(文件无权限; expect:查询失败----'
        self.log.info(step_txt)
        sql = f"select * from {self.tb_name};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.suc_flag, result,
                      "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step11:清理数据----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_name};" \
            f"drop server {self.svc_name} cascade;"
        result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result)

        step_txt = '----step12:删除文件----'
        self.log.info(step_txt)
        file_rm_cmd = f'rm -rf  {self.file_path};ls -al {self.file_path}'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_dbuser.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        self.log.info('----Opengauss_Function_Fdw_Filefdw_Case0005:执行完毕----')

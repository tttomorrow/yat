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
Case Type   : postgres_fdw功能
Case Name   : file_fdw相关对象基本创建、查询权限校验
Description :
    1、清理已存在用户并创建用户
    2、系统用户进行file_fdw服务创建
    3、普通用户进行file_fdw服务创建
    4、初始用户进行file_fdw服务创建
    5、系统用户进行user mapping创建
    6、普通用户进行user mapping创建
    7、初始用户进行user mapping创建
    8、系统用户进行file_fdw外表创建
    9、普通用户进行file_fdw外表创建
    10、初始用户进行file_fdw外表创建
    11、系统用户进行file_fdw外表查询
    12、普通用户进行file_fdw外表查询
    13、初始用户进行file_fdw外表查询
Expect      :
    1、清理已存在用户并创建用户，操作成功
    2、系统用户进行file_fdw服务创建，创建失败
    3、普通用户进行file_fdw服务创建，创建失败
    4、初始用户进行file_fdw服务创建，创建成功
    5、系统用户进行user mapping创建，创建失败
    6、普通用户进行user mapping创建，创建失败
    7、初始用户进行user mapping创建，创建失败
    8、系统用户进行file_fdw外表创建，创建失败
    9、普通用户进行file_fdw外表创建，创建失败
    10、初始用户进行file_fdw外表创建，创建成功
    11、系统用户进行file_fdw外表查询，查询成功
    12、普通用户进行file_fdw外表查询，查询失败
    13、初始用户进行file_fdw外表查询，查询成功
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Filefdw0001(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:初始化----')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.u_sys = 'u_filefdw_sys0001'
        self.u_com = 'u_filefdw_com0001'
        self.svc = 'svc_file_server0001'
        self.tb_fdw = 'tb_filefdw0001'
        self.file_name = 'file_fdwCase0001.csv'
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, self.file_name)

        self.err_flag1 = 'ERROR:  Dist fdw are only available for ' \
                         'the supper user and Operatoradmin'
        self.err_flag2 = "ERROR:  file_fdw doesn't support in USER MAPPING."
        self.err_flag3 = 'ERROR:  must be owner of foreign server'
        self.err_flag4 = 'ERROR:  permission denied for'
        self.connect_sys = f'-U {self.u_sys} -W {macro.PASSWD_INITIAL}'
        self.connect_com = f'-U {self.u_com} -W {macro.PASSWD_INITIAL}'

    def test_main(self):
        step_txt = '----step0: 数据库用户创建文件; expect:创建成功----'
        self.log.info(step_txt)
        file_content = '0,column2,column3\n' \
                       '1,test1,test1\n' \
                       '2,test2,test2\n' \
                       '3,test3,test3'
        write_cmd = f"echo -e '{file_content}' > {self.file_path}"
        self.log.info(write_cmd)
        self.pri_dbuser.sh(write_cmd).result()
        file_exist = f'cat {self.file_path}'
        self.log.info(file_exist)
        file_cat = self.pri_dbuser.sh(file_exist).result()
        self.log.info(file_cat)
        self.assertTrue(file_content == file_cat, '执行失败:' + step_txt)

        step_txt = '----step1:清理已存在用户并创建用户; expect:成功----'
        self.log.info(step_txt)
        sql = f"drop user if exists {self.u_sys},{self.u_com} cascade;" \
            f"create user {self.u_sys} sysadmin " \
            f"password '{macro.PASSWD_INITIAL}';" \
            f"create user {self.u_com} password '{macro.PASSWD_INITIAL}';"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        assert_flag = result.count(self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step2: 系统用户进行file_fdw服务创建; expect:创建失败----'
        svc_sql = f"create server {self.svc} foreign data wrapper file_fdw;"
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(svc_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step3: 普通用户进行file_fdw服务创建; expect:创建失败----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(svc_sql, sql_type=self.connect_com)
        self.log.info(result)
        self.assertIn(self.err_flag4, result, "执行失败" + step_txt)

        step_txt = '----step4: 初始用户进行file_fdw服务创建; expect:创建成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(svc_sql)
        self.log.info(result)
        self.assertIn(self.constant.create_server_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step5: 系统用户进行user mapping创建; expect:创建失败----'
        self.log.info(step_txt)
        map_sql = f"create user mapping for {self.u_sys} server {self.svc};"
        result = self.pri_sh.execut_db_sql(map_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step6: 普通用户进行user mapping创建; expect:创建失败----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(map_sql, sql_type=self.connect_com)
        self.log.info(result)
        self.assertIn(self.err_flag3, result, "执行失败" + step_txt)

        step_txt = '----step7: 初始用户进行user mapping创建; expect:创建失败----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(map_sql)
        self.log.info(result)
        self.assertIn(self.err_flag2, result, "执行失败" + step_txt)

        step_txt = '----step8: 系统用户进行file_fdw外表创建; expect:创建失败----'
        self.log.info(step_txt)
        tb_sql = f"create foreign table {self.tb_fdw} " \
            f"(column1 int,column2 char(20),column3 char(20)) " \
            f"server {self.svc} options (filename '{self.file_path}'," \
            f"format 'csv', header 'true');"
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step9: 普通用户进行file_fdw外表创建; expect:创建失败----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_com)
        self.log.info(result)
        self.assertIn(self.err_flag4, result, "执行失败" + step_txt)

        step_txt = '----step10: 初始用户进行file_fdw外表创建; expect:创建成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step11: 系统用户进行file_fdw外表查询; expect:查询成功----'
        self.log.info(step_txt)
        tb_sql = f"select * from {self.tb_fdw};"
        result1 = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_sys)
        self.log.info(result1)
        self.assertIn('3 rows', result1, "执行失败" + step_txt)

        step_txt = '----step12: 普通用户进行file_fdw外表查询; expect:查询失败----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_com)
        self.log.info(result)
        self.assertIn(self.err_flag4, result, "执行失败" + step_txt)

        step_txt = '----step13: 初始用户进行file_fdw外表查询; expect:查询成功----'
        self.log.info(step_txt)
        result2 = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        self.assertIn('3 rows', result2, "执行失败" + step_txt)
        self.assertEqual(result1, result2, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step:清理数据; expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_fdw};" \
            f"drop server {self.svc} cascade;" \
            f"drop user if exists {self.u_sys},{self.u_com} cascade;"
        result1 = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(result1)

        step_txt = '----step:删除文件; expect:删除成功----'
        self.log.info(step_txt)
        file_rm_cmd = f'rm -rf {self.file_path};' \
            f'if [ -f {self.file_path} ]; ' \
            f'then echo "exists"; else echo "not exists"; fi'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_dbuser.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        step_txt = '----teardown断言----'
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.drop_server_success, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, result1,
                      "执行失败" + step_txt)
        self.assertEqual('not exists', file_rm_result, "执行失败" + step_txt)

        self.log.info(f'----{os.path.basename(__file__)}:执行完毕----')

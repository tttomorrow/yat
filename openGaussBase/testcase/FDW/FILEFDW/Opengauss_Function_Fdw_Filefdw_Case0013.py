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
Case Name   : 运维管理员创建file_fdw对象server、foreign table校验
Description :
    1.数据库用户创建文件;
    2.修改参数operation_mode为off;
    3.清理并创建运维管理员用户;
    4.运维管理员用户非运维模式下进行file_fdw服务创建;
    5.修改参数operation_mode为on;
    6.运维管理员用户运维模式下进行file_fdw服务创建;
    7.修改参数operation_mode为off;
    8.运维管理员用户非运维模式下进行usermapping创建;
    9.运维管理员用户非运维模式下file_fdw外表创建;
    10.修改参数operation_mode为on;
    11.运维管理员用户运维模式下进行usermapping创建;
    12.运维管理员用户运维模式下file_fdw外表创建;
    13.进行file_fdw外表查询;
Expect      :
    1.数据库用户创建文件;expect:创建成功
    2.修改参数operation_mode为off;expect:修改成功
    3.清理并创建运维管理员用户;expect:成功
    4.运维管理员用户非运维模式下进行file_fdw服务创建;expect:创建失败
    5.修改参数operation_mode为on;expect:修改成功
    6.运维管理员用户运维模式下进行file_fdw服务创建;expect:创建成功
    7.修改参数operation_mode为off;expect:修改成功
    8.运维管理员用户非运维模式下进行usermapping创建;expect:创建失败
    9.运维管理员用户非运维模式下file_fdw外表创建;expect:创建失败
    10.修改参数operation_mode为on;expect:修改成功
    11.运维管理员用户运维模式下进行usermapping创建;expect:创建失败
    12.运维管理员用户运维模式下file_fdw外表创建;expect:创建成功
    13.进行file_fdw外表查询;expect:查询成功
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
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
        self.com = Common()
        self.u_opradmin = 'u_filefdw_opra0013'
        self.svc = 'svc_file_server0013'
        self.tb_fdw = 'tb_filefdw0013'
        self.file_name = 'file_fdwCase0013.csv'
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, self.file_name)

        self.err_flag1 = 'ERROR:  Dist fdw are only available for ' \
                         'the supper user and Operatoradmin'
        self.err_flag2 = "ERROR:  file_fdw doesn't support in USER MAPPING."
        self.conn_opra = f'-U {self.u_opradmin} -W {macro.PASSWD_INITIAL}'

        step_txt = '----查询log_file_mode初始值----'
        self.log.info(step_txt)
        self.mode = self.com.show_param("operation_mode")

    def test_main(self):
        step_txt = '----step1: 数据库用户创建文件; expect:创建成功----'
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

        step_txt = '----step2:修改参数operation_mode为off; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'operation_mode=off')
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step3:清理并创建运维管理员用户; expect:成功----'
        self.log.info(step_txt)
        sql = f"drop user if exists {self.u_opradmin} cascade;" \
            f"create user {self.u_opradmin} with opradmin " \
            f"password '{macro.PASSWD_INITIAL}';" \
            f"grant all privileges to {self.u_opradmin};"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step4: 运维管理员用户非运维模式下进行file_fdw服务创建; expect:创建失败----'
        svc_sql = f"create server {self.svc} foreign data wrapper file_fdw;"
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(svc_sql, sql_type=self.conn_opra)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step5:修改参数operation_mode为on; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'operation_mode=on')
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step6: 运维管理员用户运维模式下进行file_fdw服务创建; expect:创建成功----'
        svc_sql = f"create server {self.svc} foreign data wrapper file_fdw;"
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(svc_sql,
                                           sql_type=self.conn_opra)
        self.log.info(result)
        self.assertIn(self.constant.create_server_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step7:修改参数operation_mode为off; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'operation_mode=off')
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step8: 运维管理员用户非运维模式下进行usermapping创建; expect:创建失败----'
        self.log.info(step_txt)
        map_sql = f"create user mapping for {self.u_opradmin} " \
            f"server {self.svc};"
        result = self.pri_sh.execut_db_sql(map_sql,
                                           sql_type=self.conn_opra)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step9: 运维管理员用户非运维模式下file_fdw外表创建; expect:创建失败----'
        self.log.info(step_txt)
        tb_sql = f"create foreign table {self.tb_fdw} " \
            f"(column1 int,column2 char(20),column3 char(20)) " \
            f"server {self.svc} options (filename '{self.file_path}'," \
            f"format 'csv', header 'true');"
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.conn_opra)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step10:修改参数operation_mode为on; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'operation_mode=on')
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step11: 运维管理员用户运维模式下进行usermapping创建; expect:创建失败----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(map_sql,
                                           sql_type=self.conn_opra)
        self.log.info(result)
        self.assertIn(self.err_flag2, result, "执行失败" + step_txt)

        step_txt = '----step12: 运维管理员用户运维模式下file_fdw外表创建; expect:创建成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.conn_opra)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step13: 进行file_fdw外表查询; expect:查询成功----'
        self.log.info(step_txt)
        tb_sql = f"select * from {self.tb_fdw} "
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.conn_opra)
        self.log.info(result)
        self.assertIn('3 rows', result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step:还原参数operation_mode为默认值; expect:修改成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execute_gsguc('reload',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f'operation_mode={self.mode}')

        step_txt = '----step:清理数据; expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_fdw};" \
            f"drop server {self.svc} cascade;" \
            f"drop user if exists {self.u_opradmin} cascade;"
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
        self.assertTrue(result, '执行失败:' + step_txt)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.drop_server_success, result1,
                      "执行失败" + step_txt)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, result1,
                      "执行失败" + step_txt)
        self.assertEqual('not exists', file_rm_result, "执行失败" + step_txt)

        self.log.info(f'----{os.path.basename(__file__)}:执行完毕----')

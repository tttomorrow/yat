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
Case Name   : file_fdw相关对象创建、修改、删除权限校验-涉及赋权等操作
Description :
    1.数据库用户创建文件;
    2.清理已存在用户并创建用户;
    3.初始用户进行file_fdw服务创建;
    4.初始用户对系统用户file_fdw服务赋权;
    5.系统用户进行user
    6.系统用户进行file_fdw外表创建;
    7.初始用户进行file_fdw外表创建;
    8.系统用户进行file_fdw外表option修改;
    9.初始用户修改表owner为系统用户;
    10.系统用户再次进行file_fdw外表option修改;
    11.初始用户进行file_fdw外表option修改;
    12.初始用户进行file_fdw外表结构修改;
    13.初始用户进行file_fdw外表进行增删改;
    14.初始用户进行file_fdw服务(存在外表未删除)删除;
    15.普通用户进行file_fdw外表删除;
    16.系统用户进行file_fdw外表删除;
    17.普通用户进行file_fdw服务删除;
    18.系统用户进行file_fdw服务(不存在外表)删除;
Expect      :
    1.数据库用户创建文件;expect:创建成功
    2.清理已存在用户并创建用户;expect:成功
    3.初始用户进行file_fdw服务创建;expect:创建成功
    4.初始用户对系统用户file_fdw服务赋权;expect:赋权成功
    5.系统用户进行userexpect:创建失败
    6.系统用户进行file_fdw外表创建;expect:创建失败
    7.初始用户进行file_fdw外表创建;expect:创建成功
    8.系统用户进行file_fdw外表option修改;expect:修改失败
    9.初始用户修改表owner为系统用户;expect:修改成功
    10.系统用户再次进行file_fdw外表option修改;expect:修改失败
    11.初始用户进行file_fdw外表option修改;expect:修改成功
    12.初始用户进行file_fdw外表结构修改;expect:修改失败
    13.初始用户进行file_fdw外表进行增删改;expect:操作失败
    14.初始用户进行file_fdw服务(存在外表未删除)删除;expect:删除失败
    15.普通用户进行file_fdw外表删除;expect:删除失败
    16.系统用户进行file_fdw外表删除;expect:删除成功
    17.普通用户进行file_fdw服务删除;expect:删除失败
    18.系统用户进行file_fdw服务(不存在外表)删除;expect:删除成功
History     :
"""
import os
import re
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Filefdw0002(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:初始化----')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.u_sys = 'u_filefdw_sys0002'
        self.u_com = 'u_filefdw_com0002'
        self.svc = 'svc_file_server0002'
        self.tb_fdw = 'tb_filefdw0002'
        self.file_name = 'file_fdwCase0002.csv'
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, self.file_name)

        self.err_flag1 = 'ERROR:  Dist fdw are only available for ' \
                         'the supper user and Operatoradmin'
        self.err_flag2 = 'ERROR:  Un-support feature'
        self.err_flag3 = 'ERROR:  permission denied'
        self.err_flag4 = 'ERROR:  cannot drop server .* ' \
                         'because other objects depend on it'
        self.connect_sys = f'-U {self.u_sys} -W {macro.PASSWD_INITIAL}'
        self.connect_com = f'-U {self.u_com} -W {macro.PASSWD_INITIAL}'

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

        step_txt = '----step2:清理已存在用户并创建用户; expect:成功----'
        self.log.info(step_txt)
        sql = f"drop user if exists {self.u_sys},{self.u_com} cascade;" \
            f"create user {self.u_sys} sysadmin " \
            f"password '{macro.PASSWD_INITIAL}';" \
            f"create user {self.u_com} password '{macro.PASSWD_INITIAL}';"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        assert_flag = result.count(self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step3: 初始用户进行file_fdw服务创建; expect:创建成功----'
        svc_sql = f"create server {self.svc} foreign data wrapper file_fdw;"
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(svc_sql)
        self.log.info(result)
        self.assertIn(self.constant.create_server_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step4: 初始用户对系统用户file_fdw服务赋权; expect:赋权成功----'
        self.log.info(step_txt)
        map_sql = f"grant usage on foreign server {self.svc} to {self.u_sys};"
        result = self.pri_sh.execut_db_sql(map_sql)
        self.log.info(result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step5: 系统用户进行user mapping创建; expect:创建失败----'
        self.log.info(step_txt)
        map_sql = f"create user mapping for {self.u_sys} server {self.svc};"
        result = self.pri_sh.execut_db_sql(map_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step6: 系统用户进行file_fdw外表创建; expect:创建失败----'
        self.log.info(step_txt)
        tb_sql = f"create foreign table public.{self.tb_fdw} " \
            f"(column1 int,column2 char(20),column3 char(20)) " \
            f"server {self.svc} options (filename '{self.file_path}'," \
            f"format 'csv', header 'true');"
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step7: 初始用户进行file_fdw外表创建; expect:创建成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step8: 系统用户进行file_fdw外表option修改; expect:修改失败----'
        self.log.info(step_txt)
        tb_sql = f"alter foreign table public.{self.tb_fdw} " \
            f"options (set header 'true');"
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step9: 初始用户修改表owner为系统用户; expect:修改成功----'
        self.log.info(step_txt)
        tb_sql = f"alter foreign table public.{self.tb_fdw} " \
            f"owner to {self.u_sys};"
        result = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        self.assertIn(self.constant.alter_foreign_table_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step10: 系统用户再次进行file_fdw外表option修改; expect:修改失败----'
        self.log.info(step_txt)
        tb_sql = f"alter foreign table public.{self.tb_fdw} " \
            f"options (set header 'true');"
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.err_flag1, result, "执行失败" + step_txt)

        step_txt = '----step11: 初始用户进行file_fdw外表option修改; expect:修改成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        self.assertIn(self.constant.alter_foreign_table_success, result,
                      "执行失败" + step_txt)

        step_txt = '----step12: 初始用户进行file_fdw外表结构修改; expect:修改失败----'
        self.log.info(step_txt)
        tb_sql = f"alter foreign table public.{self.tb_fdw} " \
            f"alter column id type char(1000);"
        result = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        self.assertIn(self.err_flag2, result, "执行失败" + step_txt)

        step_txt = '----step13: 初始用户进行file_fdw外表进行增删改; expect:操作失败----'
        self.log.info(step_txt)
        tb_sql = f"insert into public.{self.tb_fdw} values(1,2,3);" \
            f"update public.{self.tb_fdw} set column1 = 3;" \
            f"delete public.{self.tb_fdw} where column1 = 0;"
        result = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        assert_flag = result.count(self.err_flag2)
        self.assertEqual(3, assert_flag, "执行失败" + step_txt)

        step_txt = '----step14: 初始用户进行file_fdw服务(存在外表未删除)删除; expect:删除失败----'
        self.log.info(step_txt)
        svc_sql = f"drop server {self.svc};"
        result = self.pri_sh.execut_db_sql(svc_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIsNotNone(re.findall(self.err_flag3, result),
                             "执行失败" + step_txt)

        step_txt = '----step15: 普通用户进行file_fdw外表删除; expect:删除失败----'
        self.log.info(step_txt)
        tb_sql = f"drop foreign table public.{self.tb_fdw};"
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_com)
        self.log.info(result)
        self.assertIn(self.err_flag3, result, "执行失败" + step_txt)

        step_txt = '----step16: 系统用户进行file_fdw外表删除; expect:删除成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(tb_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step17: 普通用户进行file_fdw服务删除; expect:删除失败----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(svc_sql, sql_type=self.connect_com)
        self.log.info(result)
        self.assertIn(self.err_flag3, result, "执行失败" + step_txt)

        step_txt = '----step18: 系统用户进行file_fdw服务(不存在外表)删除; expect:删除成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(svc_sql, sql_type=self.connect_sys)
        self.log.info(result)
        self.assertIn(self.constant.drop_server_success, result,
                      "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step_txt = '----step:清理数据; expect:清理成功----'
        self.log.info(step_txt)
        drop_sql = f"drop foreign table if exists {self.tb_fdw};" \
            f"drop server if exists {self.svc} cascade;" \
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

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
Case Name   : 使用普通用户指定log errors data
Description :
    1.创建测试表并插入数据
    2.构造数据文件
    3.给文件中插入数据
    4.创建普通用户
    5.使用普通用户对指定log errors data 进行copy from
    6.清理环境
Expect      :
    1.创建测试表并插入数据成功
    2.构造数据文件成功
    3.文件中插入数据成功
    4.创建用户成功
    5.使用普通用户copy失败
    6.清理环境成功
History     :
"""

import unittest
import os

from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class CopyFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_user = Node(node='PrimaryDbUser')
        self.common = Common()
        self.Constant = Constant()
        self.tb_name = 't_copy_111'
        self.file_name = 'testcopy111.dat'
        self.user = 'u_copy_01'
        self.copy_dir_path = os.path.join(macro.DB_INSTANCE_PATH,
                                          'pg_copydir')

    def test_copy_file(self):
        text = '-----step1:创建测试表并对测试表插入数据' \
               'Expect:创建测试表并插入数据成功-----'
        self.log.info(text)
        sql_cmd = f"drop table if exists {self.tb_name};" \
            f"create table {self.tb_name} (sk integer,id varchar(16)," \
            f"name varchar(20),sq_ft integer);"
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_res,
                      '执行失败:' + text)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_res,
                         '执行失败:' + text)
        sql_cmd1 = self.pri_sh.execut_db_sql(
            f"select copy_error_log_create();")
        self.log.info(sql_cmd1)
        self.assertIn('copy_error_log_create', sql_cmd1,
                      '执行失败:' + text)

        text = '-----step2:构造数据文件 Expect:构造数据文件成功-----'
        self.log.info(text)
        excute_cmd = f'''mkdir {self.copy_dir_path};
            touch {os.path.join(self.copy_dir_path, self.file_name)};'''
        self.log.info(excute_cmd)
        msg = self.common.get_sh_result(self.pri_user, excute_cmd)
        self.log.info(msg)
        self.assertEqual(len(msg), 0, '执行失败:' + text)

        text = '-----step3:给文件中插入数据 Expect:文件中插入数据成功-----'
        self.log.info(text)
        excute_cmd = f'echo "001	sk1	tt	3332\n' \
            f'001	sk1	tt	3332\n' \
            f'001	sk1	tt	nnn2" >> ' \
            f'{os.path.join(self.copy_dir_path, self.file_name)};'
        self.log.info(excute_cmd)
        msg = self.common.get_sh_result(self.pri_user, excute_cmd)
        self.log.info(msg)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], msg)

        text = '-----step4:创建普通权限的用户' \
               'Expect:创建用户成功-----'
        self.log.info(text)
        sql_cmd = f'''drop user if exists {self.user} cascade; \
            create user {self.user} password '{macro.COMMON_PASSWD}';'''
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_res,
                      '执行失败:' + text)

        text = '-----step5:使用普通用户对reject与log errors共用进行copy from' \
               'Expect:使用普通用户copy失败-----'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(
            f"copy {self.tb_name} from '"
            f"{os.path.join(self.copy_dir_path, self.file_name)}'"
            f"log errors data reject limit '2';",
            sql_type=f' -U {self.user} -W {macro.COMMON_PASSWD}')
        self.log.info(sql_cmd)
        self.assertIn(' COPY to or from a file is prohibited for ', sql_cmd,
                      '执行失败:' + text)

    def tearDown(self):
        text = '-----step6:清理环境 Expect:清理环境成功-----'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(
            f"drop table if exists {self.tb_name};"
            f"drop table if exists pgxc_copy_error_log;")
        self.log.info(sql_cmd)
        excute_cmd = f'''rm -rf {self.copy_dir_path}'''
        self.log.info(excute_cmd)
        msg = self.common.get_sh_result(self.pri_user, excute_cmd)
        self.log.info(msg)
        self.assertEqual(len(msg), 0, '执行失败:' + text)
        assert_eq = sql_cmd.count('DROP TABLE') is 2
        self.assertTrue(assert_eq, '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

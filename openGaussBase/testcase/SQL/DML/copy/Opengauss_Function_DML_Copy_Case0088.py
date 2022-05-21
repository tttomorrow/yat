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
Case Name   : text/binary/fixed格式数据指定quote进行copy from/to
Description :
    1.创建测试表并插入数据
    2.构造数据文件
    3.text格式数据指定quote进行copy to
    4.text格式数据指定quote进行copy from
    5.binary格式数据指定quote进行copy to
    6.binary格式数据指定quote进行copy from
    7.fixed格式数据指定quote进行copy to
    8.fixed格式数据指定quote进行copy from
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
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class CopyFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)[:-3]}start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_user = Node(node='PrimaryDbUser')
        self.common = Common()
        self.Constant = Constant()
        self.tb_name = 't_copy_88'
        self.file_name = 'testcopy88.csv'
        self.copy_dir_path = os.path.join(macro.DB_INSTANCE_PATH,
                                          'pg_copydir')

    def test_copy_file(self):
        text = '-----step1:创建测试表并对测试表插入数据' \
               'Expect:创建测试表并插入数据成功-----'
        self.log.info(text)
        sql_cmd = f"drop table if exists {self.tb_name};" \
            f"create table {self.tb_name} (sk integer,id varchar(16)," \
            f"name varchar(20),sq_ft integer);" \
            f"insert into {self.tb_name} values (generate_series(1,3)," \
            f"'sk'||generate_series(1,3),'tt'||generate_series(1,3)," \
            f"generate_series(3331,3333));"
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, sql_res,
                      '执行失败:' + text)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_res,
                      '执行失败:' + text)
        self.assertNotIn(self.Constant.SQL_WRONG_MSG[1], sql_res,
                      '执行失败:' + text)

        text = '-----step2:构造数据文件 Expect:构造数据文件成功-----'
        self.log.info(text)
        excute_cmd = f'''mkdir {self.copy_dir_path};
                   touch {os.path.join(self.copy_dir_path, self.file_name)};'''
        self.log.info(excute_cmd)
        msg = self.common.get_sh_result(self.pri_user, excute_cmd)
        self.log.info(msg)
        self.assertEqual(len(msg),  0, '执行失败:' + text)

        text = '-----step3:text格式数据指定quote进行copy to ' \
               'Expect:copy失败-----'
        self.log.info(text)
        sql_cmd = f"copy {self.tb_name} to '" \
            f"{os.path.join(self.copy_dir_path, self.file_name)}'" \
            f" with(format 'text',quote '/');"
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('COPY quote available only in CSV mode', sql_res,
                      '执行失败:' + text)

        text = '-----step4:text格式数据指定quote进行copy from ' \
               'Expect:copy失败-----'
        self.log.info(text)
        sql_cmd = f"copy {self.tb_name} from '" \
            f"{os.path.join(self.copy_dir_path, self.file_name)}'" \
            f" with(format 'text',quote '/');"
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('COPY quote available only in CSV mode', sql_res,
                      '执行失败:' + text)

        text = '-----step5:binary格式数据指定quote进行copy to ' \
               'Expect:copy失败-----'
        self.log.info(text)
        sql_cmd = f"copy {self.tb_name} to '" \
            f"{os.path.join(self.copy_dir_path, self.file_name)}'" \
            f" with(format 'binary',quote '/');"
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('COPY quote available only in CSV mode', sql_res,
                      '执行失败:' + text)

        text = '-----step6:binary格式数据指定quote进行copy from ' \
               'Expect:copy失败-----'
        self.log.info(text)
        sql_cmd = f"copy {self.tb_name} from '" \
            f"{os.path.join(self.copy_dir_path, self.file_name)}'" \
            f" with(format 'binary',quote '/');"
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('COPY quote available only in CSV mode', sql_res,
                      '执行失败:' + text)

        text = '-----step7:fixed格式数据指定quote进行copy to ' \
               'Expect:copy失败-----'
        self.log.info(text)
        sql_cmd = f"copy {self.tb_name} to '" \
            f"{os.path.join(self.copy_dir_path, self.file_name)}'" \
            f" fixed formatter(name(1,3)) quote '/';"
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('COPY quote available only in CSV mode', sql_res,
                      '执行失败:' + text)

        text = '-----step8:fixed格式数据指定quote进行copy from ' \
               'Expect:copy失败-----'
        self.log.info(text)
        sql_cmd = f"copy {self.tb_name} from '" \
            f"{os.path.join(self.copy_dir_path, self.file_name)}'" \
            f"fixed formatter(name(1,3)) quote '/';"
        self.log.info(sql_cmd)
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn('COPY quote available only in CSV mode', sql_res,
                      '执行失败:' + text)

    def tearDown(self):
        text = '-----step9:清理环境 Expect:清理环境成功-----'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(
            f"drop table if exists {self.tb_name};")
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        excute_cmd = f'''rm -rf {self.copy_dir_path}'''
        self.log.info(excute_cmd)
        msg = self.common.get_sh_result(self.pri_user, excute_cmd)
        self.log.info(msg)
        self.assertEqual(len(msg), 0, '执行失败:' + text)
        self.assertIn(self.Constant.TABLE_DROP_SUCCESS, sql_cmd)
        self.log.info(f'-----{os.path.basename(__file__)[:-3]}end-----')










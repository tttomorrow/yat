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
Case Type   : DDL_Create_Directory
Case Name   : 已创建表空间，再创建和表空间同名同路径目录对象，校验是否冲突
Description :
    1.创建表空间
    2.初始用户创建目录对象
    3.删除表空间,删除目录对象
Expect      :
    1.创建表空间成功
    2.创建目录对象成功，与表空间不冲突
    3.删除成功
History     :
"""
import os
import re
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common


class CreateDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.dir_name = 'dir_object_create_directory_0020'
        self.ts_path = 'dir_create_directory_0020'
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH,
                                     'pg_location', self.ts_path)

    def test_create_directory(self):
        text = "-----step1:创建表空间，expect:创建成功-----"
        self.logger.info(text)
        create_cmd = f"create tablespace {self.dir_name} " \
            f"relative location '{self.ts_path}';" \
            f"select * from pg_tablespace;"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS and
                      self.dir_name, create_msg, '执行失败' + text)

        text = "-----step2:初始用户创建目录对象，expect:创建成功,与表空间不冲突-----"
        self.logger.info(text)
        create_cmd = f"create directory {self.dir_name} as '{self.dir_path}';" \
            f"select * from pg_directory;"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)
        expect = f"{self.dir_name} .* 10 .* {self.dir_path} .*"
        search_res = re.search(expect, create_msg.splitlines()[-2], re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)

    def tearDown(self):
        text = "-----step3:删除表空间,删除目录对象，expect:删除成功-----"
        self.logger.info(text)
        drop_cmd = f"drop tablespace {self.dir_name};" \
            f"drop directory {self.dir_name};"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        del_cmd = f"rm -rf {self.dir_path}"
        self.logger.info(del_cmd)
        del_msg = self.userNode.sh(del_cmd).result()
        self.logger.info(del_msg)
        check_dir_cmd = f'''if [ -d {self.dir_path} ];
                            then echo "exists";
                            else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        del_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(del_result)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS and
                      self.constant.DROP_DIRECTORY_SUCCESS_MSG,
                      drop_msg, '执行失败' + text)
        self.assertEqual("not exists", del_result, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
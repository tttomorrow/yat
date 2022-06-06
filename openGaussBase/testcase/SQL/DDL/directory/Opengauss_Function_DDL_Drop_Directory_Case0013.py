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
Case Type   : DDL_Drop_Directory
Case Name   : 使用if exists删除目录对象
Description :
    1.创建目录
    2.初始用户创建目录对象
    3.使用if exists分别删除存在和不存在的目录对象
    4.不使用if exists分别删除存在和不存在的目录对象
    5.删除目录
Expect      :
    1.创建目录成功
    2.创建成功
    3.directory_name存在时删除成功，directory_name不存在时会提示，但不会报错
    4.directory_name存在时删除成功，directory_name不存在时，合理报错
    5.删除成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common


class DropDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.dir_name_1 = 'dir_object_drop_directory_0013_1'
        self.dir_name_2 = 'dir_object_drop_directory_0013_2'
        self.dir_path = os.path.join('/tmp', 'dir_drop_directory_0013')

    def test_drop_directory(self):
        text = '-----step1:创建目录,expect:创建目录成功-----'
        self.logger.info(text)
        mkdir_cmd = f"mkdir {self.dir_path} && ls -ld {self.dir_path}"
        self.logger.info(mkdir_cmd)
        mkdir_msg = self.userNode.sh(mkdir_cmd).result()
        self.logger.info(mkdir_msg)
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                            then echo "exists"; 
                            else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        mkdir_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEquals("exists", mkdir_result, '执行失败' + text)

        text = "-----step2:初始用户创建目录对象，expect:创建成功-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory {self.dir_name_1} " \
            f"as '{self.dir_path}';" \
            f"create or replace directory {self.dir_name_2} " \
            f"as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertEquals(
            create_msg.count(self.constant.CREATE_DIRECTORY_SUCCESS_MSG),
            2, '执行失败' + text)
        sql_cmd = f"select * from pg_directory;"
        sql_msg = self.sh_primary.execut_db_sql(sql_cmd)
        self.logger.info(sql_msg)
        self.assertIn(self.dir_name_1 and self.dir_name_2,
                      sql_msg, '执行失败' + text)

        text = "-----step3:使用if exists分别删除存在和不存在的目录对象，" \
               "expect:directory_name存在时删除成功，" \
               "directory_name不存在时会提示，但不会报错-----"
        self.logger.info(text)
        self.logger.info("-----directory_name存在时删除成功-----")
        drop_cmd = f"drop directory if exists {self.dir_name_1};"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG,
                      drop_msg, '执行失败' + text)
        self.logger.info("-----directory_name不存在时会提示，但不会报错-----")
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertNotIn("ERROR", drop_msg, '执行失败' + text)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG and
                      f'NOTICE:  directory "{self.dir_name_1}" does not exist, '
                      f'skipping', drop_msg, '执行失败' + text)

        text = "-----step4:不使用if exists分别删除存在和不存在的目录对象，" \
               "expect:directory_name 存在时删除成功，" \
               "directory_name不存在时，合理报错-----"
        self.logger.info(text)
        self.logger.info("-----directory_name不存在时合理报错-----")
        drop_cmd = f"drop directory {self.dir_name_1};"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertIn(f'ERROR:  directory "{self.dir_name_1}" does not exist',
                      drop_msg, '执行失败' + text)
        self.logger.info("-----directory_name存在时删除成功-----")
        drop_cmd = f"drop directory {self.dir_name_2};"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG,
                      drop_msg, '执行失败' + text)

    def tearDown(self):
        text = "-----step5:删除目录，expect:删除成功-----"
        self.logger.info(text)
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
        self.assertEquals("not exists", del_result, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
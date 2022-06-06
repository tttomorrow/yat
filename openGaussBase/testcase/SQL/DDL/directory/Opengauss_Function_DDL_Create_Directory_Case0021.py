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
Case Name   : 在目录下创建文件，再创建目录对象，是否对目录进行非空校验
Description :
    1.创建目录
    2.在目录下创建文件
    3.创建目录对象
    4.删除目录对象，删除目录
Expect      :
    1.创建目录成功
    2.创建表空间成功
    3.创建目录对象成功，不进行非空校验
    4.删除成功
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
        self.dir_name = 'dir_object_create_directory_0021'
        self.dir_path = os.path.join('/tmp', 'dir_create_directory_0021')
        self.file_name = os.path.join(self.dir_path,
                                      'file_create_directory_0021.txt')

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
        self.assertEqual("exists", mkdir_result, '执行失败' + text)

    def test_create_directory(self):
        text = "-----step2:在目录下创建文件，expect:创建成功-----"
        self.logger.info(text)
        touch_cmd = f"touch {self.file_name} && " \
            f"ls -ld {self.file_name}"
        self.logger.info(touch_cmd)
        touch_msg = self.userNode.sh(touch_cmd).result()
        self.logger.info(touch_msg)
        self.assertIn(self.file_name, touch_msg, '执行失败' + text)
        content = "Use the create directory statement to " \
                  "create a directory object that defines " \
                  "the alias of a directory on the server file system " \
                  "and is used to store data files used by users."
        self.logger.info(content)
        shell_cmd = f"echo {content} >> {self.file_name};cat {self.file_name}"
        self.logger.info(shell_cmd)
        shell_msg = self.userNode.sh(shell_cmd).result()
        self.logger.info(shell_msg)
        search_res = re.search(content, shell_msg, re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)

        text = "-----step3:创建目录对象，expect:创建成功,不进行非空校验-----"
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
        text = "-----step4:删除目录对象，删除目录;expect:删除成功-----"
        self.logger.info(text)
        drop_cmd = f"drop directory {self.dir_name};"
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
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG,
                      drop_msg, '执行失败' + text)
        self.assertEqual("not exists", del_result, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
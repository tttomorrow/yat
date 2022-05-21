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
Case Name   : directory路径合法性验证，分别测试路径不存在、路径权限不足的情况和目录属主为root的情况
Description :
    1.创建目录
    2.初始用户创建目录对象，路径不存在
    3.初始用户创建目录对象，路径权限不足
    4.目录属主为root，初始化用户权限赋予读/写/执行权限，创建目录对象
    5.目录属主为root，初始化用户无读/写/执行权限，创建目录对象
    6.初始用户创建目录对象，有读/写/执行权限
    7.删除目录
Expect      :
    1.创建目录成功
    2.创建成功，提示风险
    3.创建成功，提示风险
    4.创建成功
    5.创建成功，提示风险
    6.创建成功
    7.删除目录成功
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
        self.rootNode = Node('PrimaryRoot')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.dir_path_1 = os.path.join('/tmp', 'dir_create_directory_0013_01')
        self.dir_path_2 = os.path.join('/tmp', 'dir_create_directory_0013_02')
        self.dir_path_not_exists = os.path.join('/tmp',
                                                'dir_create_directory_0013_03')
        self.dir_name_1 = 'u_create_directory_0013_01'
        self.dir_name_2 = 'u_create_directory_0013_02'
        self.dir_name_3 = 'u_create_directory_0013_03'
        self.dir_name_4 = 'u_create_directory_0013_04'
        self.dir_name_5 = 'u_create_directory_0013_05'

        text = '-----step1:创建目录,expect:创建目录成功-----'
        self.logger.info(text)
        self.logger.info("-----初始用户用户创建目录;expect:创建成功-----")
        mkdir_cmd = f"mkdir {self.dir_path_1} && ls -ld {self.dir_path_1}"
        self.logger.info(mkdir_cmd)
        mkdir_msg = self.userNode.sh(mkdir_cmd).result()
        self.logger.info(mkdir_msg)
        check_dir_cmd = f'''if [ -d {self.dir_path_1} ]; 
                    then echo "exists"; 
                    else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        mkdir_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEqual("exists", mkdir_result, '执行失败' + text)
        self.logger.info("-----root用户创建目录;expect:创建成功-----")
        mkdir_cmd = f"mkdir {self.dir_path_2}"
        self.logger.info(mkdir_cmd)
        mkdir_msg = self.rootNode.sh(mkdir_cmd).result()
        self.logger.info(mkdir_msg)
        check_dir_cmd = f'''if [ -d {self.dir_path_2} ]; 
                           then echo "exists"; 
                           else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        mkdir_result = self.rootNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEqual("exists", mkdir_result, '执行失败' + text)

    def test_create_directory(self):
        text = "-----step2:初始用户创建目录对象，路径不存在;" \
               "expect:创建成功，提示风险-----"
        self.logger.info(text)
        create_cmd = f"create directory {self.dir_name_1} " \
            f"as '{self.dir_path_not_exists}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG and
                      f"WARNING:  could not get \"{self.dir_path_not_exists}\" "
                      f"status, directory does not exist, "
                      f"must make sure directory existance before using",
                      create_msg, '执行失败' + text)

        text = "-----step3:初始用户创建目录对象，路径权限不足;" \
               "expect:创建成功，提示风险-----"
        self.logger.info(text)
        chmod_cmd = f"chmod -R 600 {self.dir_path_1} && " \
            f"ls -ld {self.dir_path_1}"
        self.logger.info(chmod_cmd)
        chmod_msg = self.userNode.sh(chmod_cmd).result()
        self.logger.info(chmod_msg)
        expect = f"drw------- .* {self.userNode.ssh_user} .* {self.dir_path_1}"
        search_res = re.search(expect, chmod_msg, re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)
        create_cmd = f"create directory {self.dir_name_2} " \
            f"as '{self.dir_path_1}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG and
                      "do not have full permissions (Read/Write/Exec)",
                      create_msg, '执行失败' + text)

        text = "-----step4:目录属主为root，初始化用户无读/写/执行权限，" \
               "创建目录对象;expect:创建成功，提示风险-----"
        self.logger.info(text)
        shell_cmd = f"chmod -R 700 {self.dir_path_2} && " \
            f"ls -ld {self.dir_path_2}"
        self.logger.info(shell_cmd)
        shell_msg = self.rootNode.sh(shell_cmd).result()
        self.logger.info(shell_msg)
        expect = f".*drwx------ .* root root .* {self.dir_path_2}.*"
        search_res = re.search(expect, shell_msg, re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)
        create_cmd = f"create directory {self.dir_name_3} " \
            f"as '{self.dir_path_2}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG and
                      "do not have full permissions (Read/Write/Exec)",
                      create_msg, '执行失败' + text)

        text = "-----step5:目录属主为root，初始化用户赋予读/写/执行权限，" \
               "创建目录对象;expect:创建成功-----"
        self.logger.info(text)
        chmod_cmd = f"chmod o+rwx {self.dir_path_2} && " \
            f"ls -ld {self.dir_path_2}"
        chmod_result = self.rootNode.sh(chmod_cmd).result()
        self.logger.info(chmod_result)
        expect = f"drwx---rwx .* root root .* {self.dir_path_2}"
        search_res = re.search(expect, chmod_result, re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)
        create_cmd = f"create directory {self.dir_name_4} " \
            f"as '{self.dir_path_2}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step6:初始用户创建目录对象，有读/写/执行权限;" \
               "expect:创建成功-----"
        self.logger.info(text)
        chmod_cmd = f"chmod -R 700 {self.dir_path_1} && " \
            f"ls -ld {self.dir_path_1}"
        chmod_msg = self.userNode.sh(chmod_cmd).result()
        self.logger.info(chmod_msg)
        expect = f"drwx------ .* {self.userNode.ssh_user} .* {self.dir_path_1}"
        search_res = re.search(expect, chmod_msg, re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)
        create_cmd = f"create directory {self.dir_name_5} " \
            f"as '{self.dir_path_1}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

    def tearDown(self):
        text = "-----step10:删除目录对象，expect:删除成功-----"
        self.logger.info(text)
        drop_cmd = f'''drop directory {self.dir_name_1}; 
            drop directory {self.dir_name_2}; 
            drop directory {self.dir_name_3}; 
            drop directory {self.dir_name_4}; 
            drop directory {self.dir_name_5};'''
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        del_cmd = f"rm -rf {self.dir_path_1} {self.dir_path_2}"
        self.logger.info(del_cmd)
        del_msg = self.rootNode.sh(del_cmd).result()
        self.logger.info(del_msg)
        check_dir_cmd = f''' if [ -d {self.dir_path_1} ]; 
            then echo "exists"; 
            else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        del_result_1 = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(del_result_1)
        check_dir_cmd = f''' if [ -d {self.dir_path_2} ]; 
                    then echo "exists"; 
                    else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        del_result_2 = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(del_result_2)
        self.assertEquals(
            drop_msg.count(self.constant.DROP_DIRECTORY_SUCCESS_MSG),
            5, '执行失败' + text)
        self.assertEqual("not exists", del_result_1, '执行失败' + text)
        self.assertEqual("not exists", del_result_2, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
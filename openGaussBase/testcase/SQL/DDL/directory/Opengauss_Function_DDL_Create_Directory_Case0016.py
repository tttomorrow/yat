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
Case Name   : 查询系统表pg_directory，select * 查询少了oid字段
Description :
    1.创建目录
    2.初始用户创建目录对象
    3.通过系统表查看目录信息
    4.删除目录
Expect      :
    1.创建目录成功
    2.初始用户创建目录对象成功，返回CREATE DIRECTORY
    3.select * 查询少了oid字段
    4.删除目录成功
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
        self.user_name = 'u_create_directory_0016'
        self.dir_name = 'dir_object_create_directory_0016'
        self.dir_path = os.path.join('/tmp', 'dir_create_directory_0016')

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
        text = "-----step2:初始用户创建目录对象，" \
               "expect:创建成功，返回CREATE DIRECTORY-----"
        self.logger.info(text)
        create_cmd = f"create directory {self.dir_name} as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step3:通过系统表查看目录信息，" \
               "expect:select * 查询少了oid字段-----"
        self.logger.info(text)
        sql_cmd = f"select oid,dirname,owner,dirpath,diracl from pg_directory;"
        sql_msg = self.sh_primary.execut_db_sql(sql_cmd)
        self.logger.info(sql_msg)
        expect = f"oid .* dirname .* owner .* dirpath .* diracl"
        search_res = re.search(expect, sql_msg.splitlines()[0], re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)
        self.assertIn(self.dir_name and self.dir_path and '10',
                      sql_msg.splitlines()[-2], '执行失败' + text)
        sql_cmd = f"select * from pg_directory;"
        sql_msg = self.sh_primary.execut_db_sql(sql_cmd)
        self.logger.info(sql_msg)
        expect = f"dirname .* owner .* dirpath .* diracl"
        search_res = re.search(expect, sql_msg.splitlines()[0], re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)
        self.assertIn(self.dir_name and self.dir_path and '10',
                      sql_msg.splitlines()[-2], '执行失败' + text)

    def tearDown(self):
        text_5 = "-----step4:删除目录，expect:删除成功-----"
        self.logger.info(text_5)
        drop_user = f"drop directory {self.dir_name};"
        drop_msg = self.sh_primary.execut_db_sql(drop_user)
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
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
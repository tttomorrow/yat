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
Case Name   : 使用replace创建目录对象
Description :
    1.创建目录
    2.初始用户使用replace创建不存在和已存在的目录对象
    3.初始用户不使用replace创建不存在和已存在的目录对象
    4.删除目录对象，删除目录
Expect      :
    1.创建目录成功
    2.创建目录对象成功
    3.创建不存在的目录对象成功，创建已存在的目录对象失败，合理报错
    4.删除成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class CreateDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.dir_name_1 = 'dir_object_create_directory_0017_1'
        self.dir_name_2 = 'dir_object_create_directory_0017_2'
        self.dir_path_1 = os.path.join('/tmp', 'dir_create_directory_0017_1')
        self.dir_path_2 = os.path.join('/tmp', 'dir_create_directory_0017_2')

    def test_create_directory(self):
        text = '-----step1:创建目录,expect:创建目录成功-----'
        self.logger.info(text)
        mkdir_cmd = f"mkdir {self.dir_path_1} {self.dir_path_2} && " \
            f"ls -ld {self.dir_path_1} && ls -ld {self.dir_path_2}"
        self.logger.info(mkdir_cmd)
        mkdir_msg = self.userNode.sh(mkdir_cmd).result()
        self.logger.info(mkdir_msg)
        check_dir_cmd = f'''
            if [[ -e {self.dir_path_1} && -e {self.dir_path_2} ]];  
            then echo "exists"; else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        mkdir_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEquals("exists", mkdir_result, '执行失败' + text)

        text = "-----step2:初始用户使用replace创建不存在和已存在的目录对象，" \
               "expect:创建成功-----"
        self.logger.info(text)
        self.logger.info("-----创建不存在的目录对象，expect:创建成功-----")
        create_cmd = f"create or replace directory {self.dir_name_1} " \
            f"as '{self.dir_path_1}';" \
            f"select * from pg_directory " \
            f"where dirname like '{self.dir_name_1}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg.splitlines()[0], '执行失败' + text)
        self.assertIn(self.dir_name_1 and '10' and self.dir_path_1,
                      create_msg.splitlines()[-2], '执行失败' + text)

        self.logger.info("-----创建已存在的目录对象，expect:创建成功，替换为新路径-----")
        create_cmd = f"create or replace directory {self.dir_name_1} " \
            f"as '{self.dir_path_2}';" \
            f"select * from pg_directory " \
            f"where dirname like '{self.dir_name_1}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg.splitlines()[0], '执行失败' + text)
        self.assertIn(self.dir_name_1 and '10' and self.dir_path_2,
                      create_msg.splitlines()[-2], '执行失败' + text)

        text = "-----step3:初始用户不使用replace创建不存在和已存在的目录对象，" \
               "expect:创建不存在的目录对象成功，创建已存在的目录对象失败，合理报错-----"
        self.logger.info(text)
        self.logger.info("-----创建不存在的目录对象，expect:创建成功-----")
        create_cmd = f"create directory {self.dir_name_2} " \
            f"as '{self.dir_path_1}';" \
            f"select * from pg_directory " \
            f"where dirname like '{self.dir_name_2}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg.splitlines()[0], '执行失败' + text)
        self.assertIn(self.dir_name_2 and '10' and self.dir_path_1,
                      create_msg.splitlines()[-2], '执行失败' + text)

        self.logger.info("-----创建已存在的目录对象，expect:创建失败，合理报错-----")
        create_cmd = f"create directory {self.dir_name_2} " \
            f"as '{self.dir_path_2}';" \
            f"select * from pg_directory " \
            f"where dirname like '{self.dir_name_2}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(f'ERROR:  directory "{self.dir_name_2}" is '
                      f'already used by an existing object',
                      create_msg, '执行失败' + text)
        self.assertIn(self.dir_name_2 and '10' and self.dir_path_1,
                      create_msg.splitlines()[-2], '执行失败' + text)

    def tearDown(self):
        text = "-----step4:删除目录对象，删除目录，expect:删除成功-----"
        self.logger.info(text)
        drop_cmd = f"drop directory {self.dir_name_1};" \
            f"drop directory {self.dir_name_2};"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        del_cmd = f"rm -rf {self.dir_path_1} {self.dir_path_2}"
        self.logger.info(del_cmd)
        del_msg = self.userNode.sh(del_cmd).result()
        self.logger.info(del_msg)
        check_dir_cmd = f'''
            if [[ -e {self.dir_path_1} && -e {self.dir_path_2} ]];  
            then echo "exists"; else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        del_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(del_result)
        self.assertEquals(
            2, drop_msg.count(self.constant.DROP_DIRECTORY_SUCCESS_MSG),
            '执行失败' + text)
        self.assertEquals("not exists", del_result, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
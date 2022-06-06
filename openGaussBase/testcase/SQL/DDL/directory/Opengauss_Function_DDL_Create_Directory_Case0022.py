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
Case Name   : 主备节点路径一致性验证
Description :
    1.创建目录
    2.主节点存在路径，备节点不存在路径,创建目录对象
    3.备节点存在路径，但权限不足，创建目录对象
    4.删除目录对象，删除目录
Expect      :
    1.创建目录成功
    2.创建成功
    3.创建成功
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

primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == primary_sh.get_node_num(), '单机环境不执行')
class CreateDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.standbyNode = Node('Standby1DbUser')
        self.constant = Constant()
        self.common = Common()
        self.dir_name_1 = 'dir_object_create_directory_0022_01'
        self.dir_name_2 = 'dir_object_create_directory_0022_02'
        self.dir_path = os.path.join('/tmp', 'dir_create_directory_0022')

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

    def test_create_directory(self):
        text = "-----step2:主节点存在路径，备节点不存在路径，" \
               "创建目录对象;expect:创建成功-----"
        self.logger.info(text)
        create_cmd = f"create directory {self.dir_name_1} " \
            f"as '{self.dir_path}';" \
            f"select * from pg_directory;"
        create_msg = primary_sh.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)
        expect = f"{self.dir_name_1} .* 10 .* {self.dir_path} .*"
        search_res = re.search(expect, create_msg.splitlines()[-2], re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)

        text = "-----step3:备节点存在路径，但权限不足，创建目录对象，" \
               "expect:创建成功-----"
        self.logger.info(text)
        mkdir_cmd = f"mkdir {self.dir_path}"
        self.standbyNode.sh(mkdir_cmd).result()
        check_dir_cmd = f'''if [ -d {self.dir_path} ];  
            then echo "exists"; else echo "not exists"; fi'''
        mkdir_result = self.standbyNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEquals("exists", mkdir_result, '执行失败' + text)
        create_cmd = f"create directory {self.dir_name_2} " \
            f"as '{self.dir_path}';" \
            f"select * from pg_directory;"
        create_msg = primary_sh.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)
        expect = f"{self.dir_name_2} .* 10 .* {self.dir_path} .*"
        search_res = re.search(expect, create_msg.splitlines()[-2], re.S)
        self.assertIsNotNone(search_res, '执行失败' + text)

    def tearDown(self):
        text = "-----step4:删除目录对象，删除目录;expect:删除成功-----"
        self.logger.info(text)
        drop_cmd = f"drop directory {self.dir_name_1};" \
            f"drop directory {self.dir_name_2};"
        drop_msg = primary_sh.execut_db_sql(drop_cmd)
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
        self.assertEquals("not exists", del_result, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
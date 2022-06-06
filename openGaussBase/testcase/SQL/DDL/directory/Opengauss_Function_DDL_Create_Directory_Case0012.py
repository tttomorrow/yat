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
Case Name   : directory_name标识符的命名规范验证
Description :
    1.创建目录
    2.初始用户创建目录对象，目录名含特殊字符
    3.初始用户创建目录对象，目录名为纯数字和纯数字字符串
    4.初始用户创建目录对象，目录名为空
    5.初始用户创建目录对象，目录名含中文
    6.初始用户创建目录对象，命名为数据库保留关键字
    7.初始用户创建目录对象，命名为数据库非保留关键字
    8.初始用户创建目录对象，命名含大写字母
    9.查询目录信息
    10.删除目录对象
Expect      :
    1.创建目录成功
    2.目录名含特殊字符@,*创建失败，合理报错
     目录名含特殊字符#,$创建成功
    3.创建目录名为纯数字的目录对象失败，合理报错
     创建目录名为纯数字的字符串的目录对象成功
    4.创建失败，合理报错
    5.创建成功
    6.创建失败，合理报错
    7.创建成功
    8.创建成功，忽略大小写
    9.查询目录信息正确
    10.删除目录成功
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
        self.dir_path = os.path.join('/tmp', 'dir_create_directory_0012')

        text = '-----step1:创建目录,expect:创建目录成功-----'
        self.logger.info(text)
        mkdir_cmd = f"mkdir {self.dir_path}"
        self.userNode.sh(mkdir_cmd).result()
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                    then echo "exists"; 
                    else echo "not exists"; fi'''
        mkdir_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEquals("exists", mkdir_result, '执行失败' + text)

    def test_create_directory(self):
        text = "-----step2:初始用户创建目录对象，目录名含特殊字符;" \
               "expect:目录名含特殊字符@,*创建失败，合理报错;" \
               "目录名含特殊字符#,$创建成功-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory dir@object0012 " \
            f"as '{self.dir_path}';" \
            f"create or replace directory dir*object0012 as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertEquals(create_msg.count(self.constant.SYNTAX_ERROR_MSG),
                          2, '执行失败' + text)
        create_cmd = f"create or replace directory dir\\$object0012 " \
            f"as '{self.dir_path}';" \
            f"create or replace directory dir#object0012 as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step3:初始用户创建目录对象，目录名为纯数字和纯数字字符串;" \
               "expect:创建目录名为纯数字的目录对象失败，合理报错;" \
               "创建目录名为纯数字的字符串的目录对象成功-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory 0012 as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG,
                      create_msg, '执行失败' + text)
        create_cmd = f"create or replace directory \\\"0012\\\" " \
            f"as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step4:初始用户创建目录对象，目录名为空;" \
               "expect:创建失败，合理报错-----"
        self.logger.info(text)
        create_cmd = f'''create or replace directory   as '{self.dir_path}';
            create or replace directory \\\"\\\" as '{self.dir_path}';'''
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG,
                      create_msg.splitlines()[0], '执行失败' + text)
        self.assertIn("ERROR:  zero-length delimited identifier",
                      create_msg.splitlines()[-3], '执行失败' + text)

        text = "-----step5:初始用户创建目录对象，目录名含中文;expect:创建成功-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory 目录0012 " \
            f"as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step6:初始用户创建目录对象，命名为数据库保留关键字;" \
               "expect:创建失败，合理报错-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory case as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step7:初始用户创建目录对象，命名为数据库非保留关键字;" \
               "expect:创建成功-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory directory " \
            f"as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step8:初始用户创建目录对象，命名含大写字母;" \
               "expect:创建成功-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory dir_OBJECT_0012 " \
            f"as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step9:通过系统表查看目录信息，expect:目录信息正确-----"
        self.logger.info(text)
        sql_cmd = f"select oid,dirname,owner,dirpath,diracl from pg_directory;"
        sql_msg = self.sh_primary.execut_db_sql(sql_cmd)
        self.logger.info(sql_msg)
        self.assertIn('dir\\$object0012' and 'object0012' and '0012'
                      and '目录0012' and 'directory' and 'dir_object_0012',
                      sql_msg, '执行失败' + text)

    def tearDown(self):
        text = "-----step10:删除目录对象，expect:删除成功-----"
        self.logger.info(text)
        drop_cmd = f'''drop directory dir\\$object0012; 
            drop directory dir#object0012; 
            drop directory \\\"0012\\\"; 
            drop directory 目录0012; 
            drop directory directory;
            drop directory dir_object_0012;'''
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        del_cmd = f"rm -rf {self.dir_path}"
        self.userNode.sh(del_cmd).result()
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                            then echo "exists"; 
                            else echo "not exists"; fi'''
        del_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(del_result)
        self.assertEquals(
            drop_msg.count(self.constant.DROP_DIRECTORY_SUCCESS_MSG),
            6, '执行失败' + text)
        self.assertEquals("not exists", del_result, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
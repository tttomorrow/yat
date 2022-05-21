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
Case Type   : DDL_Alter_Directory
Case Name   : 修改不合法的目录，合理报错
Description :
    1.创建用户
    2.修改不存在的目录
    3.修改命名包含特殊字符@*等的目录
    4.修改命名为空的目录
    5.修改命名为纯数字的目录
    6.修改命名为数据库保留关键字的目录
    7.删除用户
Expect      :
    1.创建成功
    2.修改失败，合理报错，目录对象不存在
    3.先校验语法，合理报错:syntax error at or near
    4.无directory_name时报语法错误syntax error at or near，
      directory_name为空字符串时报错zero-length delimited identifier
    5.先校验语法，合理报错:syntax error at or near
    6.先校验语法，合理报错:syntax error at or near
    7.删除成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class AlterDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.user_name = 'u_alter_directory_0004'

    def test_alter_directory(self):
        text = "-----step1:创建用户，expect:创建成功-----"
        self.logger.info(text)
        create_user = f"drop user if exists {self.user_name};" \
            f"create user {self.user_name} " \
            f"sysadmin password '{macro.COMMON_PASSWD}';"
        create_msg = self.sh_primary.execut_db_sql(create_user)
        self.logger.info(create_msg)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG and
                      self.constant.CREATE_ROLE_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step2:修改不存在的目录，" \
               "expect:修改失败，合理报错，目录对象不存在-----"
        self.logger.info(text)
        alter_cmd = f"alter directory dir_alter_directory_0004 " \
            f"owner to {self.user_name};"
        alter_msg = self.sh_primary.execut_db_sql(alter_cmd)
        self.logger.info(alter_msg)
        self.assertIn("ERROR:  directory \"dir_alter_directory_0004\" "
                      "does not exist", alter_msg, '执行失败' + text)

        text = "-----step3:修改命名包含特殊字符@*等的目录，" \
               "expect:先校验语法，合理报错:syntax error at or near-----"
        self.logger.info(text)
        alter_cmd = f"alter directory dir@alter_directory_0004 " \
            f"owner to {self.user_name};" \
            f"alter directory dir*alter_directory_0004 " \
            f"owner to {self.user_name};"
        alter_msg = self.sh_primary.execut_db_sql(alter_cmd)
        self.logger.info(alter_msg)
        self.assertEquals(2, alter_msg.count(self.constant.SYNTAX_ERROR_MSG),
                          '执行失败' + text)

        text = "-----step4:修改命名为空的目录，expect:无directory_name时" \
               "报语法错误syntax error at or near，directory_name为空字符串时" \
               "报错zero-length delimited identifier-----"
        self.logger.info(text)
        alter_cmd = f"alter directory  owner to {self.user_name};"
        alter_msg = self.sh_primary.execut_db_sql(alter_cmd)
        self.logger.info(alter_msg)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG,
                      alter_msg, '执行失败' + text)
        alter_cmd = f"alter directory \\\"\\\" owner to {self.user_name};"
        alter_msg = self.sh_primary.execut_db_sql(alter_cmd)
        self.logger.info(alter_msg)
        self.assertIn("ERROR:  zero-length delimited identifier",
                      alter_msg, '执行失败' + text)

        text = "-----step5:修改命名为纯数字的目录，" \
               "expect:先校验语法，合理报错:syntax error at or near-----"
        self.logger.info(text)
        alter_cmd = f"alter directory 0004 owner to {self.user_name};"
        alter_msg = self.sh_primary.execut_db_sql(alter_cmd)
        self.logger.info(alter_msg)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG,
                      alter_msg, '执行失败' + text)

        text = "-----step6:修改命名为数据库保留关键字的目录，" \
               "expect:先校验语法，合理报错:syntax error at or near-----"
        self.logger.info(text)
        alter_cmd = f"alter directory case owner to {self.user_name};"
        alter_msg = self.sh_primary.execut_db_sql(alter_cmd)
        self.logger.info(alter_msg)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG,
                      alter_msg, '执行失败' + text)

    def tearDown(self):
        text = "-----step7:删除用户，expect:删除成功-----"
        self.logger.info(text)
        drop_user = f"drop user {self.user_name};"
        drop_msg = self.sh_primary.execut_db_sql(drop_user)
        self.logger.info(drop_msg)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG,
                      drop_msg, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
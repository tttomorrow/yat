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
Case Name   : 初始用户删除不符合规范的directory_name，合理报错
Description :
    1.初始用户删除不存在的目录对象
    2.删除命名包含特殊字符@*等的目录对象
    3.删除命名为空的目录对象
    4.删除命名为纯数字的目录对象
    5.删除命名为数据库保留关键字的目录对象
Expect      :
    1.删除失败，合理报错
    2.删除失败，合理报错
    3.删除失败，合理报错
    4.删除失败，合理报错
    5.删除失败，合理报错
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

    def test_drop_directory(self):
        text = "-----step1:初始用户删除不存在的目录对象，expect:删除失败，合理报错-----"
        self.logger.info(text)
        drop_cmd = f"drop directory dir_object_drop_directory_0010;"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertIn('ERROR:  directory "dir_object_drop_directory_0010" '
                      'does not exist', drop_msg, '执行失败' + text)

        text = "-----step2:删除命名包含特殊字符@*等的目录对象，" \
               "expect:删除失败，合理报错-----"
        self.logger.info(text)
        drop_cmd = f"drop directory dir@object_drop_directory_0010;" \
            f"drop directory dir*object_drop_directory_0010;"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertEquals(2, drop_msg.count(self.constant.SYNTAX_ERROR_MSG),
                          '执行失败' + text)

        text = "-----step3:删除命名为空目录的目录对象，expect:删除失败，合理报错-----"
        self.logger.info(text)
        drop_cmd = f"drop directory ;" \
            f"drop directory '';"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertEquals(2, drop_msg.count(self.constant.SYNTAX_ERROR_MSG),
                          '执行失败' + text)

        text = "-----step4:删除命名为纯数字的目录对象，expect:删除失败，合理报错-----"
        self.logger.info(text)
        drop_cmd = f"drop directory 0010;"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, drop_msg, '执行失败' + text)

        text = "-----step5:删除命名为数据库保留关键字的目录对象，" \
               "expect:删除失败，合理报错-----"
        self.logger.info(text)
        drop_cmd = f"drop directory case;"
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertIn(self.constant.SYNTAX_ERROR_MSG, drop_msg, '执行失败' + text)

    def tearDown(self):
        self.logger.info("-----无需清理环境-----")
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
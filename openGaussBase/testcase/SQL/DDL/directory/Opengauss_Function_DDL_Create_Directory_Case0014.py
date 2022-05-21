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
Case Name   : enable_access_server_directory参数取值验证
Description :
    1.修改guc参数enable_access_server_directory的值包含特殊字符
    2.修改guc参数enable_access_server_directory的值为其它字母
    3.修改guc参数enable_access_server_directory的值为空
    4.修改guc参数enable_access_server_directory的值为除1和0之外的其它数字
    5.修改guc参数enable_access_server_directory的值为1和0
    6.修改guc参数enable_access_server_directory的值为true和false
    7.修改guc参数enable_access_server_directory的值为on和off
    8.使用-c "enable_access_server_directory"的方式恢复默认参数
Expect      :
    1.修改guc参数失败,合理报错
    2.修改guc参数失败,合理报错
    3.修改guc参数失败,合理报错
    4.修改guc参数失败,合理报错
    5.修改guc参数成功
    6.修改guc参数成功
    7.修改guc参数成功
    8.恢复默认参数成功
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


class CreateDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.config_directory = 'enable_access_server_directory'
        self.check_default = self.common.show_param(self.config_directory)

    def test_create_directory(self):
        text = "-----step1:修改guc参数enable_access_server_directory的值" \
               "包含特殊字符，expect:修改guc参数失败,合理报错-----"
        self.logger.info(text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f'{self.config_directory}=$on',
                                               get_detail=True)
        self.logger.info(result)
        self.assertIn("exists illegal character", result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, self.check_default, '执行失败' + text)

        text = "-----step2:修改guc参数enable_access_server_directory的值" \
               "为其它字母，expect:修改guc参数失败,合理报错-----"
        self.logger.info(text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f'{self.config_directory}=aa',
                                               get_detail=True)
        self.logger.info(result)
        self.assertIn(f'ERROR: The value "aa" for parameter '
                      f'"{self.config_directory}" is incorrect, '
                      f'requires a boolean value', result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, self.check_default, '执行失败' + text)

        text = "-----step3:修改guc参数enable_access_server_directory的值" \
               "为空字符串，expect:修改guc参数失败,合理报错-----"
        self.logger.info(text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f"{self.config_directory}=''",
                                               get_detail=True)
        self.logger.info(result)
        self.assertIn(f'ERROR: The value "\'\'" for parameter '
                      f'"{self.config_directory}" is incorrect, '
                      f'requires a boolean value', result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, self.check_default, '执行失败' + text)

        text = "-----step4:修改guc参数enable_access_server_directory的值" \
               "为除1和0之外的其它数字，expect:修改guc参数失败,合理报错-----"
        self.logger.info(text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f"{self.config_directory}='5'",
                                               get_detail=True)
        self.logger.info(result)
        self.assertIn(f'ERROR: The value "\'5\'" for parameter '
                      f'"{self.config_directory}" is incorrect, '
                      f'requires a boolean value', result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, self.check_default, '执行失败' + text)

        text = "-----step5:修改guc参数enable_access_server_directory的值" \
               "为1和0，expect:修改guc参数成功-----"
        self.logger.info(text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f"{self.config_directory}='1'")
        self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'on', '执行失败' + text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f"{self.config_directory}='0'")
        self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'off', '执行失败' + text)

        text = "-----step6:修改guc参数enable_access_server_directory的值" \
               "为true和false，expect:修改guc参数成功-----"
        self.logger.info(text)
        result = self.sh_primary.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            f"{self.config_directory}='true'")
        self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'on', '执行失败' + text)
        result = self.sh_primary.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            f"{self.config_directory}='false'")
        self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'off', '执行失败' + text)

        text = "-----step7:修改guc参数enable_access_server_directory的值" \
               "为on和off，expect:修改guc参数成功-----"
        self.logger.info(text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f"{self.config_directory}='on'")
        self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'on', '执行失败' + text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f"{self.config_directory}='off'")
        self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'off', '执行失败' + text)

        text = '-----step7:使用-c "enable_access_server_directory"的方式' \
               '恢复默认参数，expect:恢复默认参数成功-----'
        self.logger.info(text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f"{self.config_directory}='on'")
        self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'on', '执行失败' + text)
        result = self.sh_primary.execute_gsguc('reload',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               f"{self.config_directory}")
        self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'off', '执行失败' + text)

    def tearDown(self):
        self.logger.info("-----恢复参数-----")
        current = self.common.show_param(self.config_directory)
        if self.check_default != current:
            self.guc_result = self.sh_primary.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_directory}={self.check_default}')
        show_msg = self.common.show_param(self.config_directory)
        self.assertEquals(show_msg, self.check_default, '恢复参数失败')
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
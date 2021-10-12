"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : 服务端工具
Case Name   : 检查操作系统版本，内核版本,Unicode状态,时区状态,交换内存状态,
              系统控制参数,文件系统配置状态,磁盘配置状态,预读块大小状态,IO
              调度状态,网卡配置状态,时间一致性
Description :
    检查操作系统版本，内核版本,Unicode状态,时区状态,交换内存状态,
    系统控制参数,文件系统配置状态,磁盘配置状态,预读块大小状态,
    IO调度状态,网卡配置状态,时间一致性
Expect      :
    检查完成
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Tools_gs_checkos_Case0070start---')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools(self):
        logger.info('----------root用户检查操作系统版本，内核版本,Unicode\
状态,时区状态,交换内存状态,系统控制参数,文件系统配置状态,磁盘配置状态,预读块\
大小状态,IO调度状态,网卡配置状态,时间一致性-----------')
        checkos_cmd = f'''
                    source {macro.DB_ENV_PATH}
                    gs_checkos -i  A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12
                            '''
        logger.info(checkos_cmd)
        msg = self.rootNode.sh(checkos_cmd).result()
        logger.info(msg)
        logger.info('--------------解析执行结果---------------')
        str_1 = msg.splitlines()
        logger.info(str_1)
        status_list = []
        num_list = []
        logger.info('--------------提取选项信息---------------')
        for i in str_1:
            if '[' in i and ']' in i:
                num_list.append(i.split('.')[0].strip())
        logger.info(num_list)
        logger.info('--------------提取状态信息---------------')
        for j in str_1:
            if '[' in j and ']' in j:
                status_list.append(j.split(':')[-1].strip())
        logger.info(status_list)

        logger.info('---断言，判断选项信息是否正确，判断状态信息是否正常---')
        self.assertEqual(len(num_list), 12)
        self.assertIn(num_list[0], self.Constant.GS_CHECKOS_SUCCESS_MSG1)
        self.assertEqual(len(status_list), 12)
        for i in status_list:
            self.assertTrue(i in ['Normal', 'Warning'], f'状态验证\
失败，当前状态：{i}')

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('--Opengauss_Function_Tools_gs_checkos_Case0070finish--')

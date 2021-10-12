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
Case Name   : 检查操作系统信息时指定主机名称，指定日志文件及存放路径，并显示检查结果详情
Description :
    1.检查操作系统信息时指定主机名称，指定日志文件及存放路径，并显示检查结果详情
    2.查看文件内容，分析主机状态
Expect      :
    1.检查成功
    2.查看文件成功，主机状态正确
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.root_user = Node('default')
        self.primary_dbuser = Node('PrimaryDbUser')

    def test_server_tools1(self):
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0058开始-')
        self.log.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname)

        self.log.info('-检查操作系统信息时指定主机名称，指定日志文件及存放路径，并显示检查结果详情-')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8  -h {hostname} -o /home/tmp.log --detail'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_user.sh(checkos_cmd).result()
        self.log.info(checkos_msg)

        self.log.info('-----查看tmp.log文件内容，分析检查结果-----')
        check_cmd = f'cat /home/tmp.log'
        self.log.info(check_cmd)
        cat_msg = self.root_user.sh(check_cmd).result()
        self.log.info(cat_msg)
        list1 = cat_msg.split('\n')
        self.log.info(list1)
        list2 = list1[1].split(':')
        self.log.info(list2)
        self.assertEqual(list2[0].strip(),
            'A8. [ Disk configuration status ]', '状态异常')
        i = list2[1].strip()
        self.assertTrue(i in ['Normal', 'Warning'], f'状态异常: {i}')

    def tearDown(self):
        self.log.info('-----------------清理环境----------------')
        rm_cmd = f'rm -rf /home/tmp.log'
        self.log.info(rm_cmd)
        rm_msg = self.root_user.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('-Opengauss_Function_Tools_gs_checkos_Case0058结束-')

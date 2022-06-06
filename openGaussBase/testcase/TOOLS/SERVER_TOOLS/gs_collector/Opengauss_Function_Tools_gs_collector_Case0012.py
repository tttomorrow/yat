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
Case Type   : 服务端工具
Case Name   : 收集日志信息时指定主机名称
Description :
    1.收集日志信息时指定主机名称
    2.清理环境
Expect      :
    1.收集日志信息成功
    2.清理环境
History     :
"""
import os
import unittest
import time
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.primary_dbuser = Node('PrimaryDbUser')
        self.root_node = Node('PrimaryRoot')
        self.constant = Constant()
        self.tmp_dir_path = os.path.join(os.path.dirname(macro.PG_LOG_PATH))

    def test_server_tools1(self):
        self.log.info(f'-----{os.path.basename(__file__)}start-----')
        self.log.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname)

        self.log.info('----收集日志信息时指定主机名称--------')
        start_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(start_time)
        time.sleep(30)
        end_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(end_time)
        collector_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_collector --begin-time="{start_time}" ' \
            f' --end-time="{end_time}" -h {hostname}'
        self.log.info(collector_cmd)
        collector_msg = self.primary_dbuser.sh(collector_cmd).result()
        self.log.info(collector_msg)
        self.assertIn(self.constant.GS_COLLECTOR_SUCCESS_MSG, collector_msg)
        time.sleep(5)
        self.log.info('----查看日志是否生成--------')
        self.log.info('----查看目录下文件--------')
        ls_cmd = f"ls -al {self.tmp_dir_path}"
        self.log.info(ls_cmd)
        ls_msg = self.primary_dbuser.sh(ls_cmd).result()
        self.log.info(ls_msg)
        self.log.info('----获取指定目录下的所有文件和目录名-----')
        find_cmd = f'find {self.tmp_dir_path} -type f -name\
                    "collector*.tar.gz" -cmin -1'
        self.log.info(find_cmd)
        find_msg = self.primary_dbuser.sh(find_cmd).result()
        self.log.info(find_msg)
        file_name = find_msg.split('/')[-1]
        self.assertTrue(file_name.startswith('collector') and \
                        file_name.endswith('tar.gz'))
        tar_cmd = f'cd {self.tmp_dir_path}; ' \
            f'tar -zxvf {file_name};'
        self.log.info(tar_cmd)
        tar_msg = self.primary_dbuser.sh(tar_cmd).result()
        self.log.info(tar_msg)
        self.assertIn('Summary.log', tar_msg)
        self.assertIn('Detail.log', tar_msg)
        self.assertIn(f'{hostname}.tar.gz', tar_msg)

    def tearDown(self):
        self.log.info('------清理环境，删除生成的collector日志文件------')
        rm_cmd = f'cd {self.tmp_dir_path};' \
            f'rm -rf collector_*'
        self.log.info(rm_cmd)
        rm_msg = self.root_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info(f'-----{os.path.basename(__file__)}finish-----')

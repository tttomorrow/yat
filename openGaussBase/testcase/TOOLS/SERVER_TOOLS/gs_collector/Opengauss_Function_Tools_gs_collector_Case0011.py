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
Case Name   : gs_collector工具收集日志信息时指定开始和结束时间
Description : 收集日志信息时指定开始和结束时间
Expect      : 收集成功
History     :
"""
import os
import unittest
import time
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info(f'-----{os.path.basename(__file__)}start-----')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()
        self.tmp_dir_path = os.path.join(os.path.dirname(macro.PG_LOG_PATH))

    def test_server_tools1(self):
        LOG.info('---收集日志信息时指定开始和结束时间---')
        start_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        LOG.info(start_time)
        time.sleep(30)
        end_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        LOG.info(end_time)
        check_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_collector --begin-time="{start_time}" ' \
            f' --end-time="{end_time}";'
        LOG.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.Constant.GS_COLLECTOR_SUCCESS_MSG, msg1)
        time.sleep(5)
        LOG.info('----查看目录下文件--------')
        ls_cmd = f"ls -al {self.tmp_dir_path}"
        LOG.info(ls_cmd)
        ls_msg = self.dbuserNode.sh(ls_cmd).result()
        LOG.info(ls_msg)
        LOG.info('----获取指定目录下的所有文件和目录名-----')
        find_cmd = f'find {self.tmp_dir_path} -type f -name\
                            "collector*.tar.gz" -cmin -1'
        LOG.info(find_cmd)
        find_msg = self.dbuserNode.sh(find_cmd).result()
        LOG.info(find_msg)
        file_name = find_msg.split('/')[-1]
        self.assertTrue(file_name.startswith('collector') and \
                        file_name.endswith('tar.gz'))
        tar_cmd = f'cd {self.tmp_dir_path}; ' \
            f'tar -zxvf {file_name};'
        LOG.info(tar_cmd)
        tar_msg = self.dbuserNode.sh(tar_cmd).result()
        LOG.info(tar_msg)
        self.assertIn('Summary.log', tar_msg)
        self.assertIn('Detail.log', tar_msg)

    def tearDown(self):
        LOG.info('------清理环境，删除生成的collector日志文件------')
        rm_cmd = f'cd {self.tmp_dir_path};' \
            f'rm -rf collector_*'
        LOG.info(rm_cmd)
        rm_msg = self.dbuserNode.sh(rm_cmd).result()
        LOG.info(rm_msg)
        LOG.info(f'-----{os.path.basename(__file__)}finish-----')

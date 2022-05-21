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
Case Type   : 系统内部使用工具
Case Name   : 执行gs_preinstall -? 查看帮助信息
Description :
    1.拷贝script文件,创建数据库相关文件夹
    2.在script目录下，执行gs_preinstall命令：./gs_preinstall -?
    3.清理环境
Expect      :
    1.成功
    2.返回帮助信息
    3.清理成功
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.Common import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        primary_sh = CommonSH('PrimaryDbUser')
        if primary_sh.get_node_num() == 1:
            self.root_node = Node('PrimaryRoot')
        else:
            self.root_node = Node('Standby2Root')
        self.common = Common()
        path = os.path.dirname(os.path.dirname(macro.DB_INSTANCE_PATH))
        self.openGauss_path = os.path.join(path, 'dir_gs_preinstall_0014')
        self.package_path = os.path.join(self.openGauss_path, 'pkg')

    def test_standby(self):
        text = '-----step1:拷贝script文件,创建数据库相关文件夹 expect:成功-----'
        self.log.info(text)
        pkg_path = os.path.dirname(macro.DB_SCRIPT_PATH)
        mkdir_cmd = f"rm -rf {self.openGauss_path}/;" \
            f"mkdir -p {self.openGauss_path};" \
            f"cp -r {pkg_path} {self.openGauss_path}"
        self.log.info(mkdir_cmd)
        msg = self.common.get_sh_result(self.root_node, mkdir_cmd)
        self.assertEqual('', msg, '执行失败:' + text)
        package_path = os.path.join(self.openGauss_path,
                                    os.path.basename(pkg_path))
        script_path = os.path.join(package_path, 'script')

        step = '----step2:在script目录下，执行gs_preinstall命令 expect:返回帮助信息----'
        self.log.info(step)
        preinstall_cmd = f"cd {script_path};" \
            f"./gs_preinstall -? "
        self.log.info(preinstall_cmd)
        msg = self.root_node.sh(preinstall_cmd).result()
        self.log.info(msg)
        msg_list = ['gs_preinstall -? | --help',
                    'gs_preinstall -V | --version',
                    'gs_preinstall -U USER -G GROUP -X XMLFILE', '-U', '-G',
                    '-X', '-L', '--skip-os-set', '--env-var="ENVVAR"',
                    '--sep-env-file=ENVFILE', '--skip-hostname-set',
                    '-?, --help', '-V, --version', '--non-interactive']
        for content in msg_list:
            self.assertTrue(msg.find(content) > -1, '执行失败:' + step)

    def tearDown(self):
        self.log.info('----清理环境----')
        text = '-----删除数据准备目录 expect:成功-----'
        self.log.info(text)
        del_cmd = f'rm -rf {self.openGauss_path}'
        self.common.get_sh_result(self.root_node, del_cmd)
        check_cmd = f'if [ -d {self.openGauss_path} ]; ' \
            f'then echo "exists"; else echo "not exists"; fi'
        del_msg = self.common.get_sh_result(self.root_node, check_cmd)

        self.assertEqual('not exists', del_msg, '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

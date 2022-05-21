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
Case Type   : 简化安装
Case Name   : 极简安装--安装路径权限为500
Description :
    1.创建omm用户和用户组
    2.root用户创建安装目录
    3.下载并解压openGauss安装包到安装目录
    4.安装目录权限改为500
    5.omm进入解压后目录下的simpleInstall.执行安装脚本
      sh install.sh  -p xxx -w xxx
    6.清理环境：删除安装目录，删除omm用户
Expect      :
    1.用户和用户组创建成功
    2.目录创建成功
    3.安装目录下成功解压openGauss安装包
    4.安装目录权限修改成功
    5.安装失败，提示权限不足
    6.清理成功
History     :
"""


import os
import unittest
import time
from testcase.utils.Common import Common
from testcase.utils.Common import CommonSH
from testcase.utils.Constant import Constant
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
            self.primary_node = Node('PrimaryDbUser')
        else:
            self.root_node = Node('Standby2Root')
            self.primary_node = Node('Standby2DbUser')
        self.common = Common()
        self.constant = Constant()
        self.path = os.path.dirname(macro.DB_SCRIPT_PATH)
        self.pkg_path = os.path.join(os.path.dirname(macro.DB_SCRIPT_PATH),
                                     '*.tar.bz2')
        self.install_pkg_path = os.path.join(
            os.path.dirname(macro.DB_SCRIPT_PATH), 'pkg')
        self.bz_pkg_path = os.path.join(self.install_pkg_path, '*.tar.bz2')
        self.log.info(self.bz_pkg_path)
        self.simpleInstall_path = os.path.join(self.install_pkg_path,
                                               'simpleInstall')
        self.u_name = 'u_sim_0035'
        self.env_path = os.path.join('/home', self.u_name, '.bashrc')

    def test_tools_simpleinstall(self):

        text = '----查询系统未使用端口----'
        self.log.info(text)
        port = self.common.get_not_used_port(self.primary_node)
        self.log.info(port)

        text = '----step1:创建数据库用户和用户组;expect:创建成功----'
        self.log.info(text)
        self.common.create_user(self.root_node, self.u_name)

        text = '----step2:root用户创建安装包目录;expect:安装包目录创建成功----'
        self.log.info(text)
        is_dir_exists_cmd = f'''if [ ! -d "{self.install_pkg_path}" ]
                                then
                                    mkdir -p {self.install_pkg_path}
                                fi'''
        result = self.common.get_sh_result(self.root_node, is_dir_exists_cmd)
        self.log.info(result)
        self.assertEqual(result, '', '执行失败:' + text)

        text = '----step3:下载解压数据库安装包 expect:下载解压成功----'
        self.log.info(text)
        cp_cmd = f'cp -r {self.pkg_path} {self.install_pkg_path};' \
                 f'ls {self.install_pkg_path}'
        self.log.info(cp_cmd)
        result = self.root_node.sh(cp_cmd).result()
        self.log.info(result)
        self.assertIn('.tar.bz2', result, '执行失败:' + text)
        text = '-----解压文件-----'
        self.log.info('text')
        tar_cmd = f'tar -jxf {self.bz_pkg_path} -C {self.install_pkg_path}; '
        self.log.info(tar_cmd)
        tar_result = self.root_node.sh(tar_cmd).result()
        time.sleep(15)
        self.log.info(tar_result)
        ls_cmd = f'ls {self.install_pkg_path}'
        self.log.info(ls_cmd)
        ls_result = self.common.get_sh_result(self.root_node, ls_cmd)
        self.log.info(ls_result)
        self.assertIn('simpleInstall', ls_result, '执行失败:' + text)

        text = '----step4:root用户修改安装路径权限为500;expect:修改权限成功----'
        self.log.info(text)
        chm_cmd = f'chmod -R 500 {self.install_pkg_path};'
        self.log.info(chm_cmd)
        chm_result = self.common.get_sh_result(self.root_node, chm_cmd)
        self.log.info(chm_result)

        text = '----step5:omm用户进入安装目录下执行安装;expect:安装失败----'
        self.log.info(text)
        install_cmd = f'su - {self.u_name} -c ' \
                      f'"source {self.env_path}&&' \
                      f'cd {self.simpleInstall_path}&&' \
                      f'pwd&&' \
                      f'sh install.sh  -p {port} -w {macro.COMMON_PASSWD}"'
        self.log.info(install_cmd)
        install_msg = self.common.get_sh_result(self.root_node, install_cmd)
        self.log.info(install_msg)
        self.assertIn(self.constant.PERMISSION_DENY_MSG,
                      install_msg, '执行失败' + text)

    def tearDown(self):
        text = '----step6:清理环境;expect:清理环境成功----'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.install_pkg_path};'
        self.log.info(rm_cmd)
        rm_result = self.common.get_sh_result(self.root_node, rm_cmd)
        self.log.info(rm_result)
        check_cmd = f'if [ -d {self.install_pkg_path} ]; ' \
                    f'then echo "exists"; else echo "not exists"; fi'
        self.log.info(check_cmd)
        check_result = self.common.get_sh_result(self.root_node, check_cmd)
        self.log.info(check_result)
        user_del = f'userdel -rf {self.u_name}'
        self.log.info(user_del)
        user_result = self.common.get_sh_result(self.root_node, user_del)
        self.log.info(user_result)
        self.assertEqual('not exists', check_result, '执行失败:' + text)
        self.assertEqual('', user_result, '删除用户失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')
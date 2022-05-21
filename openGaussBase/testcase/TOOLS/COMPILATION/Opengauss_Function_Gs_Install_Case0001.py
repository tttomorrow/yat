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
Case Name   : 执行gs_install命令安装数据库，指定安装日志文件及日志文件存放的
              路径
Description :
    1.下载解压数据库安装包
    2.配置xml文件
    3.修改新数据库文件属组为数据库初始用户
    4.gs_preinstall预安装：
    ./gs_preinstall -U [初始用户] -G [初始用户组] -X [xml配置文件路径]
    --sep-env-file=[env文件路径] --non-interactive --skip-hostname-set
    5.gs_install安装数据库：
    gs_install -X [xml配置文件路径] -l [指定日志路径]/[文件名]
    6.清理环境
    gs_uninstall 删除数据库：gs_uninstall --delete-data
    postuninstall清理数据库：
    ./gs_postuninstall -U autotest  -X [xml配置文件路径]
    删除数据库相关目录：
    rm -rf [数据库相关目录]
Expect      :
    1.下载解压成功
    2.配置成功
    3.成功
    4.预安装成功
    5.安装成功,[指定日志路径]下生成"gs_local"+时间戳+".log"和
    "[指定文件名]"+时间戳+".log"命名的两个日志文件
    6.清理成功
History     :
"""
import os
import re
import unittest

from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_node = Node('PrimaryDbUser')
Constant = Constant()

wget_result = Primary_node.sh(f"wget {macro.FTP_PATH} -c -t2 -T30").result()


@unittest.skipIf(re.search(Constant.wget_connect_success_msg, wget_result)
                 is None, 'wget连接失败')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Install_Case0001开始执行----')
        self.primary_root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.common = Common()
        path = os.path.dirname(os.path.dirname(macro.DB_INSTANCE_PATH))
        self.openGauss_path = os.path.join(path, 'dir_gs_install_0001')
        self.package_path = os.path.join(self.openGauss_path, 'pkg')
        self.conf_path = os.path.join(self.openGauss_path, 'config')
        self.data_path = os.path.join(self.openGauss_path, 'cluster')
        self.xml_path = os.path.join(self.conf_path, 'single.xml')
        self.env_path = os.path.join(self.conf_path, 'env')
        self.script_path = os.path.join(self.package_path, 'script')

    def test_standby(self):
        text = '----step1:下载解压数据库安装包 expect:下载解压成功----'
        self.log.info(text)
        self.common.check_load_msg(self.primary_root_node, self.primary_node,
                                   self.package_path, self.conf_path)

        test = '----step1.1查看主机名;expect:成功----'
        self.log.info(test)
        node_name = self.primary_root_node.sh("uname -n").result()
        self.log.info(node_name)
        self.assertIsNotNone(node_name, '执行失败:' + text)

        test = '----step1.2:查询系统未使用端口;expect:成功----'
        self.log.info(test)
        port = self.common.get_not_used_port(self.primary_node)
        self.assertNotEqual(0, port, '执行失败:' + text)

        text = '----step2:配置xml文件 expect:配置成功----'
        self.log.info(text)
        gaussdb_app_path = os.path.join(self.data_path, 'app')
        gaussdb_log_path = os.path.join(self.data_path, 'gaussdb_log')
        tmpmppdb_path = os.path.join(self.data_path, 'tmp')
        gaussdb_tool_path = os.path.join(self.data_path, 'tool')
        data_node1 = os.path.join(self.data_path, 'dn1')
        self.common.scp_file(self.primary_root_node, 'single.xml',
                             self.conf_path)
        xml_cmd = f"sed -i 's#v_nodeNames#{node_name}#g' {self.xml_path};" \
                  f"sed -i 's#v_gaussdbAppPath#{gaussdb_app_path}#g' " \
                  f"{self.xml_path};" \
                  f"sed -i 's#v_gaussdbLogPath#{gaussdb_log_path}#g' " \
                  f"{self.xml_path};" \
                  f"sed -i 's#v_tmpMppdbPath#{tmpmppdb_path}#g' " \
                  f"{self.xml_path};" \
                  f"sed -i 's#v_gaussdbToolPath#{gaussdb_tool_path}#g' " \
                  f"{self.xml_path};" \
                  f"sed -i 's#v_corePath#{macro.DB_CORE_PATH}#g' " \
                  f"{self.xml_path};" \
                  f"sed -i 's#v_db_host#{self.primary_node.db_host}#g' " \
                  f"{self.xml_path};" \
                  f"sed -i 's#v_dataPortBase#{port}#g' {self.xml_path};" \
                  f"sed -i 's#v_dataNode1#{data_node1}#g' {self.xml_path};" \
                  f"cat {self.xml_path}"
        self.log.info(xml_cmd)
        result = self.primary_root_node.sh(xml_cmd).result()
        self.log.info(result)
        msg_list = [node_name, self.data_path, f"{port}",
                    self.primary_node.db_host]
        for content in msg_list:
            self.assertTrue(result.find(content) > -1, '执行失败:' + text)

        text = '----step2.1:获取数据库用户的用户组;expect:成功----'
        self.log.info(text)
        user_groups = f'groups {self.primary_node.ssh_user}'
        self.log.info(user_groups)
        groups_msg = self.primary_root_node.sh(user_groups).result()
        self.log.info(groups_msg)
        self.assertIn(f'{self.primary_node.ssh_user}', groups_msg,
                      '执行失败:' + test)
        group = groups_msg.split()[2]

        text = '----step3:修改属组 expect:成功----'
        self.log.info(text)
        file_own = f'chown -R {self.primary_node.ssh_user}:{group} ' \
                   f'{self.openGauss_path}'
        self.log.info(file_own)
        file_msg = self.primary_root_node.sh(file_own).result()
        self.log.info(file_msg)
        self.assertEqual('', file_msg, '执行失败:' + test)

        text = '----step4:执行gs_preinstall命令 expect:预安装成功----'
        self.log.info(text)
        preinstall_cmd = f"cd {self.script_path};" \
                         f"./gs_preinstall -U {self.primary_node.ssh_user} " \
                         f"-G {group} " \
                         f"-X {self.xml_path} " \
                         f"--sep-env-file={self.env_path} " \
                         f"--non-interactive --skip-hostname-set;" \
                         f"chown -R {self.primary_node.ssh_user}:{group} " \
                         f"{self.openGauss_path}"
        self.log.info(preinstall_cmd)
        msg = self.primary_root_node.sh(preinstall_cmd).result()
        self.log.info(msg)
        self.assertIn(Constant.preinstall_success_msg, msg,
                      '执行失败:' + text)

        text = '--step5:执行gs_install命令 expect:安装成功,生成指定log文件--'
        self.log.info(text)
        log_file = os.path.join(self.openGauss_path, 'install_0001.log')
        install_cmd = f"gs_install -X {self.xml_path} -l {log_file}"
        exec_msg = self.common.do_install(self.primary_node, self.env_path,
                                          install_cmd)
        self.assertIn(Constant.install_success_msg, exec_msg,
                      '执行失败:' + text)
        ls_cmd = f"ls {self.openGauss_path}"
        exec_msg = self.primary_root_node.sh(ls_cmd).result()
        assert1 = re.search(
            r"gs_local-[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}.log", exec_msg)
        assert2 = re.search(
            r"install_0001-[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}.log", exec_msg)
        self.assertIsNotNone(assert1, '执行失败:' + text)
        self.assertIsNotNone(assert2, '执行失败:' + text)

    def tearDown(self):
        self.log.info('----step6:清理环境----')
        text_1 = '----gs_uninstall卸载数据库 expect:卸载成功----'
        self.log.info(text_1)
        uninstall_cmd = f"source {self.env_path};" \
                        f"cd {self.script_path};" \
                        f"./gs_uninstall --delete-data"
        self.log.info(uninstall_cmd)
        uninstall_msg = self.primary_node.sh(uninstall_cmd).result()
        self.log.info(uninstall_msg)

        text_2 = '----gs_postuninstall清理数据库 expect:成功----'
        self.log.info(text_2)
        postuninstall_cmd = f'source {self.env_path};' \
                            f'cd {self.script_path};' \
                            f'./gs_postuninstall  ' \
                            f'-U {self.primary_node.ssh_user}  ' \
                            f'-X {self.xml_path}'
        postuninstall_msg = self.primary_root_node.sh(
            postuninstall_cmd).result()
        self.log.info(postuninstall_msg)

        text_3 = '----删除数据准备目录 expect:成功----'
        self.log.info(text_3)
        del_cmd = f'rm -rf {self.openGauss_path}'
        self.log.info(del_cmd)
        del_msg = self.primary_root_node.sh(del_cmd).result()
        self.log.info(del_msg)
        self.log.info('断言teardown成功')
        self.assertIn(Constant.uninstall_success_msg, uninstall_msg,
                      '执行失败:' + text_1)
        self.assertIn(Constant.postuninstall_success_msg,
                      postuninstall_msg, '执行失败:' + text_2)
        self.assertEqual('', del_msg, '执行失败:' + text_3)
        self.log.info(
            '----Opengauss_Function_Gs_Install_Case0001执行完成----')

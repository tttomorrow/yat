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
Case Name   : 执行gs_preinstall命令，设置操作系统参数--skip-os-set
Description :
    1.下载解压数据库安装包
    2.配置xml文件
    3.修改新数据库文件属组为数据库初始用户
    4.在script目录下，执行gs_preinstall命令：
    ./gs_preinstall -U [数据库初始用户] -G [初始用户组] -X [xml配置文件路径]
    --sep-env-file=[env文件路径]  --skip-os-set --non-interactive
    --skip-hostname-set
    5.清理环境
    删除数据库相关目录：
    rm -rf [数据库相关目录]
Expect      :
    1.下载解压成功
    2.配置成功
    3.成功
    4.预安装成功,打印内容不包含Setting OS parameters
    5.清理成功
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
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.primary_root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.common = Common()
        path = os.path.dirname(os.path.dirname(macro.DB_INSTANCE_PATH))
        while True:
            if len(path.split('/')) == 2:
                break
            else:
                path = os.path.dirname(path)
        self.openGauss_path = os.path.join(path, 'dir_gs_preinstall_0006')
        self.package_path = os.path.join(self.openGauss_path, 'pkg')
        self.conf_path = os.path.join(self.openGauss_path, 'config')
        self.data_path = os.path.join(self.openGauss_path, 'cluster')
        self.xml_path = os.path.join(self.conf_path, 'single.xml')
        self.env_path = os.path.join(self.conf_path, 'env')
        self.script_path = os.path.join(self.package_path, 'script')

    def test_standby(self):
        text = '-----step1:下载解压数据库安装包 expect:下载解压成功-----'
        self.log.info(text)
        self.common.check_load_msg(self.primary_root_node, self.primary_node,
                                   self.package_path, self.conf_path)

        test = '-----查看主机名-----'
        self.log.info(test)
        node_name = self.primary_root_node.sh("uname -n").result()
        self.log.info(node_name)
        self.assertIsNotNone(node_name, '执行失败:' + text)

        test = '-----查询系统未使用端口-----'
        self.log.info(test)
        port = self.common.get_not_used_port(self.primary_node)
        self.assertNotEqual(0, port, '执行失败:' + text)

        text = '-----step2:配置xml文件 expect:配置成功-----'
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
            f"sed -i 's#v_corePath#{macro.DB_CORE_PATH}#g' {self.xml_path};" \
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

        text = '-----获取数据库用户的用户组-----'
        self.log.info(text)
        user_groups = f'groups {self.primary_node.ssh_user}'
        self.log.info(user_groups)
        groups_msg = self.primary_root_node.sh(user_groups).result()
        self.log.info(groups_msg)
        self.assertIn(f'{self.primary_node.ssh_user}', groups_msg,
                      '执行失败:' + test)
        group = groups_msg.split()[2]

        text = '-----step3:修改属组 expect:成功-----'
        self.log.info(text)
        file_own = f'chown -R {self.primary_node.ssh_user}:{group} ' \
            f'{self.openGauss_path}'
        self.log.info(file_own)
        file_msg = self.primary_root_node.sh(file_own).result()
        self.log.info(file_msg)
        self.assertEqual('', file_msg, '执行失败:' + test)

        text = '-----step4:在script目录下，执行gs_preinstall命令 ' \
               'expect:预安装成功,打印内容不包含Setting OS parameters-----'
        self.log.info(text)
        preinstall_cmd = f"cd {self.script_path};" \
            f"./gs_preinstall -U {self.primary_node.ssh_user} -G {group} " \
            f"-X {self.xml_path} --sep-env-file={self.env_path} " \
            f"--skip-os-set --non-interactive --skip-hostname-set"
        self.log.info(preinstall_cmd)
        msg = self.primary_root_node.sh(preinstall_cmd).result()
        self.log.info(msg)
        self.assertIn(Constant.preinstall_success_msg, msg,
                      '执行失败:' + text)
        self.assertNotIn(Constant.preinstall_setos_success_msg, msg,
                         '执行失败:' + text)

    def tearDown(self):
        self.log.info('-----step5:清理环境-----')
        text_1 = '-----删除数据准备目录 expect:成功-----'
        self.log.info(text_1)
        del_cmd = f'rm -rf {self.openGauss_path}'
        self.common.get_sh_result(self.primary_root_node, del_cmd)
        check_cmd = f'if [ -d {self.openGauss_path} ]; ' \
            f'then echo "exists"; else echo "not exists"; fi'
        del_msg = self.common.get_sh_result(self.primary_root_node, check_cmd)

        self.assertEqual('not exists', del_msg, '执行失败:' + text_1)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

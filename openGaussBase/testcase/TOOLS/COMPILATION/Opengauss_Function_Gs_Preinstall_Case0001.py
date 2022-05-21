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
Case Name   : 使用初始用户（非root）用户执行gs_preinstall命令
Description :
    1.拷贝script文件,创建数据库相关文件夹
    2.配置数据库xml文件
    3.修改新数据库文件属组为数据库初始用户
    4.在script目录下，切换自定义初始用户执行gs_preinstall命令：
    ./gs_preinstall -U [初始用户] -G [初始用户组] -X [xml配置文件路径]
    --sep-env-file=[env文件路径]  --non-interactive  --skip-hostname-set
    5.清理环境
    删除数据目录
    rm -rf [数据库相关目录]
Expect      :
    1.成功
    2.配置成功
    3.成功
    4.预安装失败，返回错误信息：
    Only a user with the root permission can run this script
    5.清理成功
History     :
"""
import os
import unittest

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
            self.node = Node('PrimaryDbUser')
        else:
            self.root_node = Node('Standby2Root')
            self.node = Node('Standby2DbUser')
        self.constant = Constant()
        self.common = Common()
        path = macro.DB_INSTANCE_PATH
        for i in range(len(path.split('/')) - 2):
            path = os.path.join(path, '..')
        self.openGauss_path = os.path.join(path, 'dir_gs_preinstall_0001')
        self.conf_path = os.path.join(self.openGauss_path, 'config')
        self.data_path = os.path.join(self.openGauss_path, 'cluster')
        self.xml_path = os.path.join(self.conf_path, 'single.xml')
        self.env_path = os.path.join(self.conf_path, 'env')

    def test_standby(self):
        text = '-----step1:拷贝script文件,创建数据库相关文件夹 expect:成功-----'
        self.log.info(text)
        pkg_path = os.path.dirname(macro.DB_SCRIPT_PATH)
        mkdir_cmd = f"rm -rf {self.openGauss_path}/;" \
            f"mkdir -p {self.conf_path};" \
            f"cp -r {pkg_path} {self.openGauss_path}"
        self.log.info(mkdir_cmd)
        msg = self.common.get_sh_result(self.root_node, mkdir_cmd)
        self.assertEqual('', msg, '执行失败:' + text)
        package_path = os.path.join(self.openGauss_path,
                                    os.path.basename(pkg_path))
        script_path = os.path.join(package_path, 'script')

        test = '----查看主机名----'
        self.log.info(test)
        node_name = self.root_node.sh("uname -n").result()
        self.log.info(node_name)
        self.assertIsNotNone(node_name, '执行失败:' + text)

        test = '----查询系统未使用端口----'
        self.log.info(test)
        port = self.common.get_not_used_port(self.node)
        self.assertNotEqual(0, port, '执行失败:' + text)

        text = '----step2:配置xml文件 expect:配置成功----'
        self.log.info(text)
        gaussdb_app_path = os.path.join(self.data_path, 'app')
        gaussdb_log_path = os.path.join(self.data_path, 'gaussdb_log')
        tmpmppdb_path = os.path.join(self.data_path, 'tmp')
        gaussdb_tool_path = os.path.join(self.data_path, 'tool')
        data_node1 = os.path.join(self.data_path, 'dn1')
        self.common.scp_file(self.root_node, 'single.xml', self.conf_path)
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
            f"sed -i 's#v_db_host#{self.node.db_host}#g' " \
            f"{self.xml_path};" \
            f"sed -i 's#v_dataPortBase#{port}#g' {self.xml_path};" \
            f"sed -i 's#v_dataNode1#{data_node1}#g' {self.xml_path};" \
            f"cat {self.xml_path}"
        self.log.info(xml_cmd)
        result = self.root_node.sh(xml_cmd).result()
        self.log.info(result)
        msg_list = [node_name, self.data_path, f"{port}", self.node.db_host]
        for content in msg_list:
            self.assertTrue(result.find(content) > -1, '执行失败:' + text)

        text = '----获取数据库用户的用户组----'
        self.log.info(text)
        user_groups = f'groups {self.node.ssh_user}'
        self.log.info(user_groups)
        groups_msg = self.root_node.sh(user_groups).result()
        self.log.info(groups_msg)
        self.assertIn(f'{self.node.ssh_user}', groups_msg,
                      '执行失败:' + test)
        group = groups_msg.split()[2]

        text = '----step3:修改属组 expect:成功----'
        self.log.info(text)
        file_own = f'chown -R {self.node.ssh_user}:{group} ' \
            f'{self.openGauss_path}'
        self.log.info(file_own)
        file_msg = self.root_node.sh(file_own).result()
        self.log.info(file_msg)
        self.assertEqual('', file_msg, '执行失败:' + test)

        text = '----step4:在script目录下，普通用户执行' \
               'gs_preinstall命令 expect:预安装失败----'
        self.log.info(text)
        preinstall_cmd = f"cd {script_path};" \
            f"./gs_preinstall -U {self.node.ssh_user} " \
            f"-G {self.node.ssh_user} -X {self.xml_path} " \
            f"--sep-env-file={self.env_path} --non-interactive " \
            f"--skip-hostname-set"
        self.log.info(preinstall_cmd)
        exec_msg = self.node.sh(preinstall_cmd).result()
        self.log.info(exec_msg)
        self.assertIn(self.constant.preinstall_error_msg, exec_msg,
                      '执行失败:' + text)

    def tearDown(self):
        self.log.info('----step5:清理环境----')
        text = '----删除数据目录 expect:成功----'
        self.log.info(text)
        del_cmd = f'rm -rf {self.openGauss_path}'
        self.common.get_sh_result(self.root_node, del_cmd)
        check_cmd = f'if [ -d {self.openGauss_path} ]; ' \
            f'then echo "exists"; else echo "not exists"; fi'
        del_msg = self.common.get_sh_result(self.root_node, check_cmd)

        self.assertEqual('not exists', del_msg, '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

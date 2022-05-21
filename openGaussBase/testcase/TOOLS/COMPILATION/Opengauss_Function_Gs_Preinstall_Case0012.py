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
Case Name   : 执行gs_preinstall命令，为安全交互模式时，输入密码包含特殊字符";","'","$"
Description :
    1.下载解压数据库安装包
    2.配置xml文件,配置参数gaussdbLogPath
    3.创建初始用户并修改文件属组
    4.gs_preinstall预安装,输入密码包含特殊字符";","'","$"：
    ./gs_preinstall -U [自定义初始用户] -G [自定义初始用户组] -X [xml配置文件路径]
    --sep-env-file=[env文件路径]
    5.清理环境
    rm -rf [数据库相关目录]
    userdel -r [自定义初始用户]
Expect      :
    1.下载解压成功
    2.配置成功
    3.创建成功
    4.预安装失败
    5.清理成功
History     :
"""
import os
import re
import unittest

from testcase.utils.Common import Common
from testcase.utils.Common import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_node = Node('PrimaryDbUser')
primary_sh = CommonSH('PrimaryDbUser')
constant = Constant()
wget_result = Primary_node.sh(f"wget {macro.FTP_PATH} -c -t2 -T30").result()


@unittest.skipIf(re.search(constant.wget_connect_success_msg, wget_result)
                 is None, 'wget连接失败')
@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_gs_preinstall_Case0012'
                      '开始执行----')
        self.primary_root_node = Node('PrimaryRoot')
        self.standby1_root_node = Node('Standby1Root')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.common = Common()
        self.u_name = 'u_gs_preinstall_0012'
        self.path = os.path.split(macro.DB_INSTANCE_PATH)[0].split('/')[1]
        self.openGauss_path = os.path.join('/', '%s' % self.path,
                                           'dir_gs_preinstall_0012')
        self.package_path = os.path.join(self.openGauss_path, 'pkg')
        self.conf_path = os.path.join(self.openGauss_path, 'config')
        self.data_path = os.path.join(self.openGauss_path, 'cluster')
        self.xml_path = os.path.join(self.conf_path, 'primary_standby.xml')
        self.env_path = os.path.join(self.conf_path, 'env')
        self.script_path = os.path.join(self.package_path, 'script')
        self.log_path = os.path.join(self.openGauss_path, 'log_path')

    def test_gs_preinstall(self):
        text = '----step1:下载解压数据库安装包 expect:下载解压成功----'
        self.log.info(text)
        self.common.check_load_msg(self.primary_root_node, self.primary_node,
                                   self.package_path, self.conf_path)

        test = '----查看主机名----'
        self.log.info(test)
        pri_node_name = self.primary_root_node.sh("uname -n").result()
        self.log.info(pri_node_name)
        self.assertIsNotNone(pri_node_name, '执行失败:' + text)
        sta_node_name = self.standby1_root_node.sh("uname -n").result()
        self.log.info(sta_node_name)
        self.assertIsNotNone(sta_node_name, '执行失败:' + text)

        test = '----查询系统未使用端口----'
        self.log.info(test)
        port = self.common.get_not_used_port(self.primary_node)
        self.assertNotEqual(0, port, '执行失败:' + text)

        text = '----step2:配置xml文件,配置参数gaussdbLogPath expect:配置成功----'
        self.log.info(text)
        gaussdb_app_path = os.path.join(self.data_path, 'app')
        gaussdb_log_path = os.path.join(self.data_path, 'gaussdb_log')
        tmpmppdb_path = os.path.join(self.data_path, 'tmp')
        gaussdb_tool_path = os.path.join(self.data_path, 'tool')
        data_node1 = os.path.join(self.data_path, 'dn1')
        self.common.scp_file(self.primary_root_node, 'primary_standby.xml',
                             self.conf_path)
        xml_cmd = f"sed -i 's#v_nodeNames#{pri_node_name},{sta_node_name}" \
            f"#g' {self.xml_path};" \
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
            f"sed -i 's#v_db_host#{self.primary_node.db_host}," \
            f"{self.standby_node.db_host}#g' {self.xml_path};" \
            f"sed -i 's#v_pri_nodeNames#{pri_node_name}#g' " \
            f"{self.xml_path};" \
            f"sed -i 's#v_pri_db_host#{self.primary_node.db_host}#g' " \
            f"{self.xml_path};" \
            f"sed -i 's#v_dataPortBase#{port}#g' {self.xml_path};" \
            f"sed -i 's#v_dataNode1#{data_node1},{sta_node_name}," \
            f"{data_node1}#g' {self.xml_path};" \
            f"sed -i 's#v_sta_nodeNames#{sta_node_name}#g' " \
            f"{self.xml_path};" \
            f"sed -i 's#v_sta_db_host#{self.standby_node.db_host}#g' " \
            f"{self.xml_path};" \
            f"cat {self.xml_path}"
        self.log.info(xml_cmd)
        result = self.primary_root_node.sh(xml_cmd).result()
        self.log.info(result)
        msg_list = [pri_node_name, self.primary_node.db_host,
                    sta_node_name, self.standby_node.db_host,
                    self.data_path, f"{port}"]
        for content in msg_list:
            self.assertTrue(result.find(content) > -1, '执行失败:' + text)
        self.assertIn('gaussdbLogPath', result, '执行失败:' + text)

        text = '----step3:创建初始用户修改密码并修改文件属性 expect:成功----'
        self.log.info(text)
        self.common.create_user(self.primary_root_node, self.u_name)
        file_own = f'chown -R {self.u_name}:{self.u_name} ' \
            f'{self.openGauss_path}'
        self.log.info(file_own)
        file_msg = self.primary_root_node.sh(file_own).result()
        self.log.info(file_msg)
        self.assertEqual('', file_msg, '执行失败:' + test)

        text = '----step4:执行gs_preinstall命令，输入密码包含特殊字符' \
               'expect:预安装失败----'
        self.log.info(text)
        spec_passwdlis = ["zaq1WSX\'", "zaq1WSX;", "zaq1WSX\\\$"]
        preinstall_cmd = f"./gs_preinstall " \
                         f"-U {self.u_name} -G {self.u_name} " \
                         f"-X {self.xml_path} " \
                         f"--sep-env-file={self.env_path}"
        for spec_passwd in spec_passwdlis:
            execute_cmd = f'''cd {self.script_path}
                       expect <<EOF
                       set timeout 400
                       spawn {preinstall_cmd}
                       expect "you want to create trust for root (yes/no)?"
                       send "no\\n"
                       expect "and create trust for it (yes/no)?"
                       send "yes\\n"
                       expect "Password:"
                       send "{spec_passwd}\\n"
                       expect "Failed to obtain the password"
                       expect eof\n''' + '''EOF'''
            self.log.info(execute_cmd)
            msg = self.primary_root_node.sh(execute_cmd).result()
            self.log.info(msg)
            self.assertNotIn(constant.preinstall_success_msg,
                             msg, '执行失败' + text)

    def tearDown(self):
        text = '----step5:清理环境 expect:配置成功----'
        self.log.info(text)
        text_1 = '----删除数据准备目录及用户 expect:成功----'
        self.log.info(text_1)
        del_cmd = f'rm -rf {self.openGauss_path}'
        userdel_cmd = f'userdel -r {self.u_name}'
        del_msg1 = self.primary_root_node.sh(del_cmd).result()
        self.log.info(del_msg1)
        del_msg2 = self.standby1_root_node.sh(del_cmd).result()
        self.log.info(del_msg2)
        del_msg3 = self.primary_root_node.sh(userdel_cmd).result()
        self.log.info(del_msg3)
        self.assertEqual('', del_msg1, '执行失败:' + text_1)
        self.assertEqual('', del_msg2, '执行失败:' + text_1)
        self.assertEqual('', del_msg3, '执行失败:' + text_1)
        self.log.info(
            '----Opengauss_Function_Gs_Preinstall_Case0012执行完成----')

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
Case Name   : 执行gs_preinstall命令，设置参数--skip-hostname-set
Description :
    1.拷贝script文件,创建数据库相关文件夹
    2.配置xml文件
    3.创建好初始用户并修改文件属组并备份hosts文件
    4.在script目录下，执行gs_preinstall命令：
    ./gs_preinstall -U [自定义初始用户] -G [自定义初始用户组] -X [xml配置文件路径]
    --sep-env-file=[env文件路径] --skip-hostname-set
    5.清理环境
    postuninstall清理数据库：
    ./gs_postuninstall -U [自定义初始用户]  -X [xml配置文件路径]
    删除数据库相关目录及用户并恢复hosts文件：
    rm -rf [数据库相关目录]
    userdel -r [自定义初始用户]
Expect      :
    1.创建成功
    2.配置成功
    3.修改文件属性成功,hosts文件备份成功
    4.预安装失败,xml配置文件中主机名与IP的映射关系不写入“/etc/hosts”文件中
    5.清理成功
History     :
    修改脚本开始结束打印信息
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.Common import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 'Single node, and subsequent codes are not executed.')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.root_node = Node('Standby2Root')
        self.node = Node('Standby2DbUser')
        self.standby1_root_node = Node('Standby1Root')
        self.standby1_node = Node('Standby1DbUser')
        self.constant = Constant()
        self.common = Common()
        self.u_name = 'u_gs_preinstall_0009'
        self.path = os.path.split(macro.DB_INSTANCE_PATH)[0].split('/')[1]
        self.openGauss_path = os.path.join('/', '%s' % self.path,
                                           'dir_gs_preinstall_0009')
        self.conf_path = os.path.join(self.openGauss_path, 'config')
        self.data_path = os.path.join(self.openGauss_path, 'cluster')
        self.xml_path = os.path.join(self.conf_path, 'primary_standby.xml')
        self.env_path = os.path.join(self.conf_path, 'env')
        self.log_path = os.path.join(self.openGauss_path, 'log_path')
        self.host_file = os.path.join('/', 'etc', 'hosts')
        self.host_bk = os.path.join('/', 'etc', 'hostsbk')

        test = '-----备份/etc/hosts文件,-----'
        self.log.info(test)
        hosts_cmd = f"mv {self.host_file} {self.host_bk};" \
            f"touch {self.host_file};" \
            f'echo "127.0.0.1    localhost" > {self.host_file};' \
            f'echo "::1    localhost" > {self.host_file}'
        msg1 = self.common.get_sh_result(self.standby1_root_node, hosts_cmd)
        msg2 = self.common.get_sh_result(self.root_node, hosts_cmd)
        self.assertEqual('', msg1 and msg2, '执行失败:' + test)

    def test_gs_preinstall(self):
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
        pri_node_name = self.root_node.sh("uname -n").result()
        self.log.info(pri_node_name)
        self.assertIsNotNone(pri_node_name, '执行失败:' + text)
        sta_node_name = self.standby1_root_node.sh("uname -n").result()
        self.log.info(sta_node_name)
        self.assertIsNotNone(sta_node_name, '执行失败:' + text)

        test = '----查询系统未使用端口----'
        self.log.info(test)
        port = self.common.get_not_used_port(self.node)
        self.assertNotEqual(0, port, '执行失败:' + text)

        text = '----step2:配置xml文件,配置参数gaussdbLogPath expect:配置成功----'
        self.log.info(text)
        gaussdb_app_path = os.path.join(self.data_path, 'app')
        gaussdb_log_path = os.path.join(self.data_path, 'gaussdb_log')
        tmpmppdb_path = os.path.join(self.data_path, 'tmp')
        gaussdb_tool_path = os.path.join(self.data_path, 'tool')
        data_node1 = os.path.join(self.data_path, 'dn1')
        self.common.scp_file(self.root_node, 'primary_standby.xml',
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
            f"sed -i 's#v_db_host#{self.node.db_host}," \
            f"{self.standby1_node.db_host}#g' {self.xml_path};" \
            f"sed -i 's#v_pri_nodeNames#{pri_node_name}#g' " \
            f"{self.xml_path};" \
            f"sed -i 's#v_pri_db_host#{self.node.db_host}#g' " \
            f"{self.xml_path};" \
            f"sed -i 's#v_dataPortBase#{port}#g' {self.xml_path};" \
            f"sed -i 's#v_dataNode1#{data_node1},{sta_node_name}," \
            f"{data_node1}#g' {self.xml_path};" \
            f"sed -i 's#v_sta_nodeNames#{sta_node_name}#g' " \
            f"{self.xml_path};" \
            f"sed -i 's#v_sta_db_host#{self.standby1_node.db_host}#g' " \
            f"{self.xml_path};" \
            f"cat {self.xml_path}"
        self.log.info(xml_cmd)
        result = self.root_node.sh(xml_cmd).result()
        self.log.info(result)
        msg_list = [pri_node_name, self.node.db_host,
                    sta_node_name, self.standby1_node.db_host,
                    self.data_path, f"{port}"]
        for content in msg_list:
            self.assertTrue(result.find(content) > -1, '执行失败:' + text)
        self.assertIn('gaussdbLogPath', result, '执行失败:' + text)

        text = '-----删除用户进程 expect:成功-----'
        self.log.info(text)
        kill_cmd = f"ps -u {self.u_name} | grep -v PID| " \
            f"awk \'{{{{print $1}}}}\' | xargs kill -9"
        self.common.get_sh_result(self.standby1_root_node, kill_cmd)
        self.common.get_sh_result(self.root_node, kill_cmd)

        text = '-----step3:创建初始新用户并修改属组 expect:成功-----'
        self.log.info(text)
        self.common.create_user(self.root_node, self.u_name)
        file_own = f'chown -R {self.u_name}:{self.u_name} ' \
            f'{self.openGauss_path};'
        self.log.info(file_own)
        file_msg = self.root_node.sh(file_own).result()
        self.log.info(file_msg)
        self.assertEqual('', file_msg, '执行失败:' + text)

        test = '----step4:在script目录下，执行gs_preinstall命令 ' \
               'expect:预安装失败,xml配置文件中主机名与IP的映射' \
               '关系不写入“/etc/hosts”文件中----'
        self.log.info(test)
        preinstall_cmd = f"./gs_preinstall -U {self.u_name} " \
            f"-G {self.u_name} -X {self.xml_path} " \
            f"--sep-env-file={self.env_path} " \
            f"--skip-hostname-set"
        cat_cmd = f"cat {self.host_file}"
        execute_cmd = f'''cd {script_path}
                   expect <<EOF
                   set timeout 600
                   spawn {preinstall_cmd}
                   expect "you want to create trust for root (yes/no)?"
                   send "no\\n"
                   expect "and create trust for it (yes/no)?"
                   send "yes\\n"
                   expect "Password:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect "Password:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        msg1 = self.root_node.sh(execute_cmd).result()
        self.log.info(msg1)
        msg2 = self.root_node.sh(cat_cmd).result()
        self.log.info(msg2)
        self.assertNotIn(self.constant.preinstall_success_msg, msg1,
                         '执行失败:' + test)
        self.assertNotIn(f'{self.node.db_host}  {pri_node_name}',
                         msg2, '执行失败:' + test)
        self.assertNotIn(f'{self.standby1_node.db_host}  {sta_node_name}',
                         msg2, '执行失败:' + test)

    def tearDown(self):
        self.log.info('----step5:清理环境----')
        text_1 = '-----恢复hosts文件 expect:成功-----'
        self.log.info(text_1)
        hosts_cmd = f'if [[ -e {self.host_file} && -e {self.host_bk} ]]; ' \
            f'then rm -rf {self.host_file}; ' \
            f'mv {self.host_bk} {self.host_file}; ' \
            f'else echo not exits; fi'
        hosts_msg1 = self.common.get_sh_result(self.standby1_root_node,
                                               hosts_cmd)
        hosts_msg2 = self.common.get_sh_result(self.root_node, hosts_cmd)

        text = '-----删除用户下进程 expect:成功-----'
        self.log.info(text)
        kill_cmd = f"ps -u {self.u_name} | grep -v PID| " \
            f"awk \'{{{{print $1}}}}\' | xargs kill -9"
        self.common.get_sh_result(self.standby1_root_node, kill_cmd)
        self.common.get_sh_result(self.root_node, kill_cmd)

        text_2 = '-----删除用户 expect:成功-----'
        self.log.info(text_2)
        udel_cmd = f'userdel -rf {self.u_name};'
        udel_msg = self.common.get_sh_result(self.root_node, udel_cmd)

        text_3 = '-----删除数据准备目录 expect:成功-----'
        self.log.info(text_3)
        del_cmd = f'rm -rf {self.openGauss_path}'
        self.common.get_sh_result(self.standby1_root_node, del_cmd)
        self.common.get_sh_result(self.root_node, del_cmd)
        check_cmd = f'if [ -d {self.openGauss_path} ]; ' \
            f'then echo "exists"; else echo "not exists"; fi'
        del_msg1 = self.common.get_sh_result(self.standby1_root_node,
                                             check_cmd)
        del_msg2 = self.common.get_sh_result(self.root_node, check_cmd)

        self.assertEqual('', hosts_msg1 and hosts_msg2, '执行失败:' + text_1)
        self.assertEqual('', udel_msg, '执行失败:' + text_1)
        self.assertEqual('not exists', del_msg1 and del_msg2,
                         '执行失败:' + text_3)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

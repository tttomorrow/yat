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
Case Name   : 安装包方式单节点安装数据库，备机扩容成功后主备切换正常
Description :
    1.下载解压数据库安装包
    2.配置单节点及备机扩容xml文件
    3.创建用户并修改文件属性
    4.gs_preinstall预安装：
    ./gs_preinstall -U [初始用户] -G [初始用户组] -X [xml配置文件路径]
    --sep-env-file=[env文件路径] --skip-hostname-set --non-interactive
    5.gs_install安装数据库：
    gs_install -X [xml配置文件路径]
    6.建立扩容备机root及用户互信
    7.gs_expansion备机扩容：
    ./gs_expansion -U {usrname} -G {grp_name} -X {xml_path} -h {hostname}
    8.停止数据库主机并执行gs_ctl failover -D {INSTANCE_PATH}进行failover
    9.清理环境
    gs_uninstall 删除数据库：gs_uninstall --delete-data
    清理用户下进程
    删除数据库相关目录并删除用户
Expect      :
    1.下载解压成功
    2.配置成功
    3.用户创建成功且文件属性修改成功
    4.预安装成功
    5.数据库安装成功
    6.互信建立成功
    7.备机扩容成功
    8.停止成功并成功进行failover
    9.清理成功
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
Constant = Constant()

wget_result = Primary_node.sh(f"wget {macro.FTP_PATH} -c -t2 -T30").result()


@unittest.skipIf(3 != primary_sh.get_node_num(), '非1+2环境不执行')
@unittest.skipIf(re.search(Constant.wget_connect_success_msg, wget_result)
                 is None, 'wget连接失败')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.common = Common()
        self.log.info(f'----{os.path.basename(__file__)} start----')
        self.primary_root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_root_node = Node('Standby1Root')
        self.standby_node = Node('Standby1DbUser')
        self.standby2_root_node = Node('Standby2Root')
        self.u_name = os.path.basename(__file__)[:-3].split('Tools_')[-1]
        self.pri_host = self.primary_node.db_host
        self.sta_host = self.standby_node.db_host
        self.sta2_host = self.standby2_root_node.db_host
        self.ssh_file = os.path.join('/home', self.u_name, 'hostfile')
        self.path = macro.DB_INSTANCE_PATH.split('/')[1]
        self.openGauss_path = os.path.join('/', f'{self.path}',
                                           f'{self.u_name}')
        self.package_path = os.path.join(self.openGauss_path, 'pkg')
        self.conf_path = os.path.join(self.openGauss_path, 'config')
        self.data_path = os.path.join(self.openGauss_path, 'cluster')
        self.xml_single_path = os.path.join(self.conf_path, 'single.xml')
        self.xml_expansion_path = os.path.join(self.conf_path,
                                               'primary_standby.xml')
        self.env_path = os.path.join(self.conf_path, 'env')
        self.script_path = os.path.join(self.package_path, 'script')
        self.instance_path = os.path.join(self.data_path, 'dn1')

    def test_gs_install(self):
        text = '----step1:下载解压数据库安装包 expect:下载解压成功----'
        self.log.info(text)
        self.common.check_load_msg(self.primary_root_node, self.primary_node,
                                   self.package_path, self.conf_path)
        text = '----查看主机名----'
        self.log.info(text)
        primary_node_name = self.primary_root_node.sh("uname -n").result()
        standby_node_name = self.standby_root_node.sh("uname -n").result()
        self.log.info(primary_node_name)
        self.log.info(standby_node_name)
        self.assertIsNotNone(primary_node_name, '执行失败:' + text)
        self.assertIsNotNone(standby_node_name, '执行失败:' + text)
        text = '----查询系统未使用端口----'
        self.log.info(text)
        for count in range(5):
            port = self.common.get_not_used_port(self.primary_node)
            self.log.info(port)
            standby_port_check_cmd = f'netstat -tlnp | grep {port}'
            check_msg = self.standby_root_node.sh(
                standby_port_check_cmd).result()
            self.log.info(check_msg)
            if not check_msg:
                self.assertNotEqual(0, port, '执行失败:' + text)
                break
            else:
                continue

        text = '----step2:配置单节点及备机扩容xml文件 expect:配置成功----'
        self.log.info(text)
        gaussdb_app_path = os.path.join(self.data_path, 'app')
        gaussdb_log_path = os.path.join(self.data_path, 'gaussdb_log')
        tmpmppdb_path = os.path.join(self.data_path, 'tmp')
        gaussdb_tool_path = os.path.join(self.data_path, 'tool')
        self.common.scp_file(self.primary_root_node, 'single.xml',
                             self.conf_path)
        self.common.scp_file(self.primary_root_node, 'primary_standby.xml',
                             self.conf_path)
        xml_single_cmd = \
            f"sed -i 's#v_nodeNames#{primary_node_name}#g' " \
            f"{self.xml_single_path};" \
            f"sed -i 's#v_gaussdbAppPath#{gaussdb_app_path}#g' " \
            f"{self.xml_single_path};" \
            f"sed -i 's#v_gaussdbLogPath#{gaussdb_log_path}#g' " \
            f"{self.xml_single_path};" \
            f"sed -i 's#v_tmpMppdbPath#{tmpmppdb_path}#g' " \
            f"{self.xml_single_path};" \
            f"sed -i 's#v_gaussdbToolPath#{gaussdb_tool_path}#g' " \
            f"{self.xml_single_path};" \
            f"sed -i 's#v_corePath#{macro.DB_CORE_PATH}#g' " \
            f"{self.xml_single_path};" \
            f"sed -i 's#v_db_host#{self.pri_host}#g' " \
            f"{self.xml_single_path};" \
            f"sed -i 's#v_dataPortBase#{port}#g' " \
            f"{self.xml_single_path};" \
            f"sed -i 's#v_dataNode1#{self.instance_path}#g' " \
            f"{self.xml_single_path};" \
            f"cat {self.xml_single_path}"
        self.log.info(xml_single_cmd)
        single_xml_result = self.primary_root_node.sh(xml_single_cmd).result()
        self.log.info(single_xml_result)
        msg_list = [primary_node_name, self.data_path, f"{port}",
                    self.pri_host]
        for content in msg_list:
            self.assertTrue(single_xml_result.find(content) > -1,
                            '执行失败:' + text)
        self.log.info('----配置扩容节点xml----')
        xml_expansion_cmd = \
            f"sed -i " \
            f"'s#v_nodeNames#{primary_node_name}, {standby_node_name}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_gaussdbAppPath#{gaussdb_app_path}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_gaussdbLogPath#{gaussdb_log_path}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_tmpMppdbPath#{tmpmppdb_path}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_gaussdbToolPath#{gaussdb_tool_path}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_corePath#{macro.DB_CORE_PATH}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_db_host#{self.pri_host}, {self.sta_host}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_pri_nodeNames#{primary_node_name}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_pri_db_host#{self.pri_host}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_dataPortBase#{port}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_dataNode1#" \
            f"{self.instance_path}, {standby_node_name}, " \
            f"{self.instance_path}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_sta_nodeNames#{standby_node_name}#g' " \
            f"{self.xml_expansion_path};" \
            f"sed -i 's#v_sta_db_host#{self.sta_host}#g' " \
            f"{self.xml_expansion_path};" \
            f"cat {self.xml_expansion_path}"
        self.log.info(xml_expansion_cmd)
        expansion_xml_result = self.primary_root_node.\
            sh(xml_expansion_cmd).result()
        self.log.info(expansion_xml_result)
        msg_list = [primary_node_name, standby_node_name, self.data_path,
                    f"{port}", self.pri_host, self.sta_host]
        for content in msg_list:
            self.assertTrue(expansion_xml_result.find(content) > -1,
                            '执行失败:' + text)

        text = '----step3:创建用户并修改文件属性 expect:成功----'
        self.log.info(text)
        self.common.create_user(self.primary_root_node, self.u_name)
        self.common.create_user(self.standby_root_node, self.u_name)
        self.common.create_user(self.standby2_root_node, self.u_name)
        file_own = f'chown -R {self.u_name}:{self.u_name} {self.openGauss_path}'
        self.log.info(file_own)
        file_msg = self.primary_root_node.sh(file_own).result()
        self.log.info(file_msg)
        self.assertEqual('', file_msg, '执行失败:' + text)

        text = '----step4:执行gs_preinstall命令 expect:预安装成功----'
        self.log.info(text)
        preinstall_cmd = f"cd {self.script_path};" \
                         f"./gs_preinstall -U {self.u_name} -G {self.u_name} " \
                         f"-X {self.xml_single_path} " \
                         f"--sep-env-file={self.env_path} " \
                         f"--skip-hostname-set --non-interactive"
        self.log.info(preinstall_cmd)
        msg = self.primary_root_node.sh(preinstall_cmd).result()
        self.log.info(msg)
        self.assertIn(Constant.preinstall_success_msg, msg,
                      '执行失败:' + text)

        text = '----step5:执行gs_install安装数据库 expect:安装成功----'
        self.log.info(text)
        su_cmd = f'su - {self.u_name}'
        install_cmd = f'gs_install -X {self.xml_single_path}'
        execute_cmd = f'''expect <<EOF
                   set timeout 120
                   spawn {su_cmd}
                   expect "$"
                   send "source {self.env_path}\\n"
                   expect "$"
                   send "{install_cmd}\\n"
                   expect "Please enter password for database:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect "Please repeat for database:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        exec_msg = self.primary_root_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        self.assertIn(Constant.install_success_msg, exec_msg, text + '执行失败')

        text = '----step6:建立与待扩容备机root及用户互信 expect:成功----'
        self.log.info(text)
        text = '----创建hostfile文件，添加主备IP信息,并修改文件属性----'
        self.log.info(text)
        add_cmd = f'source {self.env_path};' \
                  f'touch {self.ssh_file};' \
                  f'chmod -R 755 {self.ssh_file};' \
                  f"echo -e '{self.pri_host}\n{self.sta_host}\n" \
                  f"{self.sta2_host}' > {self.ssh_file};" \
                  f"chown {self.u_name}:{self.u_name} {self.ssh_file};" \
                  f"cat {self.ssh_file}"
        self.log.info(add_cmd)
        add_res = self.primary_root_node.sh(add_cmd).result()
        self.log.info(add_res)
        self.assertIn(self.pri_host and self.sta_host and self.sta2_host,
                      add_res, 'hostfile创建失败')
        self.log.info('----执行gs_sshexkey命令建立root互信----')
        ssh_root_cmd = f'./gs_sshexkey -f {self.ssh_file};'
        root_execute_cmd = f'''cd {self.script_path}
            expect <<EOF
            set timeout 120
            spawn {ssh_root_cmd}
            expect "*assword:"
            send "{self.primary_root_node.ssh_password}\\n"
            expect eof\n''' + '''EOF'''
        self.log.info(root_execute_cmd)
        root_ssh_res = self.primary_root_node.sh(root_execute_cmd).result()
        self.log.info(root_ssh_res)
        self.assertIn('Successfully created SSH trust.',
                      root_ssh_res, text + '执行失败')
        self.log.info('----执行gs_sshexkey命令建立用户互信----')
        ssh_usr_cmd = f'gs_sshexkey -f {self.ssh_file}'
        usr_execute_cmd = f'''expect <<EOF
                      set timeout 60
                      spawn {su_cmd}
                      expect "$"
                      send "source {self.env_path}\\n"
                      expect "$"
                      send "{ssh_usr_cmd}\\n"
                      expect "*assword:"
                      send "{macro.COMMON_PASSWD}\\n"
                      expect eof\n''' + '''EOF'''
        self.log.info(usr_execute_cmd)
        usr_ssh_res = self.primary_root_node.sh(usr_execute_cmd).result()
        self.log.info(usr_ssh_res)
        self.assertIn('Successfully created SSH trust.',
                      usr_ssh_res, text + '执行失败')

        text = '----step7:执行gs_expansion进行备机扩容 expect:成功'
        self.log.info(text)
        expansion_cmd = f'./gs_expansion -U {self.u_name} -G {self.u_name} ' \
                        f'-X {self.xml_expansion_path} -h {self.sta_host}'
        self.log.info(expansion_cmd)
        execute_cmd = f'''cd {self.script_path};
                           source {self.env_path};
                           expect <<EOF
                           set timeout 300
                           spawn {expansion_cmd}
                           expect "*assword*:"
                           send "{macro.COMMON_PASSWD}\\n"
                           expect "*assword*:"
                           send "{macro.COMMON_PASSWD}\\n"
                           expect "*lease repeat for database*:"
                           send "{macro.COMMON_PASSWD}\\n"
                           expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        expan_result = self.primary_root_node.sh(execute_cmd).result()
        self.log.info(expan_result)
        check_msg = f'Expansion results:\r\n' \
                    f'{self.sta_host}:\tSuccess\r\n' \
                    f'Expansion Finish.'
        self.log.info(check_msg)
        self.assertIn(check_msg, expan_result, text + '执行失败')
        self.log.info('检查是否扩容成功')
        check_cmd = f'''expect <<EOF
                           set timeout 60
                           spawn su - {self.u_name}
                           expect "$"
                           send "source {self.env_path}\\n"
                           expect "$"
                           send "gs_om -t status --detail\\n"
                           expect eof\n''' + '''EOF'''
        self.log.info(check_cmd)
        check_res = self.primary_root_node.sh(check_cmd).result()
        self.log.info(check_res)
        check_lis = [self.pri_host, self.sta_host]
        for check in check_lis:
            self.assertIn(check, check_res, '扩容后检查失败')

        text = '----step8:停止数据库主机并进行failover expect:成功----'
        self.log.info(text)
        text_1 = '----停止数据库主机----'
        self.log.info(text_1)
        execute_cmd = f'''expect <<EOF
                          set timeout 60
                          spawn su - {self.u_name}
                          expect "$"
                          send "source {self.env_path}\\n"
                          expect "$"
                          send "gs_om -t stop -h {self.pri_host}\\n"
                          expect eof\n''' + '''EOF'''
        excute_msg = self.primary_root_node.sh(execute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(Constant.STOP_NODE_SUC_MSG, excute_msg,
                      '执行失败' + text_1)
        text_2 = '----进行failover----'
        self.log.info(text)
        failover_cmd = f"gs_ctl failover -D {self.instance_path} -m fast;"
        self.log.info(failover_cmd)
        execute_cmd = f'''expect <<EOF
                          set timeout 60
                          spawn su - {self.u_name}
                          expect "$"
                          send "source {self.env_path}\\n"
                          expect "$"
                          send "{failover_cmd}\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        excute_msg = self.standby_root_node.sh(execute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(Constant.FAILOVER_SUCCESS_MSG, excute_msg,
                      '执行失败' + text_2)
        text_3 = '----进行refreshconf----'
        self.log.info(text_3)
        execute_cmd = f'''expect <<EOF
                          set timeout 60
                          spawn su - {self.u_name}
                          expect "$"
                          send "source {self.env_path}\\n"
                          expect "$"
                          send "gs_om -t refreshconf\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        excute_msg = self.standby_root_node.sh(execute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(Constant.REFRESHCONF_SUCCESS_MSG, excute_msg,
                      '执行失败' + text_3)
        text_4 = '----执行restart进行重启数据库----'
        execute_cmd = f'''expect <<EOF
                          set timeout 60
                          spawn su - {self.u_name}
                          expect "$"
                          send "source {self.env_path}\\n"
                          expect "$"
                          send "gs_om -t restart\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        res_msg = self.standby_root_node.sh(execute_cmd).result()
        self.log.info(res_msg)
        self.assertIn(Constant.STOP_SUCCESS_MSG, res_msg, text_4 + '停止失败')
        self.assertIn(Constant.START_SUCCESS_MSG, res_msg, text_4 + '启动失败')

    def tearDown(self):
        text = "----step9:卸载数据库，清理用户及文件 expect:成功----"
        self.log.info(text)
        text_1 = '----gs_uninstall卸载数据库----'
        self.log.info(text_1)
        execute_cmd = f'''expect <<EOF
                       set timeout 60
                       spawn su - {self.u_name}
                       expect "$"
                       send "source {self.env_path}\\n"
                       expect "$"
                       send "gs_uninstall --delete-data\\n"
                       expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        uninstall_msg = self.primary_root_node.sh(execute_cmd).result()
        self.log.info(uninstall_msg)
        text_2 = '-----删除用户下进程 expect:成功-----'
        self.log.info(text_2)
        kill_cmd = f"ps -u {self.u_name} | grep -v PID| " \
                   f"awk \'{{{{print $1}}}}\' | xargs kill -9;" \
                   f"ipcs -m|awk '{{{{if($3~/^[0-9]+$/) {{{{print $2}}}}}}}}'" \
                   f" | xargs -I {{{{}}}} ipcrm -m {{{{}}}};" \
                   f"ipcs -s|awk '{{{{if($3~/^[0-9]+$/) {{{{print $2}}}}}}}}'" \
                   f" | xargs -I {{{{}}}} ipcrm -s {{{{}}}};sync;" \
                   f"echo 3 > /proc/sys/vm/drop_caches"
        self.log.info(kill_cmd)
        self.common.get_sh_result(self.primary_root_node, kill_cmd)
        self.common.get_sh_result(self.standby_root_node, kill_cmd)
        text_3 = '----删除用户及数据准备目录 expect:成功----'
        self.log.info(text_3)
        dir_del_cmd = f'rm -rf {self.openGauss_path}'
        self.primary_root_node.sh(dir_del_cmd).result()
        self.standby_root_node.sh(dir_del_cmd).result()
        check_cmd = f'if [ -d {self.openGauss_path} ]; ' \
                    f'then echo "exists"; else echo "not exists"; fi'
        self.log.info(check_cmd)
        pri_del_dir_msg = self.common.get_sh_result(self.primary_root_node,
                                                    check_cmd)
        sta_del_dir_msg = self.common.get_sh_result(self.standby_root_node,
                                                    check_cmd)
        usr_del_cmd = f'userdel -rf {self.u_name};id {self.u_name}'
        pri_del_usr_msg = self.primary_root_node.sh(usr_del_cmd).result()
        sta_del_usr_msg = self.standby_root_node.sh(usr_del_cmd).result()
        sta2_del_usr_msg = self.standby2_root_node.sh(usr_del_cmd).result()
        self.assertIn(Constant.uninstall_success_msg, uninstall_msg,
                      '执行失败:' + text_1)
        self.assertEqual('not exists', pri_del_dir_msg, '执行失败:' + text_3)
        self.assertEqual('not exists', sta_del_dir_msg, '执行失败:' + text_3)
        for msg in [pri_del_usr_msg, sta_del_usr_msg, sta2_del_usr_msg]:
            self.log.info(msg)
            self.assertIn('no such user', msg, '用户删除失败' + text_3)
        self.log.info(f'----{os.path.basename(__file__)} finish----')

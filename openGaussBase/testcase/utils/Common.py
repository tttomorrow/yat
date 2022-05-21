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
public function
"""
import os
import random

from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Common:
    def __init__(self, node_name='dbuser'):
        # root用户还是数据库安装的用户执行脚本。数据库用户默认dbuser（见conf/nodes.yml）
        self.logger = Logger()
        self.Constant = Constant()
        self.sh_primy = CommonSH(node_name)

    def console(self, msg):
        """
        打印关键日志
        :param msg: 需要打印的信息
        """
        self.logger.info("---- {} ----".format(msg))

    def start_tpcc(self, db_node, tpcc_path,
                   tpcc_command='. runBenchmark.sh props.pg'):
        """
        执行TPCC
        :param db_node: 传入节点，一般是root节点
        :param tpcc_path: tpcc路径
        :param tpcc_command: tpcc指令
        :return: 返回tpcc_res
        """
        start_tpcc = f"source /etc/profile; cd {tpcc_path}; {tpcc_command}"
        self.console(start_tpcc)
        result = db_node.sh(start_tpcc).result()
        return result

    @staticmethod
    def file_find_string(file_path, content):
        """
        文件中查找字符串
        :param file_path: 文件路径
        :param content: 字符串内容
        :return: 查找到则返回True，否则返回False
        """
        # 注意这里的打开文件编码方式
        with open(file_path, "r", encoding='UTF-8') as fp:
            strr = fp.read()
            if strr.find(content) != -1:
                return True

    def get_file_string_rows(self, node, file_path, content):
        """
        获取文件中字符串匹配的所有行
        :param node: 传入节点
        :param file_path: 文件路径
        :param content: 字符串内容
        :return: 文件中字符串匹配的所有行
        """
        cmd = f"sed -n '/{content}/p' {file_path}"
        self.console(cmd)
        msg = node.sh(cmd).result()
        return msg

    def replace_file_content_by_sed(self, node, file_path, old_str, new_str):
        """
        替换文件内容，可指定node
        :param node: 传入节点
        :param file_path: 文件路径
        :param old_str: 原字符串
        :param new_str: 目标字符串
        :return: 执行结果
        """
        cmd = f"""sed -i "s/{old_str}/{new_str}/g" {file_path}"""
        self.console(cmd)
        msg = node.sh(cmd).result()
        return msg

    @staticmethod
    def replace_file_content(file_path, old_str, new_str):
        """
        替换文件内容，不可指定node
        :param file_path: 文件路径
        :param old_str: 原字符串
        :param new_str: 目标字符串
        """
        file_data = ""
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str, new_str)
                file_data += line
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_data)

    @staticmethod
    def trans_num_to_alp(origin_str):
        """
        转换数字为字母
        :param origin_str: 需要转换的字符串
        :return: 返回转换后的字符串
        """
        trantab = str.maketrans('1234567890', 'abcdefghij')
        des_str = origin_str.translate(trantab)
        return des_str

    def kill_pid(self, node, sigterm):
        """
        获取进程pid并接受kill信号
        :param node: 传入节点
        :param sigterm: kill信息，如9杀死一个进程
        :return: 执行结果
        """
        pid_list = []
        kill_cmd = ''
        cmd = f"lsof -i:{node.db_port}"
        self.console(cmd)
        msg = node.sh(cmd).result()
        self.console(msg)

        pid_lines = msg.strip().splitlines()
        for i in pid_lines:
            pid_line = i.strip().split()
            if pid_line[1].isnumeric():
                pid_list.append(pid_line[1])

        for pid in pid_list:
            kill_cmd += f"kill -{sigterm} {pid};"
        self.console(kill_cmd)
        msg = node.sh(kill_cmd).result()
        self.console(msg)
        return msg

    def mod_file_rows(self, node, file_path, start_row, end_row, contant):
        """
        修改文件中的某些行内容
        :param node: 传入节点
        :param file_path: 文件路径
        :param start_row: 起始行
        :param end_row: 结束行
        :param contant: 要修改为的内容
        :return: 执行结果
        """
        cmd = f"sed -i '{start_row},{end_row}c {contant}' {file_path};"
        self.console(cmd)
        msg = node.sh(cmd).result()
        self.console(msg)
        return msg

    def file_sql_execute(self, node, sqlfile, count):
        """
        执行sql脚本文件count次
        :param node: 节点
        :param sqlfile: sql文件路径
        :param count: 执行次数
        :return:
        """
        for i in range(count):
            filesql_cmd = f"source {macro.DB_ENV_PATH};" \
                          f"gsql -d {node.db_name} \
                                    -p {node.db_port}  -r -f {sqlfile}"
            msg = node.sh(filesql_cmd).result()
            self.console('sqlexecute result: ' + msg)

    def scp_file(self, node, file_name, target_path, del_sign=False):
        """
        传输当前主机上的文件到node所在主机target_path下
        :param node: 目标节点
        :param file_name: 文件名
        :param target_path: 目标主机上的路径
        :param del_sign: 删除标志位
        :return:
        """
        # 获取传输文件路径
        filepath_1 = os.path.join(macro.SCRIPTS_PATH, file_name)
        # 传输文件至目标主机
        newsql_path1 = os.path.join(target_path, file_name)

        if not del_sign:
            mkdir_cmd = f'if [ ! -d {target_path} ];' \
                        f'then mkdir {target_path};fi'
            self.console(mkdir_cmd)
            msg = node.sh(mkdir_cmd).result()
            self.console(msg)

            self.console('filepath_1:' + filepath_1)
            self.console('newsql_path1:' + newsql_path1)

            cmd = f'ls {newsql_path1}'
            self.console(cmd)
            msg = node.sh(cmd).result()
            if self.Constant.NO_FILE_MSG not in msg:
                cmd = f'rm -rf {newsql_path1}'
                self.console(cmd)
                msg = node.sh(cmd).result()
                self.console(msg)
            node.scp_put(filepath_1, newsql_path1)
        else:
            # 删除scp的脚本文件
            rm_sqlfile = f'rm -rf {newsql_path1}'
            self.console(rm_sqlfile)
            msg = node.sh(rm_sqlfile).result()
            self.console(msg)

    def equal_sql_mdg(self, result: str, *expect, flag=''):
        """
        一般用来判断执行结果与预期结果是否相同
        :param result: 执行结果, 未用split分隔
        :param expect: 预期结果, 以元组的形式传入
        :param flag: 删除执行结果split分隔后的第flag个元素
        :return: 无
        """

        res_list = result.splitlines()
        self.logger.info(res_list)
        if flag:
            del res_list[int(flag)]
        # 判断执行结果和预期结果长度一致
        assert len(expect) == len(res_list)
        for i in range(len(expect)):
            assert expect[i].strip() == res_list[i].strip()

    def config_set_modify(self, configitem, node='all'):
        # 设置参数
        self.sh_primy.execute_gsguc('set',
                                    self.Constant.GSGUC_SUCCESS_MSG,
                                    configitem, node)
        # 重启数据库使参数生效
        stopmsg = self.sh_primy.stop_db_cluster()
        startmsg = self.sh_primy.start_db_cluster()
        return stopmsg, startmsg

    @staticmethod
    def format_sql_result(msg):
        value_list = []
        header_line = ''
        result_dict = {}
        result_lines = msg.strip().splitlines()
        for line in result_lines:
            if '-------' in line:
                divider_index = result_lines.index(line)
                header_line = result_lines[divider_index - 1].strip()
                for i in range(divider_index + 1, len(result_lines)):
                    value_list.append(result_lines[i].strip())

        header_line = header_line.split('|')
        for i in range(len(header_line)):
            result_dict[f'{header_line[i].strip()}'] = []
            if '(' in msg and 'row' in msg and ')' in msg:
                value_list_len = len(value_list) - 1
            else:
                value_list_len = len(value_list)
            for j in range(value_list_len):
                if '|' in value_list[j]:
                    result_dict[f'{header_line[i].strip()}'].append(
                        value_list[j].split('|')[i].strip())

        return result_dict

    def get_node_num(self, node):
        """
        function:获取数据库集群节点个数
        :param node: 传入集群中任意节点即可
        :return: 节点个数
        """
        conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                 macro.DB_PG_CONFIG_NAME)
        shell_cmd = f"cat {conf_path} |grep 'pgxc_node_name'|" \
                    f"cut -d '=' -f 2|cut -d '#' -f 1"
        self.logger.info(shell_cmd)
        msg = node.sh(shell_cmd).result()
        self.logger.info(msg)
        node_list = msg.strip('\'').strip('dn_').split('_')
        self.logger.info(node_list)
        node_num = len(node_list)
        return node_num

    def get_sh_result(self, node, cmd):
        """
        function:获取sh结果
        :param node: 节点信息
        :param cmd: 执行指令
        :return: sh回显结果
        """
        result = node.sh(cmd).result()
        self.logger.info(result)
        return result

    def scp_from_standby_to_primary(self, source_path, target_path, pri_node):
        conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                 macro.DB_PG_CONFIG_NAME)
        self.logger.info('----获取备节点ip----')
        shell_cmd = f"cat {conf_path} | " \
                    f"grep 'replconninfo' | " \
                    f"grep -Ev '^#' | " \
                    f"tr -s ' '| " \
                    f"cut -d ' ' -f 7 | " \
                    f"cut -d '=' -f 2"
        self.logger.info(shell_cmd)
        msg = pri_node.sh(shell_cmd).result()
        self.logger.info(msg)
        standby_ip_list = msg.splitlines()

        self.logger.info('----查看文件是否存在----')
        scp_cmd = f"scp -r {source_path} " \
                  f"root@{pri_node.db_host}:{target_path}"
        for ip in standby_ip_list:
            shell_cmd = f'''ssh {ip} <<-EOF
                ls -al {source_path}
                exit\n''' + "EOF"
            self.logger.info(shell_cmd)
            msg = pri_node.sh(shell_cmd).result()
            if 'No such file or directory' not in msg:
                shell_cmd = f'''ssh {ip} <<-EOF
                    {scp_cmd}
                    exit\n''' + "EOF"
                self.logger.info(shell_cmd)
                msg = pri_node.sh(shell_cmd).result()
                self.logger.info(msg)
                break

    def ln_odbc_lib(self, node):
        """
        function:给lib下以来库创建软链接
        :param node: 节点信息
        :return: 结果信息为空，则返回True
        """
        exe_cmd1 = "ldconfig"
        self.logger.info(exe_cmd1)
        msg1 = node.sh(exe_cmd1).result()
        self.logger.info(msg1)
        if msg1.find("is not a symbolic link"):
            lib_list = [i for i in msg1.splitlines() if i != '']
            for item in lib_list:
                old_lib_name = item.strip()
                lib_name = old_lib_name[9:-23]
                ln_lib_name = lib_name[:-4] + lib_name[-1:] + '.so'
                ln_cmd = f"ln -s {lib_name} {ln_lib_name}"
                self.logger.info(ln_cmd)
                ln_msg = node.sh(ln_cmd).result()
                self.logger.info(ln_msg)
        else:
            return True

    def show_param(self, guc_param, env_path=macro.DB_ENV_PATH):
        """
        function:查看guc参数默认值
        :param guc_param: guc参数
        :param env_path: 环境变量路径
        :return: 返回参数默认值
        """
        check_default = f'show {guc_param};'
        default_msg = self.sh_primy.execut_db_sql(check_default, '',
                                                  None, env_path)
        self.logger.info(default_msg)
        default_msg_list = default_msg.splitlines()[2].strip()
        self.logger.info(default_msg_list)
        return default_msg_list

    def install_odbc(self, node, path, assert_flag):
        """
        function:安装unixODBC
        :param node: 节点信息
        :param path: odbc包解压路径
        assert_flag: 判断是否执行成功
        """
        unixodbc_version = 'unixODBC'
        unixodbc_devel = 'unixODBC-devel'
        odbc_pkg = os.path.join(macro.DB_SCRIPT_PATH, "..", macro.ODBC_NAME)
        check_msg = node.sh('rpm -qa |egrep ODBC').result()
        self.logger.info(check_msg)
        if 'unixODBC' in check_msg and check_msg.count('unixODBC') == 2:
            self.logger.info('----unixODBC 已安装----')
        else:
            self.check_yum_python(node)
            install_cmd = f'yum install -y {unixodbc_version};' \
                f'yum install -y {unixodbc_devel}'
            install_msg = node.sh(install_cmd).result()
            self.logger.info(install_msg)
            assert install_msg.find(assert_flag) > -1
        check_odbc = f'ls ' \
            f'{os.path.join(macro.DB_SCRIPT_PATH, "..", macro.ODBC_NAME)}'
        tar_msg = node.sh(check_odbc).result()
        self.logger.info(tar_msg)
        if 'No such file or directory' in tar_msg:
            node.scp_put(odbc_pkg, odbc_pkg)
        tar_cmd = f'mkdir -p {path}; ' \
                  f'tar -zxvf {odbc_pkg} -C {path}'
        self.logger.info(tar_cmd)
        tar_msg = node.sh(tar_cmd).result()
        self.logger.info(tar_msg)

    def check_libfile(self, node, lib_file, local_path):
        """
        function:检查依赖库是否存在
        :param node: 节点信息
        :param lib_file: 依赖库文件
        :param local_path: 依赖库文件存放路径
        """
        error_msg = 'not found'
        while True:
            self.logger.info('----开始检查依赖库是否存在----')
            exe_cmd6 = f'ldd {lib_file}'
            self.logger.info(exe_cmd6)
            msg6 = node.sh(exe_cmd6).result()
            self.logger.info(msg6)
            msg6_list = msg6.splitlines()
            if error_msg in msg6:
                self.logger.info('----获取所有未找到的依赖库----')
                for item in msg6_list:
                    if error_msg in item:
                        item_list = item.split('=>')
                        libfile = item_list[0].strip()
                        libfile_name = os.path.join(local_path, libfile)
                        exe_cmd7 = f'cp {libfile_name} /lib64'
                        self.logger.info(exe_cmd7)
                        msg7 = node.sh(exe_cmd7).result()
                        self.logger.info(msg7)
            else:
                break

    def check_load_msg(self, root_node, node, pkg_path, conf_path):
        """
        function:下载数据库安装包
        :param root_node: root节点信息
        :param node: 数据库节点信息
        :param pkg_path: 数据库package路径 例 xxx/dir_xxx_0001/pkg
        :param conf_path: 数据库配置文件(env,xml等)路径,方法中会创建此路径,用例中无需额外创建
                        例 xxx/dir_xxx_0001/conf
        """
        self.logger.info('----查询系统和数据库版本----')
        os_cpu = root_node.sh('cat /etc/*release;'
                              'uname -a').result()
        self.logger.info(os_cpu)
        find_cmd = f'source {macro.DB_ENV_PATH};' \
                   f'gaussdb -V'
        find_ver_msg = node.sh(find_cmd).result()
        self.logger.info(find_ver_msg)
        assert find_ver_msg.find('compiled at') > -1
        db_release_version = find_ver_msg.split()[2]

        self.logger.info('----获取安装包地址----')
        packages_tgz_name = f'openGauss_{db_release_version}_PACKAGES_' \
                            f'RELEASE.tar.gz'
        package_url = ''
        om_tgz_name = ''
        if 'CentOS Linux 7 (Core)' in os_cpu:
            package_url = os.path.join(macro.FTP_PATH, 'CentOS7.6',
                                       packages_tgz_name)
            om_tgz_name = f'openGauss-{db_release_version}-CentOS-' \
                          f'64bit-om.tar.gz'
        elif 'openEuler 20.03 (LTS)' in os_cpu:
            om_tgz_name = f'openGauss-{db_release_version}-openEuler-' \
                          f'64bit-om.tar.gz'
            if 'x86_64' in os_cpu:
                package_url = os.path.join(macro.FTP_PATH,
                                           'OpenEuler20.03_X86',
                                           packages_tgz_name)
            elif 'aarch64' in os_cpu:
                package_url = os.path.join(macro.FTP_PATH,
                                           'OpenEuler20.03',
                                           packages_tgz_name)
        else:
            self.logger.info("获取安装包地址失败！")
        assert package_url != ''

        self.logger.info('----下载解压数据库安装包----')
        load_cmd = f"rm -rf {os.path.dirname(pkg_path)};" \
                   f"mkdir -p {pkg_path} {conf_path};" \
                   f"cd {pkg_path};" \
                   f"wget {package_url} -c -t2 -T30;" \
                   f"tar -zxf {packages_tgz_name};" \
                   f"tar -zxf {om_tgz_name} -C {pkg_path}"
        self.logger.info(load_cmd)
        exec_msg = root_node.sh(load_cmd).result()
        self.logger.info(exec_msg)
        assert exec_msg.find(f"‘{packages_tgz_name}’ saved") > -1
        assert exec_msg.find(self.Constant.NO_FILE_MSG) == -1

    @staticmethod
    def get_not_used_port(node):
        """
        function:查找系统未使用端口
        :param node: 数据库节点信息
        :return: 返回端口号
        """
        port = 0
        for i in range(65535):
            port_tmp = random.randint(40000, 49999)
            check_cmd = f'lsof -i:{str(port_tmp)}'
            check_result = node.sh(check_cmd).result()
            if str(port_tmp) not in check_result:
                port = port_tmp
                break
        return port

    def create_user(self, root_node, u_name):
        """
        function:创建新用户并修改密码
        :param root_node: root节点信息
        :param u_name: 用户名
        """
        self.logger.info('----创建初始用户并修改密码----')
        user_cmd = f"userdel -r {u_name};" \
                   f"groupadd {u_name};" \
                   f"useradd -g {u_name} {u_name};"
        passwd_cmd = f'passwd {u_name}'
        execute_cmd = f'''{user_cmd}
                   expect <<EOF
                   set timeout 30
                   spawn {passwd_cmd}
                   expect "New password:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect "Retype new password:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect eof\n''' + '''EOF'''
        self.logger.info(execute_cmd)
        user_res = root_node.sh(execute_cmd).result()
        self.logger.info(user_res)
        assert user_res.find(self.Constant.passwd_success_msg) > -1

    def odbc_symbolic_link(self, node, lib_path, ld_path):
        """
        function:检查是否需要给动态库创建软链接
        :param node: 节点信息
        :param lib_path: 动态库的路径
        :param ld_path: /etc/ld.so.conf文件
        """
        write_content = 'include ld.so.conf.d/*.conf\n' \
                        f'{lib_path}'
        write_cmd = f"echo '{write_content}' > {ld_path}"
        self.logger.info(write_cmd)
        write_msg = node.sh(write_cmd).result()
        self.logger.info(write_msg)
        load_cmd = 'ldconfig'
        load_msg = node.sh(load_cmd).result()
        self.logger.info(load_msg)
        if load_msg.find('is not a symbolic link'):
            load_msg_list = load_msg.splitlines()
            for item in load_msg_list:
                if 'is not a symbolic link' in item:
                    ln_file_path = item[10:][:-23]
                    ln_file = ln_file_path[:-4] + ln_file_path[-1] + '.so'
                    ln_cmd = f"ln -s {ln_file_path} {ln_file}"
                    self.logger.info(ln_cmd)
                    ln_msg = node.sh(ln_cmd).result()
                    self.logger.info(ln_msg)
        load_msg2 = node.sh(load_cmd).result()
        self.logger.info(load_msg2)
        return load_msg2

    def set_odbc_ini(self, node, ini_content, config_path):
        """
        创建ODBC驱动连接所需文件odbc.ini
        :param node: 执行机节点
        :param ini_content: odbc.ini文件内容
        :param config_path: ODBC配置文件所在路径
        :return: 配置文件创建成功返回True，否则返回False
        """
        odbc_content = f'[gaussodbc]\n' \
                       f'Driver=PostgreSQL\n' \
                       f'Servername={ini_content[0]}\n' \
                       f'Database={ini_content[1]}\n' \
                       f'Username={ini_content[2]}\n' \
                       f'Password={ini_content[3]}\n' \
                       f'Port={ini_content[4]}\n' \
                       f'ReadOnly=No\n'
        self.logger.info(odbc_content)
        write_odbc = f"echo '{odbc_content}' > " \
                     f"{os.path.join(config_path, 'odbc.ini')}"
        self.logger.info(write_odbc)
        write_res = node.sh(write_odbc).result()
        self.logger.info(write_res)
        if len(write_res) > 0:
            return False
        return True

    def set_odbcinst_ini(self, node, config_path, local_lib_path):
        """
        创建ODBC驱动连接所需文件odbcinst.ini
        :param node: 执行机节点
        :param config_path: ODBC配置文件所在路径
        :param local_lib_path: ODBC驱动依赖库路径
        :return: 配置文件创建成功返回True，否则返回False
        """
        odbcinst_content = f'[PostgreSQL]\n' \
            f'Driver64={os.path.join(local_lib_path, "psqlodbcw.so")}\n' \
            f'Setup={os.path.join(local_lib_path, "psqlodbcw.so")}\n'
        self.logger.info(odbcinst_content)
        write_odbcinst = f"echo '{odbcinst_content}' > " \
            f"{os.path.join(config_path, 'odbcinst.ini')}"
        self.logger.info(write_odbcinst)
        write_res = node.sh(write_odbcinst).result()
        self.logger.info(write_res)
        if len(write_res) > 0:
            return False
        return True

    def set_odbc_src(self, node, config_path, local_lib_path, sourcefile):
        """
        创建ODBC驱动环境变量配置文件
        :param node: 执行机节点
        :param config_path: ODBC配置文件所在路径
        :param local_lib_path: ODBC驱动依赖库路径
        :param sourcefile: ODBC驱动环境变量文件路径
        :return: 环境变量文件创建成功返回True，否则返回False
        """
        export_content = f'export ' \
            f'LD_LIBRARY_PATH={local_lib_path}:' \
            f'{os.path.join(config_path, "lib")}:$LD_LIBRARY_PATH;\n' \
            f'export ODBCSYSINI={config_path};\n' \
            f'export ODBCINI={os.path.join(config_path, "odbc.ini")}\n'
        write_export = f"echo '{export_content}' > {sourcefile}"
        self.logger.info(write_export)
        write_res = node.sh(write_export).result()
        self.logger.info(write_res)
        if len(write_res) > 0:
            return False
        return True

    def check_yum_python(self, node):
        """
        检查yum环境是否有问题
        :param node: 执行机节点
        :return: 返回两个参数，yum没问题返回(True,"")，否则返回
        (是否执行成功,/usr/bin/yum第一行)
        """
        check_cmd = f"yum list *jdk*"
        self.logger.info(check_cmd)
        check_res = node.sh(check_cmd).result()
        self.logger.info(check_res)
        if "except KeyboardInterrupt" in check_res:
            python_cmd = f"head -1 /usr/bin/yum"
            python_res = node.sh(python_cmd).result()
            self.logger.info(python_res)
            if "python" not in python_res:
                return False
            change_cmd = f"sed -i '1s/.*/\#\!\/usr\/bin\/python2/' " \
                         f"/usr/bin/yum"
            self.logger.info(change_cmd)
            change_res = node.sh(change_cmd).result()
            if len(change_res) != 0:
                return False
            python_cmd = f"head -1 /usr/bin/yum"
            python_res = node.sh(python_cmd).result()
            self.logger.info(python_res)
            if python_res != "#!/usr/bin/python2":
                return False
        else:
            return True
        return True

    def do_install(self, root_node, env_path, install_cmd):
        """
        function:gs_install安装数据库
        :param root_node: root信息
        :param env_path: env文件路径
        :param install_cmd: 安装命令
        :return: 返回安装过程信息
        """
        execute_cmd = f'''source {env_path}
                   expect <<EOF
                   set timeout 120
                   spawn {install_cmd}
                   expect "Please enter password for database:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect "Please repeat for database:"
                   send "{macro.COMMON_PASSWD}\\n"
                   expect eof\n''' + '''EOF'''
        self.logger.info(execute_cmd)
        exec_msg = root_node.sh(execute_cmd).result()
        self.logger.info(exec_msg)
        return exec_msg

    def find_pglog_content(self, node, content, env_path,
                           dn_name='', detail=False, path=''):
        """
        在最新的pg_log中查找content，找到返回True，未找到返回False
        :param node: 查询pg_log节点
        :param dn_name: 数据库dn名称dn_6001
        :param content: 查找内容
        :param env_path: 环境变量路径
        :return:
        """
        if '' == path:
            pg_log = os.path.join('$GAUSSLOG', 'pg_log', dn_name)
        else:
            pg_log = path
        cmd = f'source {env_path};' \
            f'find {pg_log} -iname "post*" -mmin -2 | xargs ls -lta '
        self.logger.info(cmd)
        result = node.sh(cmd).result()
        self.logger.info(result)
        current_log = result.splitlines()[0].split(" ")[-1]
        cmd = f'cat {current_log} | grep \'{content}\''
        self.logger.info(cmd)
        result = node.sh(cmd).result()
        self.logger.info(result)
        if detail:
            return result
        else:
            if content in result:
                return True
            else:
                return False

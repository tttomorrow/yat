"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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

from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Common:
    def __init__(self):
        # 通过root用户还是数据库安装的用户执行脚本。 数据库部署用户默认使用dbuser（见 conf/nodes.yml）
        self.logger = Logger()
        self.Constant = Constant()
        self.sh_primy = CommonSH()

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
            mkdir_cmd = f'mkdir {target_path}'
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

    def equal_sql_mdg(self, sql_mdg, *args, flag=''):
        j = 0
        sql_list = sql_mdg.splitlines()
        self.logger.info(sql_list)
        if flag == '1':
            del sql_list[1]
        if len(args) == len(sql_list):
            self.logger.info(f'{len(args)} = {len(sql_list)}')
        else:
            self.logger.error(f'{len(args)} != {len(sql_list)}')
            raise Exception('请检查长度')
        for i in args:
            sqlmsg = sql_list[j].strip()
            if i == sqlmsg:
                self.logger.info(f'{i} == {sqlmsg}')
                j += 1
            else:
                self.logger.error(f'{i} != {sqlmsg}')
                raise Exception('请检查值')

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

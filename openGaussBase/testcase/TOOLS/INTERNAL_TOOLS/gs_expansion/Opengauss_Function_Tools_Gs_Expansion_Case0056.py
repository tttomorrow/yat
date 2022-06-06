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
Case Type   : gs_expansion
Case Name   : 修复了xml文件中包含，但-h参数未指定节点被扩容
Description :
    1、准备扩容所用的XML文件，-h参数包含节点是xml中新增节点的真子集
    2、执行整个扩容流程
    3、查看扩容后集群情况
Expect      :
    1、准备xml成功
    2、扩容成功
    3、扩容后集群新增节点仅包含-h指定的节点
History     :
"""
import os
import re
import unittest

from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Pri_U_SH = CommonSH('PrimaryDbUser')
Node_Num = Pri_U_SH.get_node_num()


@unittest.skipIf(3 > Node_Num, '不满足一主两备环境跳过')
class GsExpansion56(unittest.TestCase):
    def setUp(self):
        self.sh = {'pri_root': CommonSH('PrimaryRoot'),
                   'sta1_user': CommonSH('Standby1DbUser'),
                   'sta2_user': CommonSH('Standby2DbUser')}
        self.log = Logger()
        self.cons = Constant()
        self.com = Common()
        self.hosts = (Pri_U_SH.node.ssh_host,
                      self.sh.get("sta1_user").node.ssh_host,
                      self.sh.get("sta2_user").node.ssh_host)
        self.exp_expect = 'Expansion results:.*:.*Success.*Expansion Finish.'
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = f'----前置检查：集群状态正常----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        regex_res = re.findall('(instance_state.*:.*Normal)', res)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), Node_Num, f'执行失败: {text}')

        text = '----前置操作: 一主两备减容两备 expect: 成功----'
        self.log.info(text)
        expect_msg = 'Success to drop the target nodes'
        shell_cmd = f'''source {macro.DB_ENV_PATH};
                    expect <<EOF
                    set timeout 300
                    spawn gs_dropnode -U {Pri_U_SH.node.ssh_user} \
                    -G {Pri_U_SH.node.ssh_user} \
                    -h {self.hosts[1]},{self.hosts[2]}
                    expect {{{{
                        "*(yes/no)?" {{{{ send "yes\\n";exp_continue }}}}
                        eof
                    }}}}''' + "\nEOF\n"
        self.log.info(shell_cmd)
        res = self.com.get_sh_result(Pri_U_SH.node, shell_cmd)
        self.assertIn(expect_msg, res, f'执行失败: {text}')

        text = '----前置操作: 数据库主机解压安装包，以免找不到扩容脚本 expect: 成功----'
        self.log.info(text)
        cmd = f'cd {os.path.dirname(macro.DB_SCRIPT_PATH)} && ' \
            f'tar -xf openGauss-Package-bak*.tar.gz && ' \
            f'ls {macro.DB_SCRIPT_PATH}|grep gs_sshexkey'
        self.log.info(cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node, cmd)
        self.assertEqual(res, 'gs_sshexkey', f'执行失败: {text}')

        text = '----前置操作: 建立root互信 expect: 成功----'
        self.log.info(text)
        self.hosts = (self.sh.get("pri_root").node.ssh_host,
                      self.sh.get("sta1_user").node.ssh_host,
                      self.sh.get("sta2_user").node.ssh_host)
        self.params = {'-f': 'expansion_28_hosts'}
        res = self.sh['pri_root'].exec_gs_sshexkey(macro.DB_SCRIPT_PATH,
                                                   *self.hosts,
                                                   **self.params)
        self.assertIn('Successfully created SSH trust', res,
                      f'执行失败: {text}')

    def test_1(self):
        text = '----step1: 准备扩容所用的XML文件，' \
               '-h参数包含节点是xml中新增节点的真子集(延用安装时xml) expect: 成功----'
        self.log.info(text)
        self.xml_path = macro.DB_XML_PATH

        text = '----step2: 执行整个扩容流程 expect: 扩容成功----'
        self.log.info(text)
        self.expansion_cmd = f'cd {macro.DB_SCRIPT_PATH};' \
            f'source {macro.DB_ENV_PATH}\n' \
            f'./gs_expansion -U {Pri_U_SH.node.ssh_user} ' \
            f'-G {Pri_U_SH.node.ssh_user} -X {macro.DB_XML_PATH} ' \
            f'-h {self.sh.get("sta2_user").node.ssh_host} -L'
        self.log.info(self.expansion_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node,
                                     self.expansion_cmd)
        regex_res = re.search(self.exp_expect, res, re.S)
        self.assertIsNotNone(regex_res, f'执行失败: {text}')

        text = f'----step2: 查看扩容后集群情况 expect: 扩容后集群新增节点仅包含-h指定的节点----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        self.assertIn(self.sh.get("sta2_user").node.ssh_host, res,
                      f'执行失败: {text}')
        self.assertNotIn(self.sh.get("sta1_user").node.ssh_host, res,
                         f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        text1 = '----后置操作: 扩容备1恢复集群 expect: 成功----'
        self.log.info(text1)
        self.expansion_cmd = self.expansion_cmd.replace(
            self.sh.get("sta2_user").node.ssh_host,
            self.sh.get("sta1_user").node.ssh_host)
        self.log.info(self.expansion_cmd)
        res1 = self.com.get_sh_result(self.sh.get("pri_root").node,
                                      self.expansion_cmd)
        regex_res1 = re.search(self.exp_expect, res1, re.S)

        text2 = f'----检查集群状态是否正常----'
        self.log.info(text2)
        res2 = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res2)
        regex_res2 = re.findall('(instance_state.*:.*Normal)', res2)
        self.log.info(regex_res2)

        if len(regex_res2) != Node_Num:
            regex_res3 = None
            regex_res4 = None
            if self.sh.get("sta1_user").node.ssh_host not in res2:
                self.expansion_cmd = self.expansion_cmd.replace(
                    self.sh.get("sta2_user").node.ssh_host,
                    self.sh.get("sta1_user").node.ssh_host)
                self.log.info(self.expansion_cmd)
                res3 = self.com.get_sh_result(self.sh.get("pri_root").node,
                                              self.expansion_cmd)
                regex_res3 = re.search(self.exp_expect, res3, re.S)
            if self.sh.get("sta2_user").node.ssh_host not in res2:
                self.expansion_cmd = self.expansion_cmd.replace(
                    self.sh.get("sta1_user").node.ssh_host,
                    self.sh.get("sta2_user").node.ssh_host)
                self.log.info(self.expansion_cmd)
                res4 = self.com.get_sh_result(self.sh.get("pri_root").node,
                                              self.expansion_cmd)
                regex_res4 = re.search(self.exp_expect, res4, re.S)
            flag = regex_res3 is not None or regex_res4 is not None
            self.assertTrue(flag, f'执行失败: {text1}')

        self.assertIsNotNone(regex_res1, f'执行失败: {text1}')
        self.assertEqual(len(regex_res2), Node_Num, f'执行失败: {text2}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)

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
Case Name   : xml文件中指定无效AZ值，能够合理报错
Description :
    1.一主两备减容一备
    2.准备扩容所用XML文件，指定无效的AZ值（不指定AZ值）
    3.执行扩容流程
    4.修改扩容所用XML文件，指定无效的AZ值（指定其它数据类型）
    5.执行扩容流程
    6.修改扩容所用XML文件，指定有效的AZ值
    7.执行扩容流程恢复集群
    8.还原xml
Expect      :
    1.执行成功，查看集群状态一主一备正常
    2.执行成功
    3.执行失败，合理报错，提示AZ值异常
    4.执行成功
    5.执行失败，合理报错，提示AZ值异常
    6.执行成功
    7.执行成功，查看集群状态一主两备正常
    8.还原xml
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
class GsExpansion28(unittest.TestCase):
    def setUp(self):
        self.sh = {'pri_root': CommonSH('PrimaryRoot'),
                   'sta1_user': CommonSH('Standby1DbUser'),
                   'sta2_user': CommonSH('Standby2DbUser')}
        self.log = Logger()
        self.cons = Constant()
        self.com = Common()
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = '----前置检查：集群状态正常----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        regex_res = re.findall('(instance_state.*:.*Normal)', res)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), Node_Num, f'执行失败: {text}')

        text = '----前置操作：备份xml文件，teardown中用来还原----'
        self.log.info(text)
        cp_cmd = f'cp {macro.DB_XML_PATH} {macro.DB_XML_PATH}_bak'
        self.log.info(cp_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node, cp_cmd)
        self.log.info(res)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

        text = '----前置操作：数据库主机解压安装包，以免找不到扩容、建互信脚本 expect: 成功----'
        self.log.info(text)
        cmd = f'cd {os.path.dirname(macro.DB_SCRIPT_PATH)} && ' \
            f'tar -xf openGauss-Package-bak*.tar.gz && ' \
            f'ls {macro.DB_SCRIPT_PATH}|grep gs_sshexkey'
        self.log.info(cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node, cmd)
        self.assertEqual(res, 'gs_sshexkey', f'执行失败: {text}')

        text = '----前置操作：建立root互信 expect: 成功----'
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
        text = '----step1: 一主两备减容一备 expect: 成功----'
        self.log.info(text)
        expect_msg = 'Success to drop the target nodes'
        shell_cmd = f'''source {macro.DB_ENV_PATH};
            expect <<EOF
            set timeout 300
            spawn gs_dropnode -U {Pri_U_SH.node.ssh_user} \
            -G {Pri_U_SH.node.ssh_user} \
            -h {self.sh.get("sta2_user").node.ssh_host}
            expect "*(yes/no)?"
            send "yes\\n"
            expect eof''' + "\nEOF\n"
        self.log.info(shell_cmd)
        res = self.com.get_sh_result(Pri_U_SH.node, shell_cmd)
        self.assertIn(expect_msg, res, f'执行失败: {text}')

        text = '----step2: 准备扩容所用XML文件，指定无效的AZ值（不指定AZ值） expect: 成功----'
        self.log.info(text)
        sed_cmd = f'sed -i "s#\\(.*azName.*\\)#            ' \
            f'<PARAM name=\\"azName\\" value=\\"\\"/>#g" ' \
            f'{macro.DB_XML_PATH}'
        self.log.info(sed_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node, sed_cmd)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

        text = '----step3: 执行扩容流程 expect: 成功----'
        self.log.info(text)
        self.expansion_cmd = f'cd {macro.DB_SCRIPT_PATH};' \
            f'source {macro.DB_ENV_PATH}\n' \
            f'./gs_expansion -U {Pri_U_SH.node.ssh_user} ' \
            f'-G {Pri_U_SH.node.ssh_user} -X {macro.DB_XML_PATH} ' \
            f'-h {self.sh.get("sta2_user").node.ssh_host} -L'
        self.log.info(self.expansion_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node,
                                     self.expansion_cmd)
        self.assertIn('There is no information about azName', res,
                      f'执行失败: {text}')

        text = '----step4: 修改扩容所用XML文件，指定无效的AZ值（指定其它数据类型） expect: 成功----'
        self.log.info(text)
        sed_cmd = f'sed -i "s#\\(.*azName.*\\)#            ' \
            f'<PARAM name=\\"azName\\" value=\\"1.234\\"/>#g" ' \
            f'{macro.DB_XML_PATH}'
        self.log.info(sed_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node, sed_cmd)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

        text = '----step5: 执行扩容流程 expect: 执行失败，合理报错，提示AZ值异常----'
        self.log.info(text)
        self.log.info(self.expansion_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node,
                                     self.expansion_cmd)
        expect = 'azName of .* in xml is not consistent with that in cluster'
        regex_res = re.search(expect, res)
        self.assertIsNotNone(regex_res, f'执行失败: {text}')

        text = '----step6: 修改扩容所用XML文件，指定有效的AZ值 expect: 成功----'
        self.log.info(text)
        sed_cmd = f'sed -i "s#\\(.*azName.*\\)#            ' \
            f'<PARAM name=\\"azName\\" value=\\"AZ1\\"/>#g" ' \
            f'{macro.DB_XML_PATH}'
        self.log.info(sed_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node, sed_cmd)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

        text = '----step7: 执行扩容流程 expect: 成功----'
        self.log.info(text)
        self.log.info(self.expansion_cmd)
        res = self.com.get_sh_result(self.sh.get("pri_root").node,
                                     self.expansion_cmd)
        expect = 'Expansion results:.*:.*Success.*Expansion Finish.'
        regex_res = re.search(expect, res, re.S)
        self.assertIsNotNone(regex_res, f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        text8 = '----step8: 还原xml expect: 成功----'
        self.log.info(text8)
        cp_cmd = f'\\cp -r {macro.DB_XML_PATH}_bak {macro.DB_XML_PATH};' \
            f'rm -rf {macro.DB_XML_PATH}_bak'
        self.log.info(cp_cmd)
        res8 = self.com.get_sh_result(self.sh.get("pri_root").node, cp_cmd)

        text = f'----检查集群状态是否正常----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        regex_res = re.findall('(instance_state.*:.*Normal)', res)
        self.log.info(regex_res)

        if len(regex_res) != Node_Num:
            ssh_res = self.sh['pri_root'].exec_gs_sshexkey(
                macro.DB_SCRIPT_PATH, *self.hosts, **self.params)

            self.log.info(self.expansion_cmd)
            res = self.com.get_sh_result(self.sh.get("pri_root").node,
                                         self.expansion_cmd)

            expect = 'Expansion results:.*:.*Success.*Expansion Finish.'
            regex_res = re.search(expect, res, re.S)
            self.assertIsNotNone(regex_res, f'执行失败: {text}')
            self.assertIn('Successfully created SSH trust', ssh_res,
                          f'执行失败: {text}')

        self.assertEqual(len(res8), 0, f'执行失败: {text8}')
        self.assertEqual(len(regex_res), Node_Num, f'执行失败: {text}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)

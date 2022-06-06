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
Case Name   : 内核增加了连接参数Replconninfo由不空变为空的告警-3
Description :
    1.使用方式1设置最后一个连接参数由""和空之间来回切换，观察打印报警信息
    2.使用方式2设置最后一个连接参数由""和空之间来回切换，观察打印报警信息
    3.使用方式3设置最后一个连接参数由""和空之间来回切换，观察打印报警信息
    4.使用方式4设置最后一个连接参数由""和空之间来回切换，观察打印报警信息
Expect      :
    1.方式1不打印报警信息
    2.方式2不打印报警信息
    3.方式3设置不生效
    4.方式4不打印报警信息
History     :
"""
import os
import re
import time
import unittest

from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Pri_U_SH = CommonSH('PrimaryDbUser')
Node_Num = Pri_U_SH.get_node_num()


@unittest.skipIf(3 > Node_Num, '不满足一主两备环境跳过')
class GsExpansion45(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.cons = Constant()
        self.com = Common()
        self.conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = f'----前置检查：集群状态正常----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        regex_res = re.findall('(instance_state.*:.*Normal)', res)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), Node_Num, f'执行失败: {text}')

        text = f'----备份conf文件，teardown还原----'
        self.log.info(text)
        cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ssh -c "\\cp -r {self.conf_path} {self.conf_path}_bak"'
        self.log.info(cmd)
        res = Pri_U_SH.node.sh(cmd).result()
        self.log.info(res)
        self.assertIn('Successfully execute command on all nodes',
                      res,
                      f'执行失败: {text}')

    def test_1(self):
        text = '----step1: 使用方式1设置最后一个连接参数由""和空之间来回切换，观察打印报警信息' \
               ' expect: 方式1不打印报警信息----'
        self.log.info(text)
        for i in range(3):
            for param in (f"replconninfo{Node_Num-1}=''",
                          f"replconninfo{Node_Num-1}"):
                res = Pri_U_SH.execute_gsguc('set',
                                             '',
                                             param,
                                             get_detail=True)
                self.assertIn(self.cons.GSGUC_SUCCESS_MSG,
                              res,
                              f'执行失败: {text}')
                self.assertNotIn('Warning', res, f'执行失败: {text}')

    def test_2(self):
        text = '----step2: 使用方式2设置最后一个连接参数由""和空之间来回切换，观察打印报警信息' \
               ' expect: 方式2不打印报警信息----'
        self.log.info(text)
        for i in range(3):
            for param in (f"replconninfo{Node_Num-1}=''",
                          f"replconninfo{Node_Num-1}"):
                res = Pri_U_SH.execute_gsguc('reload',
                                             '',
                                             param,
                                             get_detail=True)
                self.assertIn(self.cons.GSGUC_SUCCESS_MSG,
                              res,
                              f'执行失败: {text}')
                self.assertNotIn('Warning', res, f'执行失败: {text}')

    def test_3(self):
        text = '----step3: 使用方式3设置最后一个连接参数由""和空之间来回切换，观察打印报警信息' \
               ' expect: 方式3设置不生效----'
        self.log.info(text)
        sql = f"show replconninfo{Node_Num-1}; "
        res = Pri_U_SH.execut_db_sql(sql)
        self.log.info(res)
        value = res.splitlines()[-2].strip()

        expect = f'parameter "replconninfo{Node_Num - 1}" cannot ' \
            f'be changed now'
        for i in range(3):
            for param in ("''", "'null'"):
                sql = f"set replconninfo{Node_Num - 1} to {param}; " \
                    f"show replconninfo{Node_Num - 1};"
                res = Pri_U_SH.execut_db_sql(sql)
                self.log.info(res)
                self.assertIn(expect, res, f'执行失败: {text}')
                self.assertIn(value, res, f'执行失败: {text}')

    def test_4(self):
        text = '----step4: 使用方式4设置最后一个连接参数由""和空之间来回切换，观察打印报警信息' \
               ' expect: 方式4不打印报警信息----'
        self.log.info(text)

        for i in range(3):
            for param in ("''", "' '"):
                sql = f"alter system set replconninfo{Node_Num - 1} " \
                    f"to {param}; select pg_sleep(5); " \
                    f"show replconninfo{Node_Num - 1};"
                res = Pri_U_SH.execut_db_sql(sql)
                self.log.info(res)
                self.assertIn(self.cons.alter_system_success_msg,
                              res,
                              f'执行失败: {text}')
                self.assertNotIn('Warning', res, f'执行失败: {text}')

                cmd = f'source {macro.DB_ENV_PATH};' \
                    f'gs_ssh -c "\\cp -r {self.conf_path}_bak ' \
                    f'{self.conf_path}"'
                self.log.info(cmd)
                res3 = Pri_U_SH.node.sh(cmd).result()
                self.log.info(res3)

                time.sleep(10)

                restart_res = Pri_U_SH.restart_db_cluster()
                self.assertTrue(restart_res)

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        text3 = '----step5: 使用备份文件，还原conf文件 expect: 成功----'
        self.log.info(text3)
        cmd = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_ssh -c "' \
            f'diff {self.conf_path}_bak {self.conf_path} > /dev/null; ' \
            f'if [ \\$? -eq 0 ]; ' \
            f'then echo no need to replace; ' \
            f'rm -rf {self.conf_path}_bak; ' \
            f'else echo need to replace; ' \
            f'\\cp -r {self.conf_path}_bak {self.conf_path}; ' \
            f'rm -rf {self.conf_path}_bak; fi "'
        self.log.info(cmd)
        res3 = Pri_U_SH.node.sh(cmd).result()
        self.log.info(res3)

        restart_res = ''
        if res3.count("no need to replace") != Node_Num:
            restart_res = Pri_U_SH.restart_db_cluster()

        text4 = '----step6: 查看主节点状态 expect: 状态正常----'
        self.log.info(text4)
        res4 = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res4)
        regex_res = re.findall('(instance_state.*:.*Normal)', res4)
        self.log.info(regex_res)

        start = res4.index('instance_role')
        end = res4.index('\n', start)
        state = res4[start:end].split(':')[-1].strip()

        if len(regex_res) != Node_Num:
            restart_res = Pri_U_SH.restart_db_cluster()
            self.assertTrue(restart_res)

        self.assertIn('Successfully execute command on all nodes',
                      res3,
                      f'执行失败: {text3}')
        if restart_res:
            self.assertTrue(restart_res, f'执行失败: {text3}')
        self.assertEqual(state, 'Primary', f'执行失败: {text4}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)

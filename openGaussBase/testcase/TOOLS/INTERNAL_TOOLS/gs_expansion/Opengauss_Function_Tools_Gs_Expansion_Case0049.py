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
Case Name   : 日志打印—内核状态切换
Description :
    1、修改连接参数，数据库内核切换状态为Normal，观察日志打印
    2、修改连接参数，数据库内核切换状态为Primary，观察日志打印
Expect      :
    1、日志记录了数据库内核切换为Normal
    2、日志记录了数据库内核切换为Primary
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


@unittest.skipIf(Node_Num < 2, '不满足一主一备环境跳过')
class GsExpansion49(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.cons = Constant()
        self.com = Common()
        self.conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)
        self.new_log_path = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                         'gs_expansion_case0049')
        text = f'-----{os.path.basename(__file__)} start-----'
        self.log.info(text)

        text = f'----前置检查：集群状态正常----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        regex_res = re.findall('(instance_state.*:.*Normal)', res)
        self.log.info(regex_res)
        self.assertEqual(len(regex_res), Node_Num, f'执行失败: {text}')

        text = '----集群状态正常时为P expect: 节点状态为Primary----'
        self.log.info(text)
        start = res.index('instance_role')
        end = res.index('\n', start)
        state = res[start:end].split(':')[-1].strip()
        self.assertEqual(state, 'Primary', f'执行失败: {text}')

        text = f'----备份conf文件，teardown还原----'
        self.log.info(text)
        cmd = f'\\cp -r {self.conf_path} {self.conf_path}_bak'
        self.log.info(cmd)
        res = Pri_U_SH.node.sh(cmd).result()
        self.log.info(res)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

        step_txt = '----查询log_directory初始值----'
        self.log.info(step_txt)
        result = Pri_U_SH.execut_db_sql('show log_directory;')
        self.log.info(result)
        self.old_log_path = result.strip().splitlines()[-2]
        self.log.info(self.old_log_path)

        step_txt = '----修改参数log_directory以免查询最新pg_log时受其他因素影响----'
        self.log.info(step_txt)
        msg = Pri_U_SH.execute_gsguc('reload',
                                     self.cons.GSGUC_SUCCESS_MSG,
                                     f"log_directory='{self.new_log_path}'",
                                     single=True)
        self.assertTrue(msg, '执行失败:' + step_txt)

    def test_1(self):
        text = '----step1.1: 修改连接参数 expect: 成功----'
        self.log.info(text)
        for i in range(1, Node_Num):
            cmd = f"sed -i '/replconninfo{i}/d' {self.conf_path}"
            self.log.info(cmd)
            res = self.com.get_sh_result(Pri_U_SH.node, cmd)
            self.assertEqual(len(res), 0, f'执行失败: {text}')

        res = Pri_U_SH.restart_db_cluster(get_detail=True)
        self.assertIn(self.cons.STOP_SUCCESS_MSG, res, f'执行失败: {text}')
        self.assertEqual(res.count('[SUCCESS]'), Node_Num, f'执行失败: {text}')

        text = '----step1.2: 查看状态 expect: 主节点状态切换为Normal----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        start = res.index('instance_role')
        end = res.index('\n', start)
        state = res[start:end].split(':')[-1].strip()
        self.assertEqual(state, 'Normal', f'执行失败: {text}')

        text = '----step1.3: 查看日志打印 expect: 日志记录了数据库内核切换为Normal----'
        self.log.info(text)
        ls_cmd = f'ls -t {self.new_log_path}|head -1'
        self.log.info(ls_cmd)
        log_name = self.com.get_sh_result(Pri_U_SH.node, ls_cmd)
        expect_res = "update gaussdb state file: db state(NORMAL_STATE), " \
                     "server mode(Normal)"
        cmd = f"grep '{expect_res}' " \
            f"{os.path.join(self.new_log_path, log_name)}"
        self.log.info(cmd)
        res = self.com.get_sh_result(Pri_U_SH.node, cmd)
        self.assertIn(expect_res, res, f'执行失败: {text}')

        text = '----step2.1: 修改连接参数 expect: 成功----'
        self.log.info(text)
        cmd = f'\\cp -r {self.conf_path}_bak {self.conf_path}'
        self.log.info(cmd)
        res = self.com.get_sh_result(Pri_U_SH.node, cmd)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

        step_txt = '----step2.1: 修改参数log_directory以免查询最新pg_log时受其他因素影响 ' \
                   'expect: 成功----'
        self.log.info(step_txt)
        msg = Pri_U_SH.execute_gsguc('set',
                                     self.cons.GSGUC_SUCCESS_MSG,
                                     f"log_directory='{self.new_log_path}'",
                                     single=True)
        self.assertTrue(msg, '执行失败:' + step_txt)

        res = Pri_U_SH.restart_db_cluster(get_detail=True)
        self.assertIn(self.cons.STOP_SUCCESS_MSG, res, f'执行失败: {text}')
        self.assertEqual(res.count('[SUCCESS]'), Node_Num, f'执行失败: {text}')

        text = '----step2.2: 查看状态 expect: 主节点状态切换为Primary----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        start = res.index('instance_role')
        end = res.index('\n', start)
        state = res[start:end].split(':')[-1].strip()
        self.assertEqual(state, 'Primary', f'执行失败: {text}')

        text = '----step2.3: 查看日志打印 expect: 日志记录了数据库内核切换为Primary----'
        self.log.info(text)
        self.log.info(ls_cmd)
        log_name = self.com.get_sh_result(Pri_U_SH.node, ls_cmd)
        expect_res = expect_res.replace('Normal', 'Primary')
        cmd = f"grep '{expect_res}' " \
            f"{os.path.join(self.new_log_path, log_name)}"
        self.log.info(cmd)
        res = self.com.get_sh_result(Pri_U_SH.node, cmd)
        self.assertIn(expect_res, res, f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        text5 = '----还原参数log_directory----'
        self.log.info(text5)
        res5 = Pri_U_SH.execute_gsguc('reload',
                                      self.cons.GSGUC_SUCCESS_MSG,
                                      f"log_directory='{self.old_log_path}'",
                                      single=True)

        text3 = '----step3: 使用备份文件，还原conf文件 expect: 成功----'
        self.log.info(text3)
        cmd = f'diff {self.conf_path}_bak {self.conf_path} > /dev/null; ' \
            f'if [ $? -eq 0 ]; ' \
            f'then echo no need to replace; ' \
            f'rm -rf {self.conf_path}_bak; ' \
            f'else echo need to replace; ' \
            f'\\cp -r {self.conf_path}_bak {self.conf_path}; ' \
            f'rm -rf {self.conf_path}_bak; fi'
        self.log.info(cmd)
        res3 = self.com.get_sh_result(Pri_U_SH.node, cmd)

        restart_res = ''
        if 'no need to replace' not in res3:
            restart_res = Pri_U_SH.restart_db_cluster(get_detail=True)

        text4 = '----step4: 查看主节点状态 expect: 状态正常----'
        self.log.info(text4)
        res4 = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res4)
        regex_res = re.findall('(instance_state.*:.*Normal)', res4)
        self.log.info(regex_res)

        start = res4.index('instance_role')
        end = res4.index('\n', start)
        state = res4[start:end].split(':')[-1].strip()

        if restart_res:
            self.assertTrue(res3 == 'need to replace', f'执行失败: {text3}')
            self.assertIn(self.cons.STOP_SUCCESS_MSG, restart_res,
                          f'执行失败: {text3}')
            self.assertEqual(restart_res.count('[SUCCESS]'), Node_Num,
                             f'执行失败: {text3}')
        else:
            self.assertTrue(res3 == 'no need to replace', f'执行失败: {text3}')
        self.assertEqual(len(regex_res), Node_Num, f'执行失败: {text4}')
        self.assertEqual(state, 'Primary', f'执行失败: {text4}')
        self.assertTrue(res5, f'执行失败: {text4}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)

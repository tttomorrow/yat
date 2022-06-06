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
Case Name   : 内核能根据连接参数自动切换状态-单机P切N
Description :
    1.删除数据库节点所有连接参数
    2.使用gs_ctl命令查看数据库节点状态
Expect      :
    1.执行成功,删除最后一个连接参数后，数据库打印报警信息
    2.执行成功,主节点状态切换为Normal
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
class GsExpansion37(unittest.TestCase):
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
        cmd = f'\\cp -r {self.conf_path} {self.conf_path}_bak'
        self.log.info(cmd)
        res = Pri_U_SH.node.sh(cmd).result()
        self.log.info(res)
        self.assertEqual(len(res), 0, f'执行失败: {text}')

        text = f'----停止集群，只启动主节点，以满足前置条件:' \
            f'数据库集群中仅包含一个节点，包含多条连接参数----'
        self.log.info(text)
        stop_res = Pri_U_SH.stop_db_cluster()
        self.assertTrue(stop_res, f'执行失败: {text}')

        start_res = Pri_U_SH.start_db_instance()
        self.assertIn(self.cons.RESTART_SUCCESS_MSG, start_res,
                      f'执行失败: {text}')

        text = '----检查节点状态 expect: 节点状态为Primary----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        start = res.index('instance_role')
        end = res.index('\n', start)
        state = res[start:end].split(':')[-1].strip()
        self.assertEqual(state, 'Primary', f'执行失败: {text}')

    def test_1(self):
        text = '----step1: 删除主节点所有连接参数 expect: 成功----'
        self.log.info(text)
        for i in range(1, Node_Num):
            cmd = f"sed -i '/replconninfo{i}/d' {self.conf_path}"
            self.log.info(cmd)
            res = Pri_U_SH.node.sh(cmd).result()
            self.log.info(res)
            self.assertEqual(len(res), 0, f'执行失败: {text}')

        stop_res = Pri_U_SH.stop_db_cluster()
        self.assertTrue(stop_res, f'执行失败: {text}')

        start_res = Pri_U_SH.start_db_instance()
        self.assertIn(self.cons.RESTART_SUCCESS_MSG, start_res,
                      f'执行失败: {text}')

        text = '----step2: 使用gs_ctl命令查看主节点状态 expect: 主节点状态切换为Normal----'
        self.log.info(text)
        res = Pri_U_SH.get_db_cluster_status('all')
        self.log.info(res)
        start = res.index('instance_role')
        end = res.index('\n', start)
        state = res[start:end].split(':')[-1].strip()
        self.assertEqual(state, 'Normal', f'执行失败: {text}')

    def tearDown(self):
        text = '----run teardown----'
        self.log.info(text)

        text3 = '----step3: 使用备份文件，还原conf文件 expect: 成功----'
        self.log.info(text3)
        cmd = f'\\cp -r {self.conf_path}_bak {self.conf_path} &&' \
            f' rm -rf {self.conf_path}_bak'
        self.log.info(cmd)
        res3 = Pri_U_SH.node.sh(cmd).result()
        self.log.info(res3)

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

        if len(regex_res) != Node_Num:
            restart_res = Pri_U_SH.restart_db_cluster()
            self.assertTrue(restart_res)

        self.assertEqual(len(res3), 0, f'执行失败: {text3}')
        self.assertIn(self.cons.STOP_SUCCESS_MSG, restart_res,
                      f'执行失败: {text3}')
        self.assertEqual(restart_res.count('[SUCCESS]'), Node_Num,
                         f'执行失败: {text3}')
        self.assertEqual(len(regex_res), Node_Num, f'执行失败: {text4}')
        self.assertEqual(state, 'Primary', f'执行失败: {text4}')

        text = f'-----{os.path.basename(__file__)} end-----'
        self.log.info(text)

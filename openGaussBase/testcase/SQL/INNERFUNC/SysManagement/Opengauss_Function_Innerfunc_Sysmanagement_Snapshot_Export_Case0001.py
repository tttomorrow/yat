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
Case Type   : 功能测试
Case Name   : 使用pg_export_snapshot_and_csn()函数保存当前的快照并返回它的标识符
Description :
    1. 调用函数并查看快照是否保存
    2. 函数错误调用
Expect      :
    1. 保存当前的快照并返回它的标识符
    2. 合理报错
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('''---
           Opengauss_Function_Innerfunc_Sysmanagement_Snapshot_Export_Case0001
           开始---''')

    def test_export(self):
        self.log.info('-------------调用函数查看是否保存快照-------------')
        mark = []
        csn = []
        snap_shot = []
        for i in range(4):
            cmd1 = '''select pg_export_snapshot_and_csn();
                select txid_current_snapshot();
                '''
            msg1 = self.commonsh.execut_db_sql(cmd1)
            self.log.info(msg1)
            res1 = msg1.splitlines()[2].split(',')
            res_mark = res1[0][2:-2]
            res_csn = res1[1][:-1]
            snapshot = msg1.splitlines()[-2].strip()
            xmax = snapshot.split(':')[1]
            mark.append(res_mark)
            csn.append(res_csn)
            snap_shot.append(xmax)
        self.log.info(f'标识符：{mark}')
        self.log.info(f'csn: {csn}')
        self.log.info(f'当前快照： {snap_shot}')
        self.log.info('-----调用函数后，快照更新-----')
        for i in range(1, 4):
            incre1 = int(mark[i], base=16) == int(mark[i-1], base=16) + 1
            self.assertTrue(incre1)  # 标识符递增
            incre2 = int(csn[i], base=16) == int(csn[i-1], base=16) + 1
            self.assertTrue(incre2)  # csn递增
            incre3 = int(snap_shot[i]) == int(snap_shot[i-1]) + 1
            self.assertTrue(incre3)  # 快照txid递增

        self.log.info('-------------错误调用-------------')
        cmd2 = '''select pg_export_snapshot_and_csn('current'); 
            select pg_export_snapshot_and_csn;
            '''
        msg3 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg3)
        self.assertTrue(msg3.count('ERROR') == 2)

    def tearDown(self):
        self.log.info('''---
           Opengauss_Function_Innerfunc_Sysmanagement_Snapshot_Export_Case0001
           结束---''')
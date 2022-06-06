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
Case Type   : 系统信息函数-模式可见性查询函数
Case Name   : 使用函数pg_sequence_parameters(sequence_oid)，
              获取指定sequence的参数，包含起始值，最小值和最大值，递增值等
Description :
    1.查看序列的oid
    2.使用函数pg_sequence_parameters(sequence_oid)，
      获取指定sequence的参数，包含起始值，最小值和最大值，递增值等
    3.清理环境
Expect      :
    1.查看序列的oid成功
    2.使用函数pg_sequence_parameters(sequence_oid)，
      获取指定sequence的参数，包含起始值，最小值和最大值，递增值等成功
    3.清理环境成功
History     :
"""
import os
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class Functions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()
        self.squce_name = 'squce_system_info_0027'

    def test_func_sys_info(self):
        text = 'step1:创建序列并查看序列的oid; except:执行成功'
        sql_cmd1 = self.commonsh.execut_db_sql(
            f'create sequence {self.squce_name} start 101 cache 20;'
            f'select relid,relname,schemaname from pg_statio_user_sequences '
            f'where relname = \'{self.squce_name}\';')
        self.log.info(sql_cmd1)
        self.assertIn(self.constant.CREATE_SEQUENCE_SUCCESS_MSG, sql_cmd1,
                      "执行失败" + text)
        self.assertIn('squce_system_info_0027', sql_cmd1, "执行失败" + text)

        oid = int(sql_cmd1.split('\n')[-2].split('|')[0])
        self.log.info(oid)
        if oid >= 0:
            self.log.info('查看排序规则的oid成功')
        else:
            raise Exception('查看异常，请检查')

        text = 'step2:执行函数pg_sequence_parameters()获取指定sequence的参数，' \
               '包含起始值，最小值和最大值，递增值等; except:执行成功'
        sql_cmd2 = self.commonsh.execut_db_sql(
            f'select pg_sequence_parameters({oid});')
        self.log.info(sql_cmd2)
        self.assertIn('1 row', sql_cmd2, "执行失败" + text)
        list1 = sql_cmd2.split('\n')[2]
        self.log.info(list1)
        list2 = list1.split(',')
        self.assertEqual(len(list2), 5)

    def tearDown(self):
        text = 'step3:清理环境; except:清理环境成功'
        sql_cmd3 = self.commonsh.execut_db_sql(
            f'drop sequence {self.squce_name}')
        self.log.info(sql_cmd3)
        self.assertIn(self.constant.DROP_SEQUENCE_SUCCESS_MSG, sql_cmd3,
                      "执行失败" + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

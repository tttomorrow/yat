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
Case Type   : 系统管理函数--其他函数
Case Name   : 函数get_local_active_session() ，提供当前节点保存在内存中的历史活跃session状态的采样记录
Description :
    1.查看参数enable_asp默认值
    2.修改参数enable_asp=on，获取当前节点保存在内存中的历史活跃session状态的采样记录成功
    3.恢复参数默认值
Expect      :
    1.查看参数enable_asp默认值成功
    2.修改参数enable_asp=on，获取当前节点保存在内存中的历史活跃session状态的采样记录成功
    3.恢复参数默认值成功
History     :
"""
import re
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Innerfunc_System_Manage_Case0004 开始-')
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()
        text = '--step1: 查看参数默认值; expect:查看参数默认值成功--'
        self.log.info(text)
        sql_res = self.commonsh.execut_db_sql(f'show enable_asp;')
        self.log.info(sql_res)
        regex_res = re.search('enable_asp.*------------.*(1 row)', sql_res,
                              re.S)
        self.assertIsNotNone(regex_res, '执行失败:' + text)
        self.default_value = sql_res.splitlines()[2].strip()
        self.log.info(self.default_value)

    def test_func_sys_manage(self):
        text = '--step2: 修改参数enable_asp=on，执行函数' \
               'get_local_active_session(),获取当前节点保存在内存中的' \
               '历史活跃session状态的采样记录; expect:执行成功--'
        self.log.info(text)
        sql_res = self.commonsh.execut_db_sql(
            f'alter system set enable_asp to on;'
            f'show enable_asp;'
            f'select get_local_active_session() limit 1;')
        self.log.info(sql_res)
        self.assertIn(self.constant.ALTER_SYSTEM_SUCCESS_MSG, sql_res,
                      '执行失败:' + text)
        self.assertIn('on', sql_res, '执行失败:' + text)
        regex_res = re.search('get_local_active_session.*---------.*(1 row)',
                              sql_res, re.S)
        self.assertIsNotNone(regex_res, '执行失败:' + text)
        str_01 = sql_res.split('\n')[-2]
        self.log.info(str_01)
        list_01 = str_01.split(',')
        self.assertEqual(len(list_01), 27, '执行失败:' + text)

    def tearDown(self):
        text = '--step3:恢复参数默认值; expect:恢复参数默认值成功--'
        self.log.info(text)
        sql_res = self.commonsh.execut_db_sql(
            f'alter system set enable_asp to {self.default_value};')
        self.log.info(sql_res)
        self.assertIn(self.constant.ALTER_SYSTEM_SUCCESS_MSG, sql_res,
                      '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Innerfunc_System_Manage_Case0004 结束-')

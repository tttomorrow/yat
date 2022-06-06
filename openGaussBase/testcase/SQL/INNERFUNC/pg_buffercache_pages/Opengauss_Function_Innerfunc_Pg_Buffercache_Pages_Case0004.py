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
Case Type   : pg_buffercache_pages函数，bufferid字段验证
Case Name   : pg_buffercache_pages 验证pg_buffercache数量
Description :
    1、gsql连接数据库，查询shared_buffers参数值
    2、查询pg_buffercache数量，验证数量是否为shared_buffers/8kb
    3、修改shared_buffers参数
    4、再次查询pg_buffercache数量，验证数量是否为shared_buffers/8kb
Expect      :
    1、gsql连接数据库，查询shared_buffers参数值成功
    2、查询pg_buffercache数量，验证数量为shared_buffers/8kb
    3、修改shared_buffers参数成功
    4、再次查询pg_buffercache数量，验证数量为shared_buffers/8kb
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class PgBuffercachePagesCase0004(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0004:初始化')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.format_result = 0
        self.rest_param = 32768
        self.init_param = ''

    def test_main(self):
        step_txt = '----step1: gsql连接数据库，查询shared_buffers参数值，expect: 查询成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(
            'show shared_buffers;')
        self.log.info(f"show shared_buffers is {result}")
        self.assertNotEqual('', result, '执行失败:' + step_txt)
        self.init_param = result.strip().splitlines()[-2]
        self.para1 = self.init_param.upper()
        if 'GB' in self.para1:
            tmp_para1 = int(self.para1.split('GB')[0])
            self.format_result = tmp_para1 * 1024 * 1024
        if 'MB' in self.para1:
            tmp_para1 = int(self.para1.split('MB')[0])
            self.format_result = tmp_para1 * 1024
        if 'KB' in self.para1:
            tmp_para1 = int(self.para1.split('KB')[0])
            self.format_result = tmp_para1

        step_txt = '----step2: 查询pg_buffercache数量，验证数量是否为shared_buffers/8kb' \
                   'expect: pg_buffercache结果为shared_buffers/8kb----'
        self.log.info(step_txt)
        select_sql = 'select count(*) from pg_buffercache_pages();'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_result = int(select_result.strip().splitlines()[-2])
        self.log.info(tmp_result)
        self.assertEqual(tmp_result, self.format_result / 8,
                         '执行失败:' + step_txt)
        select_sql = 'select max(bufferid) from pg_buffercache_pages();'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_result = int(select_result.strip().splitlines()[-2])
        self.log.info(tmp_result)
        self.assertEqual(tmp_result, self.format_result / 8,
                         '执行失败:' + step_txt)

        step_txt = '----step3: 修改shared_buffers参数，expect: 修改成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"shared_buffers="
                                           f"{self.rest_param}kB")
        self.assertTrue(result, '执行失败:' + step_txt)
        self.log.info('----重启数据库----')
        restart_flag = self.pri_sh.restart_db_cluster()
        self.assertTrue(restart_flag)
        step_txt = '----step4 查询pg_buffercache数量，验证数量是否为shared_buffers/8kb，' \
                   'expect: pg_buffercache结果为shared_buffers/8kb----'
        self.log.info(step_txt)
        select_sql = 'select count(*) from pg_buffercache_pages();'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_result = int(select_result.strip().splitlines()[-2])
        self.log.info(tmp_result)
        self.assertEqual(tmp_result, self.rest_param / 8, '执行失败:' + step_txt)
        select_sql = 'select max(bufferid) from pg_buffercache_pages();'
        select_result = self.pri_sh.execut_db_sql(select_sql)
        self.log.info(select_result)
        tmp_result = int(select_result.strip().splitlines()[-2])
        self.log.info(tmp_result)
        self.assertEqual(tmp_result, self.rest_param / 8, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----step5: 还原参数----'
        self.log.info(step_txt)
        self.pri_sh.execute_gsguc("reload",
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f"shared_buffers = {self.init_param}")
        self.log.info('----重启数据库----')
        restart_flag = self.pri_sh.restart_db_cluster()
        self.assertTrue(restart_flag)

        self.log.info(
            'Opengauss_Function_Innerfunc_Pg_Buffercache_Pages_Case0004:执行完毕')

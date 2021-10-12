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
Case Type   : 系统信息函数-模式可见性查询函数 
Case Name   : 函数pg_ts_dict_is_visible(dict_oid)查看该文本检索词典是否在搜索路径中可见
Description :
    1.创建文本检索词典
    2.查看文本检索词典oid
    3.函数pg_ts_config_is_visible查看该文本检索配置是否在搜索路径中可见
    4.删除文本检索词典
Expect      :
    1.创建文本搜索配置成功
    2.2.查看文本搜索词典oid成功
    3.函数pg_ts_dict_is_visible(dict_oid)，查看该文本检索词典是否在搜索路径中可见成功
    4.删除文本检索词典
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0017开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.创建文本搜索词典')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop text search dictionary if exists pg_dict;'
            f'create text search dictionary pg_dict (template = simple);')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DICTIONARY_SUCCESS_MSG, sql_cmd)

        LOG.info(f'-步骤2.查看文本搜索词典oid')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select oid,dictname from PG_TS_DICT where'
            f' dictname= \'pg_dict\';')
        LOG.info(sql_cmd)
        oid = int(sql_cmd.split('\n')[2].split('|')[0])
        LOG.info(oid)
        if oid >= 0:
            LOG.info('查看临时模式的OID成功')
        else:
            raise Exception('查看异常，请检查')

        LOG.info(f'-步骤3.函数pg_ts_dict_is_visible(dict_oid)查看该文本检索词典是否在搜索路径中可见')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_ts_dict_is_visible({oid});')
        LOG.info(sql_cmd)
        self.assertIn('t', sql_cmd)

        LOG.info(f'-步骤4.删除文本检索词典')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop text search dictionary pg_dict;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.DROP_DICTIONARY_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0017结束-')

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
Case Type   : 功能测试
Case Name   : floor函数入参给正负整数，取不大于参数的最大整数
Description : floor(x) 描述：不大于参数的最大整数。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.执行floor函数取整并断言校验
    步骤 3.清理环境并删除测试表
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：函数返回结果正确
    步骤 3：环境清理成功
History     : 
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()
common = Common()
commonsh = CommonSH('dbuser')
constant = Constant()


class Floor_001(unittest.TestCase):

    def setUp(self):
        logger.info("-------Opengauss_Function_Innerfunc_Function_Floor_Case0001开始执行------------")
        logger.info("-----------查询数据库状态-----------")
        db_status = commonsh.get_db_cluster_status()
        logger.info(db_status)
        if not db_status:
            commonsh.start_db_cluster()
            if not db_status:
                raise Exception("db status is not true, please check!")
        logger.info(db_status)

    def test_floor_001(self):

        SqlMdg = commonsh.execut_db_sql('drop table if exists data_01;')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find(constant.TABLE_DROP_SUCCESS) > -1)
        SqlMdg = commonsh.execut_db_sql('create table data_01 (clo1 int,clo2 int);')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find(constant.TABLE_CREATE_SUCCESS) > -1)
        SqlMdg = commonsh.execut_db_sql('insert into data_01 values (21,-1);')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find('INSERT 0 1') > -1)
        SqlMdg = commonsh.execut_db_sql('select  floor(clo1) , floor(clo2) from data_01;')
        common.equal_sql_mdg(SqlMdg, 'floor | floor', '-------+-------', '21 |    -1', '(1 row)')

    def tearDown(self):
        logger.info("------------------------drop table------------------")
        SqlMdg = commonsh.execut_db_sql('drop table if exists data_01;')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find(constant.TABLE_DROP_SUCCESS) > -1)
        logger.info('------Opengauss_Function_Innerfunc_Function_Floor_Case0001执行结束----------')

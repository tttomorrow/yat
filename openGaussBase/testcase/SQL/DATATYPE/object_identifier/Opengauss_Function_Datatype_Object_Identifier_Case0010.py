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
Case Type   : DataType
Case Name   : 创建内存表，指定大对象数据类型
Description :
    1、查看enable_incremental_checkpoint参数值，并修改为off
    2、创建内存表，指定大对象数据类型(OID)
    3、清理环境，恢复默认值
Expect      :
    1、显示默认值为on，并修改为off
    2、创建内存表失败，不支持OID类型
    3、清理环境、恢复默认值成功
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class DataTypeTestCase(unittest.TestCase):
    def setUp(self):
        LOG.info("Opengauss_Function_Datatype_Object_Identifier_Case0010开始执行")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.show_config = f'''show enable_incremental_checkpoint;'''
        self.table = 'mot_table'

        LOG.info("======步骤1：检查参数，修改配置，并重启数据库======")
        self.config_item = "enable_incremental_checkpoint=off"
        check_res = self.commonsh.execut_db_sql(self.show_config)
        LOG.info(check_res)
        if 'off' not in check_res.splitlines()[-2].strip():
            self.commonsh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        self.config_item)
            result = self.commonsh.restart_db_cluster()
            LOG.info(result)
            result = self.commonsh.get_db_cluster_status()
            LOG.info(result)
            self.assertTrue("Degraded" in result or "Normal" in result)

    def test_datatype(self):
        LOG.info("======步骤2：创建内存表，指定大对象数据类型======")
        sql_cmd = f'''drop foreign table if exists {self.table};
            create foreign table {self.table}(c1 OID);'''
        LOG.info(sql_cmd)
        sql_res = self.commonsh.execut_db_sql(sql_cmd)
        LOG.info(sql_res)
        self.assertIn(self.constant.NOT_SUPPORTED_TYPE, sql_res)

    def tearDown(self):
        LOG.info("======步骤3：清理环境，恢复默认值======")
        self.config_item = "enable_incremental_checkpoint=on"
        check_res = self.commonsh.execut_db_sql(self.show_config)
        LOG.info(check_res)
        if 'on' not in check_res.splitlines()[-2].strip():
            self.commonsh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        self.config_item)
            self.commonsh.restart_db_cluster()
            result = self.commonsh.get_db_cluster_status()
            LOG.info(result)
            self.assertTrue("Degraded" in result or "Normal" in result)
        LOG.info("Opengauss_Function_Datatype_Object_Identifier_Case0010执行结束")

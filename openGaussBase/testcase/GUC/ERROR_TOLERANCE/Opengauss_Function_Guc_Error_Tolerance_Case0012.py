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
Case Type   : GUC
Case Name   : 修改retry_ecode_list为其他数据类型，观察其预期结果；
Description :
            1、查询retry_ecode_list默认值；
            show retry_ecode_list；
            2、修改retry_ecode_list为YY001，观察预期结果；
            gs_guc set -D {cluster/dn1}  -c "retry_ecode_list='YY001'"
            3、恢复默认值
Expect      :
            1、显示默认值YY001 YY002 YY003 YY004 YY005 YY006 YY007 YY008 
            YY009 YY010 YY011 YY012 YY013 YY014 YY015 53200 08006 08000 
            57P01 XX003 XX009 YY016；
            2、修改retry_ecode_list成功，预期结果正常；
            3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOGGER = Logger()
COMMONSH = CommonSH("PrimaryDbUser")


class GucTest(unittest.TestCase):
    def setUp(self):
        LOGGER.info("==Opengauss_Function_Guc_Error_Tolerance_Case0012"
                    "开始执行==")
        self.constant = Constant()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        LOGGER.info("==查询retry_ecode_list 期望：默认值YY001 YY002 "
                    "YY003 YY004 YY005 YY006 YY007 YY008 YY009 YY010 "
                    "YY011 YY012 YY013 YY014 YY015 53200 08006 08000 "
                    "57P01 XX003 XX009 YY016==")
        sql_cmd = COMMONSH.execut_db_sql("show retry_ecode_list;")
        LOGGER.info(sql_cmd)
        self.assertEqual("YY001 YY002 YY003 YY004 YY005 YY006 YY007 "
                         "YY008 YY009 YY010 YY011 YY012 YY013 YY014 "
                         "YY015 53200 08006 08000 57P01 XX003 XX009 "
                         "YY016", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("修改retry_ecode_list为YY001重启生效，期望设置成功")
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "retry_ecode_list='YY001'")
        self.assertTrue(result)

        LOGGER.info("期望：重启后查询结果为YY001")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql("show retry_ecode_list;")
        LOGGER.info(sql_cmd)
        self.assertEqual("YY001", sql_cmd.split("\n")[-2].strip())

        LOGGER.info("做DML")
        sql_cmd = COMMONSH.execut_db_sql('''
            drop table if exists test cascade;
            create table test(c_int int);
            begin
                for i in 0..100 loop
                    insert into test values(i);
                    update test set c_int = 66 where c_int = i;
                end loop;
            end;
            select count(*) from test;
            ''')
        LOGGER.info(sql_cmd)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], sql_cmd)

        LOGGER.info("恢复默认值")
        LOGGER.info("删除表")
        sql_cmd = COMMONSH.execut_db_sql(
            "drop table if exists test cascade;")
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, sql_cmd)
        result = COMMONSH.execute_gsguc("set",
                                        self.constant.GSGUC_SUCCESS_MSG,
                                       "retry_ecode_list='YY001 YY002 "
                                       "YY003 YY004 YY005 YY006 YY007 "
                                       "YY008 YY009 YY010 YY011 YY012 "
                                       "YY013 YY014 YY015 53200 08006 "
                                       "08000 57P01 XX003 XX009 YY016'")
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in result or "Normal" in result)

    def tearDown(self):
        LOGGER.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql("show retry_ecode_list;")
        LOGGER.info(sql_cmd)
        if "YY001 YY002 YY003 YY004 YY005 YY006 YY007 YY008 YY009 " \
           "YY010 YY011 YY012 YY013 YY014 YY015 53200 08006 08000 " \
           "57P01 XX003 XX009 YY016" != sql_cmd.split("\n")[-2].strip():
            COMMONSH.execute_gsguc("set",
                                   self.constant.GSGUC_SUCCESS_MSG,
                                  "retry_ecode_list='YY001 YY002 YY003 "
                                  "YY004 YY005 YY006 YY007 YY008 YY009 "
                                  "YY010 YY011 YY012 YY013 YY014 YY015 "
                                  "53200 08006 08000 57P01 XX003 XX009 "
                                  "YY016'")
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        sql_cmd = COMMONSH.execut_db_sql("show retry_ecode_list;")
        LOGGER.info(sql_cmd)
        self.assertEqual("YY001 YY002 YY003 YY004 YY005 YY006 YY007 "
                         "YY008 YY009 YY010 YY011 YY012 YY013 YY014 "
                         "YY015 53200 08006 08000 57P01 XX003 XX009 "
                         "YY016", sql_cmd.split("\n")[-2].strip())
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOGGER.info("==Opengauss_Function_Guc_Error_Tolerance_Case0012"
                    "执行结束==")

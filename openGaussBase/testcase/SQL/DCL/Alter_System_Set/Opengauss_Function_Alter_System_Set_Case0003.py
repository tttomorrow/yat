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
Case Type   :  DCL-alter-system-set
Case Name   :  有管理员权限：修改postmaster类型
Description :
    1.创建用户并附管理员权限，管理员用户登录，show如下参数 期望：显示成功
    show enable_thread_pool;
    show max_connections;
    2.管理员用户登录，修改如下参数
    alter system set enable_thread_pool  to on;
    alter system set max_connections to 20;
    3.按照2的提示重启数据库后，管理员用户登录，show参数值
    show enable_thread_pool ;
    show max_connections;
    4.恢复环境
Expect      :
    1.显示默认值
    2.修改成功
    3.再次查询显示为修改后的值
    4.恢复成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro


class AlterSystemSet(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info("Opengauss_Function_Alter_System_Set_Case0003开始执行")
        self.constant = Constant()
        self.common = Common()
        self.primary_sh = CommonSH("dbuser")
        self.max_conn = self.common.show_param("max_connections")
        self.u_name = "u_alter_system_set_0003"

    def test_alter_system(self):
        text = "--step1:创建用户并查询默认值;expect:创建成功"
        self.logger.info(text)
        sql = f'''drop schema if exists {self.u_name} cascade;
                drop role if exists {self.u_name};
                create user {self.u_name} 
                password '{macro.COMMON_PASSWD}';
                grant all privileges to {self.u_name};
                '''
        result = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      "执行失败:" + text)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, result,
                      "执行失败:" + text)

        text = "查询默认值"
        self.logger.info(text)
        sql = f'''set session authorization {self.u_name} 
                password '{macro.COMMON_PASSWD}';
                show enable_thread_pool;
                show max_connections;
                '''
        result = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertIn("off", result, "执行失败:" + text)
        self.assertIn(f"{self.max_conn}", result, "执行失败:" + text)

        text = "--step2:修改postmaster类型;expect:修改成功"
        self.logger.info(text)
        sql = f'''set session authorization {self.u_name} 
                password '{macro.COMMON_PASSWD}';
                alter system set enable_thread_pool to on;
                alter system set max_connections to 6666;
                '''
        result = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertIn("ALTER SYSTEM SET", result, "执行失败:" + text)

        status = self.primary_sh.restart_db_cluster()
        self.logger.info(status)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.logger.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

        text = "--step3:重启数据库后，管理员用户登录，show参数值;expect:修改为step2设置值"
        self.logger.info(text)
        sql = f'''set session authorization {self.u_name} 
                password '{macro.COMMON_PASSWD}';
                show enable_thread_pool;
                show max_connections;
                '''
        result = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertIn("on", result, "执行失败:" + text)
        self.assertIn("6666", result, "执行失败:" + text)

    def tearDown(self):
        self.logger.info("this is teardown")
        text = "--step3:恢复查询默认值;expect:成功"
        self.logger.info(text)
        sql = f'''set session authorization {self.u_name} 
                password '{macro.COMMON_PASSWD}';
                alter system set enable_thread_pool to off;
                alter system set max_connections to {self.max_conn};;
                '''
        result_alter = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result_alter)
        sql = f"drop schema if exists {self.u_name} cascade;" \
              f"drop role if exists {self.u_name};"
        result_drop = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result_drop)
        status = self.primary_sh.restart_db_cluster()
        self.logger.info(status)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.logger.info(status)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, result_drop,
                      "执行失败:" + text)
        self.assertIn("ALTER SYSTEM SET", result_alter, "执行失败:" + text)
        self.assertNotIn("ERROR", result_alter, "执行失败:" + text)
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败:" + text)
        self.logger.info("Opengauss_Function_Alter_System_Set_Case0003执行结束")

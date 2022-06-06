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
Case Name   :  有管理员权限：修改sighup类型
Description :
    1.创建用户并附管理员权限，管理员用户登录，show如下参数 期望：显示成功
    show archive_command;show archive_timeout;
    show archive_mode;show wal_level;
    2.管理员用户登录，修改如下参数并查询
    ALTER SYSTEM SET wal_level to 'hot_standby';
    ALTER SYSTEM SET  archive_mode to on;
    ALTER SYSTEM SET archive_command to 'cp %p /%f';
    ALTER SYSTEM SET  archive_timeout to 60;
    select pg_sleep(60);
    show archive_command;show archive_timeout;
    show archive_mode;show wal_level;
    3.恢复环境
Expect      :
    1.显示默认值
    2.修改成功 查询为修改值
    3.恢复成功
History     :
"""

import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class AlterSystemSet(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info("Opengauss_Function_Alter_System_Set_Case0005开始执行")
        self.constant = Constant()
        self.user_node = Node("PrimaryDbUser")
        self.primary_sh = CommonSH("dbuser")
        self.common = Common()

        self.command = self.common.show_param("archive_command")
        self.wal_level = self.common.show_param("wal_level")

        self.u_name = "u_alter_system_set_0005"

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
                show archive_command;
                show archive_timeout;
                show archive_mode;
                show wal_level;
                '''
        result = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertIn("0\n", result, "执行失败:" + text)
        self.assertIn("off\n", result, "执行失败:" + text)
        self.assertIn(f"{self.command}", result, "执行失败:" + text)
        if "hot_standby\n" not in result:
            res = self.primary_sh.execute_gsguc("set",
                                                self.constant.
                                                GSGUC_SUCCESS_MSG,
                                                "wal_level=hot_standby")
            self.logger.info(result)
            status = self.primary_sh.restart_db_cluster()
            self.logger.info(result)

        text = "--step2:修改postmaster类型;expect:修改成功"
        self.logger.info(text)
        sql = f'''set session authorization {self.u_name} 
                password '{macro.COMMON_PASSWD}';
                alter system set archive_command 
                to 'cp %p {macro.DB_INSTANCE_PATH}/%f';
                alter system set archive_timeout to 60;
                alter system set archive_mode to on;
                select pg_sleep(60);
                show archive_command;
                show archive_timeout;
                show archive_mode;
                '''
        result = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result)
        self.assertIn("ALTER SYSTEM SET", result, "执行失败:" + text)
        self.assertIn("1min\n", result, "执行失败:" + text)
        self.assertIn("on\n", result, "执行失败:" + text)
        self.assertIn(macro.DB_INSTANCE_PATH, result, "执行失败:" + text)

    def tearDown(self):
        self.logger.info("this is teardown")
        text = "--step3:恢复查询默认值;expect:成功"
        self.logger.info(text)
        sql = f'''set session authorization {self.u_name} 
                password '{macro.COMMON_PASSWD}';
                alter system set archive_command to '{self.command}';
                alter system set archive_timeout to 0;
                alter system set archive_mode to off;
                alter system set wal_level to {self.wal_level};
                '''
        result_alter = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result_alter)

        sql = f"drop schema if exists {self.u_name} cascade;" \
              f"drop role if exists {self.u_name};"
        result_drop = self.primary_sh.execut_db_sql(sql)
        self.logger.info(result_drop)
        result = self.common.get_sh_result(self.user_node,
                                           f"rm -rf "
                                           f"{macro.DB_INSTANCE_PATH}/0000*")
        self.logger.info(result)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.logger.info(status)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, result_drop,
                         "执行失败:" + text)
        self.assertIn("ALTER SYSTEM SET", result_alter, "执行失败:" + text)
        self.assertNotIn("ERROR", result_alter, "执行失败:" + text)
        self.assertTrue("Normal" in status or "Degraded" in status,
                        "执行失败:" + text)
        self.logger.info("Opengauss_Function_Alter_System_Set_Case0005执行结束")

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
Case Type   : GUC
Case Name   : 使用ALTER SYSTEM SET修改数据库参数listen_addresses为特殊字符
Description :
    1、使用ALTER SYSTEM SET修改数据库参数listen_addresses为+
        gsql -d [数据库名] -p [端口号]
        alter system set listen_addresses to +；
Expect      :
    1、设置失败，有合理报错
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro

logger = Logger()
primary_sh = CommonSH("PrimaryDbUser")


class GucSetListenAddresses(unittest.TestCase):
    def setUp(self):
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0024开始执行"
        )
        # 查看数据库状态是否正常
        db_status = primary_sh.get_db_cluster_status("status")
        if not db_status:
            logger.info("The status of db cluster is abnormal. Please check! \
                                db_status: {}".format(db_status))
            self.assertTrue(db_status)

        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.constant = Constant()

    def test_guc_set_listen_addresses(self):
        # 1、使用ALTER SYSTEM SET修改数据库参数listen_addresses为特殊字符，合理报错
        logger.info("使用ALTER SYSTEM SET修改数据库参数listen_addresses为特殊字符，报语法错误")
        sql1 = "alter system set listen_addresses to +"
        logger.info(sql1)
        body1 = primary_sh.execut_db_sql(sql1)
        logger.info(body1)
        self.assertIn(self.constant.SQL_WRONG_MSG[1], body1)

    def tearDown(self):
        logger.info("---------------------无需清理环境--------------------------")
        # 无需清理环境
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0024执行结束"
        )

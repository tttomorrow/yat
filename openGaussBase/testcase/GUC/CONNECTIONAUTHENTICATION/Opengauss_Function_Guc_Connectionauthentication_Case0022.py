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
Case Name   : listen_addresses参数使用gs_guc set设置为非字符类型值（单节点与多节点）
Description :
    1、使用设置gs_guc set设置listen_addresses，以123456为例
        单机（单节点）：
        gs_guc set -D [数据库实例路径] -c "listen_addresses=123456"
        主备（多节点）：
        gs_guc set -N all -D [数据库实例路径] -c "listen_addresses=123456"
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
            "Opengauss_Function_Guc_Connectionauthentication_Case0022开始执行"
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
        # 1、listen_addresses参数使用gs_guc set设置为非字符类型（单节点与多节点）
        nonchar_value = 123456
        # 1.1 单节点
        logger.info("在单节点使用set设置listen_addresses为非字符类型值")
        parameter1 = f"listen_addresses={nonchar_value}"
        body1 = primary_sh.execute_gsguc(command="set",
                                         assert_flag="",
                                         param=parameter1,
                                         get_detail=True,
                                         single=True)
        logger.info(body1)
        self.assertIn("\"listen_addresses\" is incorrect.", body1)
        logger.info("在单节点使用set设置listen_addresses为非字符类型值失败，合理报错")
        # 1.2 多节点
        logger.info("在多节点使用set设置listen_addresses为非字符类型值")
        parameter1 = f"listen_addresses={nonchar_value}"
        body2 = primary_sh.execute_gsguc(command="set",
                                         assert_flag="",
                                         param=parameter1,
                                         get_detail=True)
        logger.info(body2)
        self.assertIn("\"listen_addresses\" is incorrect.", body2)
        logger.info("在多节点使用set设置listen_addresses为非字符类型值失败，合理报错")

    def tearDown(self):
        logger.info("---------------------无需清理环境--------------------------")
        # 无需清理环境
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0022执行结束"
        )

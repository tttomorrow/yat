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
Case Name   : listen_addresses参数使用gs_guc reload设置为’*‘或
Description :
    1、查看listen_addresses默认值
        source [环境变量路径]
        gs_guc check -D [数据库实例路径] -c listen_addresses
    2、使用gs_guc reload设置listen_addresses为'*'
        单机（单节点）：
        gs_guc reload -D [数据库实例路径] -c "listen_addresses='*'"
        主备（多节点）：
        gs_guc reload -N all -D [数据库实例路径] -c "listen_addresses='*'"
    3、连接数据库，通过show查看是否生效，listen_addresses为默认值，则说明未生效
        gsql -d [数据库名] -p [端口] -c “show listen_addresses”
    4、恢复默认值，在各节点执行以下命令
        gs_guc set -D [数据库实例路径] -c "listen_addresses=[各节点默认值]"
    5、使用gs_guc reload设置listen_addresses为'0.0.0.0'
        单机（单节点）：
        gs_guc reload -D [数据库实例路径] -c "listen_addresses='0.0.0.0'"
        主备（多节点）：
        gs_guc reload -N all -D [数据库实例路径] -c "listen_addresses='0.0.0.0'"
    6、重复步骤3-4
Expect      :
    1、查看listen_addresses默认值成功；
    2、gs_guc reload设置listen_addresses成功；
    3、show listen_addresses的值和第2步设置的值不一样，说明reload设置不生效；
    4、恢复默认值成功；
    5、gs_guc reload设置listen_addresses成功；
    6、重复步骤3-4正常无报错
History     : 2021/8/18 为适配listen_addresses默认值变更，修改正则写法
"""
import re
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

logger = Logger()
db_user_list = ['PrimaryDbUser', 'Standby1DbUser', 'Standby2DbUser']
primary_sh = CommonSH(db_user_list[0])


@unittest.skipIf(1 == primary_sh.get_node_num(),
                 "当前门禁不支持一主多备用例")
class GucReloadListenAddresses(unittest.TestCase):
    def setUp(self):
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0020开始执行")

        # 查看数据库状态是否正常
        db_status = primary_sh.get_db_cluster_status("status")
        if not db_status:
            logger.info("The status of db cluster is abnormal. Please check! \
                        db_status: {}".format(db_status))
            self.assertTrue(db_status)

        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.constant = Constant()
        self.node_list = [Node(x) for x in db_user_list]
        self.commonsh_list = [CommonSH(x) for x in db_user_list]

        # 1、查看listen_addresses默认值，获取默认值
        logger.info("在各节点查看listen_addresses默认值")
        parameter = "listen_addresses"
        strs = self.commonsh_list[0].execute_gsguc(command="check",
                                                   assert_flag="",
                                                   param=parameter,
                                                   get_detail=True)
        str_list = strs.split("\n")
        logger.info(str_list)
        self.default_ips_list = []
        # 举个例子listen_addresses='localhost,192.168.0.100'
        reg1 = re.compile(r"(?<=listen_addresses=')\w{9},\d+\.\d+\.\d+\.\d+|$")
        for string in str_list:
            default_ip_list = reg1.findall(string)
            if default_ip_list and default_ip_list[0]:
                default_ip = "\'{}\'".format(default_ip_list[0])
                self.default_ips_list.append(default_ip)
        if not self.default_ips_list:
            raise Exception("listen_addresses默认值获取为空，请检查")
        logger.info("各节点查看listen_addresses默认值列表:"
                    "{}".format(self.default_ips_list))

    def test_guc_reload_listen_addresses(self):
        # 2、使用设置gs_guc reload设置listen_addresses，指定other_ip为修改值
        other_ips = ["\'*\'", "\'0.0.0.0\'"]
        index = 1
        for other_ip in other_ips:
            logger.info(f"指定ip {other_ip} 为修改值")
            # 2.1 单节点
            logger.info("在单节点使用reload设置listen_addresses")
            parameter1 = f"listen_addresses={other_ip}"
            body1 = self.commonsh_list[0].execute_gsguc(command="reload",
                                                        assert_flag="",
                                                        param=parameter1,
                                                        get_detail=True,
                                                        single=True)
            logger.info(body1)
            self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body1)
            logger.info("连接数据库，通过show命令查看listen_addresses的值，"
                        "确认是否生效")
            reg2 = re.compile(r"\'[\d+\.|\*]+\'")
            body2 = self.commonsh_list[0].execut_db_sql(
                sql="show listen_addresses")
            logger.info(body2)
            gsql_show_listen_addersses = reg2.findall(body2)
            if gsql_show_listen_addersses:
                if gsql_show_listen_addersses[0] == other_ip:
                    raise Exception(f"通过reload方式修改listen_addresses生效，"
                                    f"不符合预期，请检查！"
                                    f"gsql_show_listen_addersses: "
                                    f"{gsql_show_listen_addersses[0]}; "
                                    f"other_ip: {other_ip}")
                else:
                    logger.info("通过show命令查看的listen_addresses值，"
                                "和修改值不一致，说明未生效，符合预期")
            logger.info("将listen_addresses还原为为默认ip")
            parameter2 = f"listen_addresses={self.default_ips_list[0]}"
            body3 = self.commonsh_list[0].execute_gsguc(command="set",
                                                        assert_flag="",
                                                        param=parameter2,
                                                        get_detail=True,
                                                        single=True)
            logger.info(body3)
            self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body3)
            logger.info("在单节点使用reload设置listen_addresses完成")
            # 2.2 多节点
            logger.info("在多节点使用reload设置listen_addresses")
            body4 = self.commonsh_list[0].execute_gsguc(command="reload",
                                                        assert_flag="",
                                                        param=parameter1,
                                                        get_detail=True)
            logger.info(body4)
            self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body4)
            logger.info("在各节点连接数据库，通过show命令查看listen_addresses的值，"
                        "确认是否生效")
            for i in range(len(self.commonsh_list)):
                body5 = self.commonsh_list[i].execut_db_sql(
                    sql="show listen_addresses")
                logger.info(body5)
                gsql_show_listen_addersses = reg2.findall(body5)
                if gsql_show_listen_addersses:
                    if gsql_show_listen_addersses[0] == other_ip:
                        raise Exception(f"通过reload方式修改listen_addresses生效，"
                                        f"不符合预期，请检查！"
                                        f"gsql_show_listen_addersses: "
                                        f"{gsql_show_listen_addersses[0]}; "
                                        f"other_ip: {other_ip}")
                    else:
                        logger.info("通过show命令查看的listen_addresses值，"
                                    "和修改值不一致，说明未生效，符合预期")
            logger.info("在多节点使用reload设置listen_addresses完成")
            # <len(other_ips)的多节点listen_addresses默认值在此还原
            # 否则，放在teardown()中还原
            if index < 2:
                if self.default_ips_list:
                    logger.info("将listen_addresses还原为为默认ip")
                    for j in range(len(self.commonsh_list)):
                        parameter3 = f"listen_addresses=" \
                                     f"{self.default_ips_list[j]}"
                        body6 = self.commonsh_list[j].execute_gsguc(
                            command="set",
                            assert_flag="",
                            param=parameter3,
                            get_detail=True,
                            single=True)
                        logger.info(body6)
                        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body6)
            index += 1

    def tearDown(self):
        logger.info("---------------------清理环境--------------------------")
        if self.default_ips_list:
            logger.info("将listen_addresses还原为为默认ip")
            for k in range(len(self.commonsh_list)):
                parameter3 = f"listen_addresses={self.default_ips_list[k]}"
                body7 = self.commonsh_list[k].execute_gsguc(command="set",
                                                            assert_flag="",
                                                            param=parameter3,
                                                            get_detail=True,
                                                            single=True)
                logger.info(body7)
                self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body7)
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0020执行结束")

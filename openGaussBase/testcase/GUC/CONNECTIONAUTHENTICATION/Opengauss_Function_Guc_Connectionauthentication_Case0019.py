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
Case Name   : listen_addresses参数使用gs_guc set设置为'*'或'0.0.0.0'
              （单节点与多节点）
Description :
    1、查看listen_addresses默认值
        source [环境变量路径]
        gs_guc check -D [数据库实例路径] -c listen_addresses
    2、使用设置gs_guc set设置listen_addresses为'*'
        单机（单节点）：
        gs_guc set -D [数据库实例路径] -c "listen_addresses='*'"
        主备（多节点）：
        gs_guc set -N all -D [数据库实例路径] -c "listen_addresses='*'"
    3、在配置文件中查看listen_addresses是否为'*'
        cat [数据库实例路径]/postgresql.conf | grep listen_addresses
    4、重启数据库使其生效
        gs_om -t stop && gs_om -t start
    5、恢复默认值，在各节点执行以下命令
        gs_guc set -D [数据库实例路径] -c "listen_addresses=[各节点默认值]"
    6、重启数据库使其生效
        gs_om -t stop && gs_om -t start
    7、使用设置gs_guc set设置listen_addresses为'0.0.0.0'
        单机（单节点）：
        gs_guc set -D [数据库实例路径] -c "listen_addresses='0.0.0.0'"
        主备（多节点）：
        gs_guc set -N all -D [数据库实例路径] -c "listen_addresses='0.0.0.0'"
    8、重复步骤2~6
Expect      :
    1、查看listen_addresses默认值成功；
    2、gs_guc set设置listen_addresses成功；
    3、postgresql.conf中listen_addresses的值和第2步设置的值一样；
    4、重启数据库成功；
    5、恢复默认值成功；
    6、重启数据库成功；
    7、gs_guc set设置listen_addresses成功；
    8、重复步骤2~6无报错
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
class GucSetListenAddresses(unittest.TestCase):
    def setUp(self):
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0019开始执行"
        )

        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.constant = Constant()
        self.node_list = [Node(x) for x in db_user_list]
        self.commonsh_list = [CommonSH(x) for x in db_user_list]

        # 查看数据库状态是否正常
        db_status = self.commonsh_list[0].get_db_cluster_status("status")
        if not db_status:
            logger.info("The status of db cluster is abnormal. Please check! \
                        db_status: {}".format(db_status))
            self.assertTrue(db_status)

        # 1、查看listen_addresses默认值，获取默认值
        logger.info("在各节点查看listen_addresses默认值")
        parameter = "listen_addresses"
        strs = self.commonsh_list[0].execute_gsguc(command="check",
                                                   assert_flag="",
                                                   param=parameter,
                                                   get_detail=True,
                                                   single=False)
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

    def test_guc_set_listen_addresses(self):
        # 2、使用设置gs_guc set设置listen_addresses，指定other_ip为修改值
        other_ips = ["\'*\'", "\'0.0.0.0\'"]
        index = 1
        for other_ip in other_ips:
            logger.info(f"指定ip {other_ip} 为修改值")
            # 2.1 单节点
            logger.info("在单节点使用set设置listen_addresses")
            parameter1 = f"listen_addresses={other_ip}"
            body1 = self.commonsh_list[0].execute_gsguc(command="set",
                                                        assert_flag="",
                                                        param=parameter1,
                                                        get_detail=True,
                                                        single=True)
            logger.info(body1)
            self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body1)
            logger.info("查看postgresql.conf的值是否和修改值一致")
            command1 = f"cat {self.DB_INSTANCE_PATH}/postgresql.conf " \
                       f"| grep listen_addresses"
            body2 = self.node_list[0].sh(command1).result()
            logger.info(body2)
            reg2 = re.compile(r"\'[\d+\.|\*]+\'")
            postgresql_listen_addersses = reg2.findall(body2)
            if postgresql_listen_addersses:
                self.assertEqual(postgresql_listen_addersses[0], other_ip,
                                 msg=f"gs_guc set失败，两个ip不一样" \
                                     f"{postgresql_listen_addersses[0]}," \
                                     f"{other_ip}")
            else:
                raise Exception("postgressql.conf中listen_addresses为空")
            logger.info("postgressql.conf中listen_addresses和修改值一致")
            logger.info("重启数据库使之生效")
            if not self.commonsh_list[0].restart_db_cluster():
                logger.info(f"修改默认值为{other_ip}，数据库重启成功")
            logger.info("将listen_addresses还原为为默认ip，并重启数据库")
            parameter2 = f"listen_addresses={self.default_ips_list[0]}"
            body3 = self.commonsh_list[0].execute_gsguc(command="set",
                                                        assert_flag="",
                                                        param=parameter2,
                                                        get_detail=True,
                                                        single=True)
            logger.info(body3)
            self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body3)
            if not self.commonsh_list[0].restart_db_cluster():
                raise Exception("还原默认值后，重启数据库失败！请检查！")
            else:
                logger.info("数据库重启成功")
            logger.info("在单节点使用set设置listen_addresses成功")
            # 2.2 多节点
            logger.info("在多节点使用set设置listen_addresses")
            body4 = self.commonsh_list[0].execute_gsguc(command="set",
                                                        assert_flag="",
                                                        param=parameter1,
                                                        get_detail=True)
            logger.info(body4)
            self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body4)
            logger.info("在各节点查看postgresql.conf的值是否和修改值一致")
            for i in range(len(self.node_list)):
                body5 = self.node_list[i].sh(command1).result()
                logger.info(body5)
                postgresql_listen_addersses = reg2.findall(body5)
                if postgresql_listen_addersses:
                    self.assertEqual(postgresql_listen_addersses[0], other_ip,
                                     msg=f"gs_guc set失败，两个ip不一样" \
                                         f"{postgresql_listen_addersses[0]}," \
                                         f"{other_ip}")
                else:
                    raise Exception("postgressql.conf中listen_addresses为空")
            logger.info("postgressql.conf中listen_addresses和修改值一致")
            logger.info("重启数据库使之生效")
            if not self.commonsh_list[0].restart_db_cluster():
                logger.info("修改默认值为其他ip后，重启数据库失败")
            # <len(other_ips)的多节点listen_addresses默认值在此还原
            # 否则，放在teardown()中还原
            if index < len(other_ips):
                logger.info("将listen_addresses还原为为默认ip，并重启数据库")
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
                if not self.commonsh_list[0].restart_db_cluster():
                    raise Exception("还原默认值后，重启数据库失败！请检查！")
                else:
                    logger.info("数据库重启成功")
                logger.info("在多节点使用set设置listen_addresses成功")
            index += 1

    def tearDown(self):
        logger.info("---------------------清理环境--------------------------")
        if self.default_ips_list:
            logger.info("将listen_addresses还原为为默认ip，并重启数据库")
            for k in range(len(self.commonsh_list)):
                parameter4 = f"listen_addresses={self.default_ips_list[k]}"
                body7 = self.commonsh_list[k].execute_gsguc(command="set",
                                                            assert_flag="",
                                                            param=parameter4,
                                                            get_detail=True,
                                                            single=True)
                logger.info(body7)
                self.assertIn(self.constant.GSGUC_SUCCESS_MSG, body7)
            if not self.commonsh_list[0].restart_db_cluster():
                raise Exception("还原默认值后，重启数据库失败！请检查！")
            else:
                logger.info("数据库重启成功")
        logger.info(
            "Opengauss_Function_Guc_Connectionauthentication_Case0019执行结束"
        )

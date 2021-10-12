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
Case Name   : 创建用户组，设置角色生效的时间戳和失效时间戳
Description :
    1.创建用户，指定用户的生效时间戳
    2.未到开始生效时间，连接用户
    3.生效时间开始，连接用户
    4.生效时间过后，连接用户
Expect      :
    1.创建设置正确
    2.失败
    3.成功
    4.失败
History     :
"""

import unittest
import sys
import time
import datetime
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        logger.info("--------Opengauss_Function_DDL_Create_Group_Case0009开始执行--------")
        self.commonsh = CommonSH('dbuser')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_group(self):
        def func_login():  # 登陆
            cmd = f'''source {self.DB_ENV_PATH}
            gsql {self.userNode.db_name} my_group -W '{macro.COMMON_PASSWD}' -p {self.userNode.db_port} -c "select 'yes ok';"'''
            logger.info(cmd)
            msg = self.userNode.sh(cmd).result()
            logger.info(msg)
            return msg

        error_msg = "FATAL:  The account is not within the period of validity."

        logger.info('----------设置生效的时间是当前时间后的5-10秒内--------')
        cmd0 = f''' source {self.DB_ENV_PATH}
                    date +"%Y-%m-%d %H:%M:%S" --date="+5 second";
                    date +"%Y-%m-%d %H:%M:%S" --date="+8 second"'''
        msg0 = self.userNode.sh(cmd0).result()
        logger.info(msg0)
        begin, end = msg0.splitlines()[0].strip(), msg0.splitlines()[1].strip()
        logger.info('----------------创建用户，指定用户的生效时间戳--------')
        create_cmd = f"""drop group if exists my_group;
        create group my_group with login password '{macro.COMMON_PASSWD}' valid begin '{begin}' valid until '{end}';"""
        msg1 = self.commonsh.execut_db_sql(create_cmd)
        logger.info(msg1)
        self.assertTrue('DROP ROLE' in msg1 and 'CREATE ROLE' in msg1)
        logger.info('----------------提前登陆----------------------------')
        msg2 = func_login()
        self.assertTrue(error_msg in msg2)
        time.sleep(6)
        logger.info('----------------生效时间内登陆--------------- -------')
        msg3 = func_login()
        self.assertTrue('yes ok' in msg3)
        logger.info('----------------时间失效后登陆-----------------------')
        time.sleep(3)
        msg4 = func_login()
        self.assertTrue(error_msg in msg4)
        logger.info('----------------删除group---------------------------')
        del_cmd = """drop group my_group;"""
        msg = self.commonsh.execut_db_sql(del_cmd)
        logger.info(msg)

    def tearDown(self):
        logger.info('--------Opengauss_Function_DDL_Create_Group_Case0009执行结束--------')

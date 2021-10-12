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
Case Name   : pg_postmaster_start_time函数返回服务器启动时间
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.对数据库进行重启
    步骤 3.执行SELECT pg_postmaster_start_time;返回返回服务器启动时间
Expect      :
    步骤 1.数据库状态正常
    步骤 2.重启成功
    步骤 3.函数返回服务器启动时间timestamp with time zone
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')


class Pg_postmaster_start_time(unittest.TestCase):

    def setUp(self):
        logger.info("------------Opengauss_BaseFunc_pg_postmaster_start_time_001开始执行--------------")

    def test_pg_postmaster_start_time(self):
        data = commonsh.node.sh('date "+%Y-%m-%d %H:%M:%S"').result()
        logger.info(data)
        stop_mag = commonsh.stop_db_cluster()
        try:
            logger.info(stop_mag)
            self.assertTrue(stop_mag)
            logger.info('stop db success')
        except Exception as e:
            logger.error('db stop fail, please check!')
            raise e
        start_mag = commonsh.start_db_cluster()
        try:
            self.assertTrue(start_mag)
            logger.info('start db success')
        except Exception as e:
            logger.error('db start fail, please check!')
            raise e
        logger.info(type(data))
        SqlMdg = commonsh.execut_db_sql('SELECT pg_postmaster_start_time();').splitlines()[-2].strip()
        logger.info(SqlMdg)
        try:
            self.assertEqual(SqlMdg[0:14], data[0:14])
            logger.info(f'{SqlMdg[0:14]} == {data[0:14]}')
        except Exception as e:
            logger.info(f'{SqlMdg[0:14]} != {data[0:14]}')
            raise e
        else:
            try:
                self.assertTrue(len(SqlMdg) >= 23)
                logger.info('返回正确，带时区')
            except Exception as e:
                logger.info('返回长度不够，请检查')
                raise e

    def tearDown(self):
        logger.info('--------------Opengauss_BaseFunc_pg_postmaster_start_time_001执行结束--------------')

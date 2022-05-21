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
Case Type   : Trigger+COPY
Case Name   : 目标表中存在Trigger，COPY成功
Description :
    1、创建源表及触发表
    2、创建触发器函数
    3、创建INSERT触发器
    4、执行INSERT触发事件并检查触发结果
    5、拷贝表的数据到dat文件
    6、删除源表数据
    7、从dat文件中拷贝数据到源表中
    8、清理环境
Expect      :
    1、创建源表及触发表成功；
    2、创建触发器函数成功；
    3、创建INSERT触发器成功；
    4、执行INSERT触发事件成功，检查触发结果正常；
    5、COPY TO成功；
    6、删除源表数据成功；
    7、COPY FROM成功；
    8、清理环境成功
History     : 2021/2/24 修改单词拼写错误，纠正期望结果
"""

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
import os
import sys
import time
import unittest
from yat.test import macro
from yat.test import Node

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')


class TriggerCopyTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("-----Opengauss_Function_Trigger_Copy_Case001开始执行-----")
        # 查看数据库状态是否正常
        db_status = commonsh.get_db_cluster_status("status")
        if not db_status:
            logger.info("The status of db cluster is abnormal. Please check! \
                        db_status: {}".format(db_status))
            self.assertTrue(db_status)

        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.constant = Constant()

    def test_trigger_copy(self):
        sql1 = f'''CREATE TABLE IF NOT EXISTS test_trigger_src_tbl(id1 INT, \
                   id2 INT, id3 INT);
                   CREATE TABLE IF NOT EXISTS test_trigger_des_tbl(id1 INT, \
                   id2 INT, id3 INT);

                   CREATE OR REPLACE FUNCTION tri_insert_func() RETURNS \
                   TRIGGER AS
                   \$\$
                   DECLARE
                   BEGIN
                        INSERT INTO test_trigger_des_tbl VALUES(NEW.id1, \
                        NEW.id2, NEW.id3);
                        RETURN NEW;
                   END
                   \$\$ LANGUAGE PLPGSQL;'''
        msg = commonsh.execut_db_sql(sql1)
        logger.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)

        sql1 = f'''CREATE TRIGGER insert_trigger
                   BEFORE INSERT ON test_trigger_src_tbl
                   FOR EACH ROW
                   EXECUTE PROCEDURE tri_insert_func();

                   INSERT INTO test_trigger_src_tbl VALUES(100,200,300);
                   SELECT * FROM test_trigger_src_tbl;
                   SELECT * FROM test_trigger_des_tbl;'''
        msg = commonsh.execut_db_sql(sql1)
        logger.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)

        target_dir = os.path.join(self.DB_INSTANCE_PATH, "trigger.dat")
        sql2 = f'''COPY test_trigger_src_tbl TO '{target_dir}';'''
        msg = commonsh.execut_db_sql(sql2)
        logger.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)

        sql3 = f'''DELETE FROM test_trigger_src_tbl;
                   SELECT * FROM test_trigger_src_tbl;'''
        msg = commonsh.execut_db_sql(sql3)
        logger.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)
        self.assertIn("0 rows", msg)

        # 测试点1：从dat文件中拷贝数据到带trigger原表中，不报错
        # 测试点2：查看原表数据，是否恢复成功
        sql4 = f'''COPY test_trigger_src_tbl FROM '{target_dir}';
                   SELECT * FROM test_trigger_src_tbl;'''
        msg = commonsh.execut_db_sql(sql4)
        logger.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)
        self.assertIn("1 row", msg)

    def tearDown(self):
        logger.info("---------------------清理环境--------------------------")
        sql5 = f'''DROP TRIGGER IF EXISTS insert_trigger ON \
                   test_trigger_src_tbl;
                   DROP FUNCTION IF EXISTS tri_insert_func;
                   DROP TABLE IF EXISTS test_trigger_src_tbl;
                   DROP TABLE IF EXISTS test_trigger_des_tbl;'''
        msg = commonsh.execut_db_sql(sql5)
        logger.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)
        logger.info("-----Opengauss_Function_Trigger_Copy_Case001执行结束-----")

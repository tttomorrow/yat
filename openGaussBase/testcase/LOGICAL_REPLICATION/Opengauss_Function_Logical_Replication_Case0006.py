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
Case Type   : 逻辑复制
Case Name   : 对压缩表的COPY语句进行逻辑解码
Description :
    1.创建测试表并插入数据
    2.构造数据文件
    3.执行copy to导出数据
    4.创建逻辑复制槽
    5.执行copy命令
    6.进行逻辑解码
    7.删除新建逻辑复制槽，删除测试表
Expect      :
    1.创建测试表并插入数据成功
    2.构造数据文件成功
    3.执行copy to导出数据成功
    4.创建逻辑复制槽成功
    5.执行copy命令成功
    6.进行逻辑解码失败
    7.删除新建逻辑复制槽成功,删除测试表成功；
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant

LOG = Logger()


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        LOG.info('----------------this is setup-----------------------')
        LOG.info(
            '---Opengauss_Function_Logical_Replication_Case0006开始执行-----')
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.constant = Constant()
        self.instance_path = macro.DB_INSTANCE_PATH
        self.user_node = Node('PrimaryDbUser')
        self.parameter_values = ''

    def test_logical_replication(self):
        LOG.info(
            '----------------设置wal_level = logical----------------------')
        msg = self.comsh.execut_db_sql('show wal_level;')
        LOG.info(msg)
        self.parameter_values = msg.splitlines()[-2].strip()
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                      'wal_level=logical')
        LOG.info(msg)
        LOG.info('---------------------重启数据库--------------------')
        self.comsh.restart_db_cluster()
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        msg1 = self.comsh.execut_db_sql('show wal_level;')
        LOG.info(msg1)
        self.new_value = msg1.splitlines()[-2].strip()
        self.assertIn('logical', self.new_value)

        LOG.info(
            '-------------------创建测试表并插入数据------------------------')
        msg = self.comsh.execut_db_sql('''
                CREATE TABLE warehouse_t
                (
                    W_WAREHOUSE_SK            INTEGER               NOT NULL,
                    W_WAREHOUSE_ID            CHAR(16)              NOT NULL,
                    W_WAREHOUSE_NAME          VARCHAR(20)            
                ) WITH (ORIENTATION = COLUMN, COMPRESSION=HIGH);
                insert into warehouse_t values (2,'aa','bb');
                ''')
        LOG.info(msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, msg)

        LOG.info(
            '-------------------构造数据文件------------------------')
        excute_cmd = f'''mkdir {self.instance_path}/pg_copydir;
                        touch {self.instance_path}/pg_copydir/testzl.dat;'''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)

        LOG.info(
            '---------------------导出数据-------------------------')
        msg = self.comsh.execut_db_sql(f'''
            copy warehouse_t to '{self.instance_path}/pg_copydir/testzl.dat';
                                ''')
        LOG.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)


        LOG.info(
            '---------------------创建逻辑复制槽-------------------------')
        msg = self.comsh.execut_db_sql(
            "SELECT * FROM pg_create_logical_replication_slot"
            "('slot1', 'mppdb_decoding');")
        LOG.info(msg)
        self.res = msg.splitlines()[-1].strip()
        self.assertIn('1 row', self.res)

        LOG.info(
            '---------------------执行copy命令-------------------')
        msg = self.comsh.execut_db_sql(f'''
            copy warehouse_t from '{self.instance_path}/pg_copydir/testzl.dat'
                                        ''')
        LOG.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)

        LOG.info(
            '-----------------------进行逻辑解码-------------------')
        msg = self.comsh.execut_db_sql(
            "SELECT * FROM pg_logical_slot_peek_changes('slot1', NULL, 4096);")
        LOG.info(msg)
        self.assertNotIn(''''"'2'","'aa'","'bb'"''', msg)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        msg = self.comsh.execut_db_sql('''
                    SELECT * FROM pg_drop_replication_slot('slot1');
                    drop table warehouse_t;
                    ''')
        LOG.info(msg)
        excute_cmd = f'''rm -rf {self.instance_path}/pg_copydir'''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        msg = self.comsh.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                       f"wal_level={self.parameter_values}")
        LOG.info(msg)
        stopmsg = self.comsh.stop_db_cluster()
        LOG.info(stopmsg)
        startmsg = self.comsh.start_db_cluster()
        LOG.info(startmsg)
        LOG.info(
            '-----Opengauss_Function_Logical_Replication_Case0006执行完成---')

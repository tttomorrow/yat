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
Case Name   : pg_partition_filepath函数获取分区路径
Description : 验证函数对事务内分区表增路径获取的正确性验证
Expect      : 分区路径获取正确
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Function(unittest.TestCase):
    def setUp(self):
        LOG.info('--Opengauss_Function_Sysmanagement_Dbobject_Pfpath_Case0001'
            '开始--')
        self.sh_primy = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_getPath(self):
        sql_cmd = '''drop table if exists sales;
            create table sales
            (prod_id numeric(6),
            cust_id numeric,
            time_id date,
            channel_id char(1),
            promo_id numeric(6),
            quantity_sold numeric(3),
            amount_sold numeric(10,2)
            )
            partition by range (time_id)
            interval('1 day')
            ( partition pname1 values less than ('2018-01-01 00:00:00'),
            partition pname2 values less than ('2019-12-31 00:00:00')
            );'''
        msg = self.sh_primy.execut_db_sql(sql_cmd)
        LOG.info(msg)
        LOG.info('---------------testpoint:分区路径可以用此函数查到-------------')
        # 随表创建的分区路径存在
        sql_cmd1 = '''select pg_partition_filepath(a.oid) 
            from pg_partition a where a.relname = 'pname1';'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        LOG.info(msg1)
        self.assertIn('base', msg1)
        path1 = msg1.splitlines()[2].strip()
        sql_cmd2 = ''' select pg_partition_filepath(a.oid)
            from pg_partition a where a.relname = 'pname2';'''
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        LOG.info(msg2)
        self.assertIn('base', msg2)
        path2 = msg2.splitlines()[2].strip()
        # 新插入数据成立新分区的路径也能查到
        sql_cmd3 = '''insert into sales values(1, 12, 
            '2020-02-05 10:00:00', 'a', 1, 1, 1);
            select pg_partition_filepath(a.oid) 
            from pg_partition a where a.relname = 'sys_p1';'''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        LOG.info(msg3)
        self.assertIn('base', msg3)
        path3 = msg3.splitlines()[3].strip()
        LOG.info('---------------testpoint:验证路径存在-------------')
        cmd_1 = f'''ls -al {macro.DB_INSTANCE_PATH}/{path1}'''
        LOG.info(cmd_1)
        msg11 = self.user.sh(cmd_1).result()
        LOG.info(msg11)
        self.assertIn(path1, msg11)
        cmd_2 = f'''ls -al {macro.DB_INSTANCE_PATH}/{path2}'''
        LOG.info(cmd_2)
        msg2 = self.user.sh(cmd_2).result()
        LOG.info(msg2)
        self.assertIn(path2, msg2)
        cmd_3 = f'''ls -al {macro.DB_INSTANCE_PATH}/{path3}'''
        LOG.info(cmd_3)
        msg3 = self.user.sh(cmd_3).result()
        LOG.info(msg3)
        self.assertIn(path3, msg3)
        LOG.info('---------------testpoint:验证路径正确性-------------')
        # 修改权限000后不能插入数据
        cmd_4 = f'''chmod 000 {macro.DB_INSTANCE_PATH}/{path2}'''
        chmod_msg1 = self.user.sh(cmd_4).result()
        LOG.info(chmod_msg1)
        sql_cmd4 = '''insert into sales values(1, 12, 
            '2019-11-05 11:00:00', 'a', 1, 1, 1);'''
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        LOG.info(msg4)
        self.assertIn(' Permission denied', msg4)
        # 恢复权限后可以插入
        cmd_5 = f'''chmod 600 {macro.DB_INSTANCE_PATH}/{path2}'''
        chmod_msg2 = self.user.sh(cmd_5).result()
        LOG.info(chmod_msg2)
        sql_cmd5 = '''insert into sales values(1, 12, 
            '2019-11-05 11:00:00', 'a', 1, 1, 1);'''
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        LOG.info(msg5)
        self.assertIn('INSERT', msg5)

    def tearDown(self):
        sql_cmd9 = 'drop table sales cascade;'
        msg9 = self.sh_primy.execut_db_sql(sql_cmd9)
        LOG.info(msg9)
        self.assertTrue(msg9.find('DROP TABLE') > -1)
        LOG.info('--Opengauss_Function_Sysmanagement_Dbobject_Pfpath_Case0001'
            '结束--')
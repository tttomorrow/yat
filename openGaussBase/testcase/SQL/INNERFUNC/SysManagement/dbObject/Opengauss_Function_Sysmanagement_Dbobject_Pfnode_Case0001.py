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
Case Type   : 功能测试
Case Name   : pg_partition_filenode(partition_oid)获取分区节点名称
Description : 验验证函数对分区节点获取的准确性
Expect      : 分区路径获取正确
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Function(unittest.TestCase):
    def setUp(self):
        LOG.info('--Opengauss_Function_Sysmanagement_Dbobject_Pfnode_Case0001'
            '开始--')
        self.sh_primy = CommonSH('dbuser')
        self.user = Node('dbuser')

    def test_getNode(self):
        sql_cmd0 = '''drop table if exists sales;
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
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        LOG.info(msg0)
        LOG.info('---------------testpoint:分区路径可以用此函数查到-------------')
        # 随表创建的分区路径存在
        sql_cmd1 = '''select pg_partition_filenode(a.oid) 
            from pg_partition a where a.relname = 'pname1';'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        LOG.info(msg1)
        path1 = msg1.splitlines()[2].strip()
        self.assertTrue(int(path1) > 0)
        sql_cmd2 = ''' select pg_partition_filenode(a.oid) 
            from pg_partition a where a.relname = 'pname2';
            '''
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        LOG.info(msg2)
        path2 = msg2.splitlines()[2].strip()
        self.assertTrue(int(path2) > 0)
        # 新插入数据成立新分区的路径也能查到
        sql_cmd3 = '''insert into sales values(1, 12, 
            '2020-02-05 10:00:00', 'a', 1, 1, 1);
            select pg_partition_filenode(a.oid) 
            from pg_partition a where a.relname = 'sys_p1';
            '''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        LOG.info(msg3)
        path3 = msg3.splitlines()[3].strip()
        self.assertTrue(int(path3) > 0)
        LOG.info('---------------testpoint:验证路径存在-------------')
        sql_cmd4 = ''' select pg_partition_filepath(a.oid) 
            from pg_partition a where a.relname = 'sys_p1';
            '''
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        LOG.info(msg4)
        self.assertIn(path3, msg4)
        par_path_total = msg4.splitlines()[2].strip().split("/")[:-1]
        par_path = "/".join(par_path_total)
        cmd_5 = f'''ls -al {macro.DB_INSTANCE_PATH}/{par_path}/{path1}'''
        LOG.info(cmd_5)
        msg5 = self.user.sh(cmd_5).result()
        LOG.info(msg5)
        self.assertIn(path1, msg5)
        cmd_6 = f'''ls -al {macro.DB_INSTANCE_PATH}/{par_path}/{path2}'''
        LOG.info(cmd_6)
        msg6 = self.user.sh(cmd_6).result()
        LOG.info(msg6)
        self.assertIn(path2, msg6)
        cmd_7 = f'''ls -al {macro.DB_INSTANCE_PATH}/{par_path}/{path3}'''
        LOG.info(cmd_7)
        msg7 = self.user.sh(cmd_7).result()
        LOG.info(msg7)
        self.assertIn(path3, msg7)
        LOG.info('---------------testpoint:验证路径正确性-------------')
        # 修改权限000后不能插入数据
        cmd_8 = f'''chmod 000 {macro.DB_INSTANCE_PATH}/{par_path}/{path2}'''
        msg8 = self.user.sh(cmd_8).result()
        LOG.info(msg8)
        sql_cmd8 = '''insert into sales values(1, 12, 
            '2019-02-05 11:00:00', 'a', 1, 1, 1);
            '''
        msg81 = self.sh_primy.execut_db_sql(sql_cmd8)
        LOG.info(msg81)
        self.assertIn(' Permission denied', msg81)
        # 恢复权限后可以插入
        cmd_9 = f'''chmod 600 {macro.DB_INSTANCE_PATH}/{par_path}/{path2}'''
        msg9 = self.user.sh(cmd_9).result()
        LOG.info(msg9)
        sql_cmd9 = '''insert into sales values(1, 12, 
            '2019-02-05 11:00:00', 'a', 1, 1, 1);
            '''
        msg10 = self.sh_primy.execut_db_sql(sql_cmd9)
        LOG.info(msg10)
        self.assertIn('INSERT', msg10)

    def tearDown(self):
        sql_cmd = 'drop table sales cascade;'
        msg = self.sh_primy.execut_db_sql(sql_cmd)
        LOG.info(msg)
        self.assertTrue(msg.find("DROP TABLE") > -1)
        LOG.info('--Opengauss_Function_Sysmanagement_Dbobject_Pfnode_Case0001'
            '结束--')
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
Case Type   : 服务端工具
Case Name   : 从备机导出数据，主机导入
Description :
    1.连接数据库主机，并创建数据
    2.导出备机数据库的数据
    3.清理环境
Expect      :
    1.创建成功
    2.备机导出失败(gs_dump is not supported on standby or cascade standby)
    3.清理完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '需主备环境，若为单机环境则不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Tools_gs_dump_Case0128 start---')
        self.Pri_User = Node('PrimaryDbUser')
        self.St_User = Node('Standby1DbUser')
        self.constant = Constant()
        self.Common = Common()
        self.Standby_user = CommonSH('Standby1DbUser')
        self.dump_path1 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump1.sql')
        self.assert_msg = f'gs_dump is not supported on ' \
            f'standby or cascade standby'
        self.db_name = "db_dump0128"
        self.tb_name = "t_dump0128"

    def test_tools_dump(self):
        text = '---step1.1:创建数据库;expect:创建成功---'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f'''
            drop database if exists {self.db_name};
            create database {self.db_name};
            ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '---step1.2:在创建的数据库中创建表和数据;expect:创建成功---'
        self.log.info(text)
        sql_cmd = f'''drop table if  exists {self.tb_name};
            create table {self.tb_name} (id int);
            insert into {self.tb_name} values (generate_series(1,10));
            select count(*) from {self.tb_name};'''
        self.log.info(sql_cmd)
        sql_result = Primary_SH.execut_db_sql(sql=sql_cmd,
                                              dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)
        self.assertIn('10', sql_result, '执行失败:' + text)

        text = '---step1.3:等待备机完成数据同步;expect:同步成功---'
        self.log.info(text)
        node_num = self.Common.get_node_num(self.Pri_User)
        self.log.info(node_num)
        consistency_flag = Primary_SH.check_location_consistency('standby',
                                                                 node_num,
                                                                 300)
        self.assertTrue(consistency_flag, '执行失败:' + text)

        text = '---step1.4:查看备机数据是否同步;expect:同步成功---'
        self.log.info(text)
        sql_cmd = f'''select count(*) from {self.tb_name};'''
        sql_result = self.Standby_user.execut_db_sql(sql=sql_cmd,
                                              dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn('10', sql_result, '执行失败:' + text)

        text = '---step2:在备机上执行导出操作;expect:导出失败---'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_dump {self.db_name} \
            -p {self.St_User.db_port} \
            -f {self.dump_path1};
            '''
        self.log.info(dump_cmd)
        dump_result = self.St_User.sh(dump_cmd).result()
        self.log.info(dump_result)
        self.assertIn(self.assert_msg, dump_result, '执行失败:' + text)

    def tearDown(self):
        text = '--------------step3:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.dump_path1};'
        self.log.info(clear_cmd)
        clear_result = self.St_User.sh(clear_cmd).result()
        self.log.info(clear_result)
        sql_cmd = Primary_SH.execut_db_sql(
            f'drop database if exists  {self.db_name};')
        self.log.info(sql_cmd)
        self.assertEqual('', clear_result, '执行失败:' + text)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.log.info(
            '------Opengauss_Function_Tools_gs_dump_Case0128 finish------')

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
Case Name   : 从主机导出数据，备机导入
Description :
    1.连接数据库主机，并创建数据
    2.导出数据库的数据
    3.将导出的数据从主机复制到备机上
    4.从备机导入数据
    5.清理环境(注意主备环境的导出文件)
Expect      :
    1.数据创建成功
    2.数据导出成功
    3.导出数据复制成功
    4.从备机导入失败（备机为read-only状态，无法导入）
    5.环境清理完成
History     : 
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
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
            '---Opengauss_Function_Tools_gs_dump_Case0127start---')
        self.Pri_User = Node('PrimaryDbUser')
        self.Pri_Root = Node('PrimaryRoot')
        self.St_User = Node('Standby1DbUser')
        self.St_Root = Node('Standby1Root')
        self.constant = Constant()
        self.dump_path1 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump1.sql')
        self.dump_path2 = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump2.sql')
        self.db_name1 = "db_dump0127_01"
        self.db_name2 = "db_dump0127_02"
        self.tb_name = "t_dump0127"

    def test_tools_dump(self):
        text = '---step1.1:创建数据库;expect:创建成功---'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f'''
            drop database if exists {self.db_name1};
            drop database if exists {self.db_name2};
            create database {self.db_name1};
            create database {self.db_name2};
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
                                              dbname=f'{self.db_name1}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)
        self.assertIn('10', sql_result, '执行失败:' + text)

        text = '---step2:连接创建好的数据库,执行导出操作;expect:导出成功---'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_dump {self.db_name1} \
            -p {self.Pri_User.db_port} \
            -f {self.dump_path1};
            '''
        self.log.info(dump_cmd)
        dump_result = self.Pri_User.sh(dump_cmd).result()
        self.log.info(dump_result)
        self.assertIn(f'dump database {self.db_name1} successfully',
                      dump_result,
                      '执行失败:' + text)

        text = '-----step3:将导出的数据从主机复制到备机上;expect:复制成功---'
        self.log.info(text)
        scp_cmd = f'''source {macro.DB_ENV_PATH};
        expect <<EOF 
        spawn scp {self.dump_path1} \
        {self.St_Root.ssh_user}@{self.St_Root.ssh_host}:{self.dump_path2}
        expect "Password:"
        send "{self.Pri_User.db_password}\r"
        expect eof
        '''
        self.log.info(scp_cmd)
        msg = self.Pri_User.sh(scp_cmd).result()
        self.log.info(msg)
        self.log.info('---查看复制是否成功---')
        ls_cmd = f'chmod 755 {self.dump_path2};' \
            f'ls {os.path.dirname(self.dump_path2)};'
        self.log.info(ls_cmd)
        ls_msg = self.St_Root.sh(ls_cmd).result()
        self.log.info(ls_msg)
        self.assertIn('dump2.sql', ls_msg)

        text = '-----step4:在备机连接新的数据库进行导入;expect:导入失败---'
        self.log.info(text)
        gsql_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gsql {self.db_name2} " \
            f"-p {self.St_User.db_port} " \
            f"-f {self.dump_path2} " \
            f"-r;"
        self.log.info(gsql_cmd)
        gsql_result = self.St_User.sh(gsql_cmd).result()
        self.log.info(gsql_result)
        self.assertIn('read-only transaction', gsql_result,
                      '执行失败:' + text)
        self.assertIn('ERROR:  cannot execute', gsql_result,
                      '执行失败:' + text)

    def tearDown(self):
        text = '--------------step5:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.dump_path1};'
        self.log.info(rm_cmd)
        result = self.Pri_Root.sh(rm_cmd).result()
        self.log.info(result)
        rm_cmd = f'rm -rf {self.dump_path2};'
        self.log.info(rm_cmd)
        result = self.St_Root.sh(rm_cmd).result()
        self.log.info(result)
        sql_cmd = Primary_SH.execut_db_sql(
            f'drop database if exists  {self.db_name1};'
            f'drop database if exists  {self.db_name2};')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Tools_gs_dump_Case0127finish------')

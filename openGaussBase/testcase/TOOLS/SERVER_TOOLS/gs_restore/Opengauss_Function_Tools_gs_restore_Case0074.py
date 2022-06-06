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
Case Name   : 连接用户不是系统管理员,没有-W参数,导入到数据库会提示用户输入密码(用户赋予权限)
Description :
    1.创建数据
    1)创建数据库
    2)创建表并插入数据
    3)创建角色,并赋予权限
    2.导出数据
    3.导入之前导出的数据，提示输入密码
    4.清理环境
Expect      :
    1.创建数据
    1)创建数据库成功
    2)创建表并插入数据成功
    3)创建角色,并赋予权限成功
    2.导出数据成功
    3.导入成功
    4.清理环境
History     : 
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Tools_gs_restore_Case0074start---')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.constant = Constant()
        self.dump_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'dump.tar')
        self.db_name1 = "db_restore0074_01"
        self.db_name2 = "db_restore0074_02"
        self.tb_name = "t_restore0074"
        self.u_name = "u_restore0074"

    def test_tools_restore(self):
        text = '---step1:创建测试数据;expect:创建成功---'
        self.log.info(text)
        text = '----------step1.1:创建数据库;expect:创建成功-----------'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''
            drop database if exists {self.db_name1};
            drop database if exists {self.db_name2};
            create database {self.db_name1};
            create database {self.db_name2};
            ''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        text = '--------step1.2:在创建成功的数据库中创建数据;expect:创建成功---------'
        self.log.info(text)
        sql_cmd = f'''drop table if  exists {self.tb_name};
            drop user if  exists {self.u_name};
            create table {self.tb_name} (id int);
            insert into {self.tb_name} values (generate_series(1,10));
            select count(*) from {self.tb_name};
            create user {self.u_name} identified \
            by \'{macro.COMMON_PASSWD}\';
            grant all privileges to {self.u_name};
            '''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name1}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)
        self.assertIn('10', sql_result, '执行失败:' + text)

        text = '---step2:执行导出操作;expect:导出成功---'
        self.log.info(text)
        dump_cmd = f'''source {macro.DB_ENV_PATH};\
            gs_dump {self.db_name1} \
            -p {self.Primary_Node.db_port} \
            -F t \
            -f {self.dump_path};
            '''
        self.log.info(dump_cmd)
        dump_result = self.Primary_Node.sh(dump_cmd).result()
        self.log.info(dump_result)
        self.assertIn(f'dump database {self.db_name1} successfully',
                      dump_result,
                      '执行失败:' + text)

        text = '-----step3:导入之前导出的数据,提示输入密码;expect:密码输入正确,导入成功-----'
        self.log.info(text)
        restore_cmd = f'''source {macro.DB_ENV_PATH};
            expect <<EOF 
            spawn gs_restore -d {self.db_name2} -U  {self.u_name} \
            -p {self.Primary_Node.db_port} -c  {self.dump_path}
            expect "Password:"
            send "{macro.COMMON_PASSWD}\r"
            expect eof\n''' + '''EOF'''
        self.log.info(restore_cmd)
        restore_result = self.Primary_Node.sh(restore_cmd).result()
        self.log.info(restore_result)
        self.assertIn('restore operation successful', restore_result,
                      '执行失败:' + text)

        self.log.info('---在导入的数据库中查询表和数据都存在---')
        sql_cmd = f"select id from {self.tb_name};"
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name2}')
        self.log.info(sql_result)
        self.assertIn(f'10 row', sql_result, '执行失败:' + text)

    def tearDown(self):
        text = '--------------step4:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.dump_path};'
        self.log.info(rm_cmd)
        result = self.Root_Node.sh(rm_cmd).result()
        self.log.info(result)
        sql_cmd = self.pri_sh.execut_db_sql(
            f'drop database if exists  {self.db_name1};'
            f'drop database if exists  {self.db_name2};'
            f'drop user if  exists {self.u_name};')
        self.log.info(sql_cmd)
        self.log.info(
            '------Opengauss_Function_Tools_gs_restore_Case0074finish------')

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
Case Type   : 防篡改
Case Name   : 三权分立打开时验证超级用户对用户私有模式下创建的分区表有insert权限
                (超级用户为初始用户权限，访问普通用户创建的分区表)
Description :
    1.设置参数并重启数据库enableSeparationOfDuty=on
    2.创建普通用户
    3.切换普通用户创建分区表
    4.超级用户对分区表进行insert操作并查询表
      copyto命令导出表数据
    5.用copy from命令向表中导入数据并查询表
    6.清理环境
Expect      :
    1.成功
    2.成功
    3.成功
    4.数据插入成功表中有两条数据
    5.导入成功且表中有四条数据
    6.成功
History     :
"""


import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class ModifyCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.table_name = 't_security_insertprivilege_0009'
        self.user_name = 'u_security_insertprivilege_0009'
        self.file_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      'security_insertprivilege_0009.txt')
        self.default_value = self.common.show_param('enableSeparationOfDuty')

    def test_security(self):
        text = '-----step1：设置参数并重启数据库enableSeparationOfDuty=on; ' \
               'expect:成功-----'
        self.log.info(text)
        mod_msg = \
            self.primary_sh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'enableSeparationOfDuty=on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        restart_msg = self.primary_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '-----step2：创建普通用户 expect:成功-----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(
            f"drop user if exists {self.user_name} cascade;"
            f"create user {self.user_name} password "
            f"'{macro.PASSWD_REPLACE}';")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '----step3:切换普通用户创建分区表 expect:成功----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            set role {self.user_name} password '{macro.PASSWD_REPLACE}';
            create table {self.user_name}.{self.table_name}
            (id int,name varchar(100))partition by range(id)
            (partition p1 values less than(10),
            partition p2 values less than(20),
            partition p3 values less than(30),
            partition pmax values less than(maxvalue)
            );''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      "执行失败:" + text)
        self.assertIn(self.constant.SET_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)

        text = '----step4:超级用户对分区表进行insert操作并查询表' \
               '用copy to命令导出表数据 expect:数据插入成功表中有两条数据----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            insert into {self.user_name}.{self.table_name} 
            (id,name) values (1,'beijing'),(2,'shanghai');
            select * from {self.user_name}.{self.table_name};
            copy {self.user_name}.{self.table_name} to '{self.file_path}';''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd,
                      "执行失败:" + text)
        self.assertIn('COPY', sql_cmd, "执行失败:" + text)
        self.assertIn('2 rows', sql_cmd, "执行失败:" + text)

        text = '----step5:用copy from命令向表中导入数据并查询表 ' \
               'expect:导入成功且表中有四条数据----'
        self.log.info(text)
        sql_cmd = self.primary_sh.execut_db_sql(f'''
            copy {self.user_name}.{self.table_name} from '{self.file_path}';
            select * from {self.user_name}.{self.table_name};''')
        self.log.info(sql_cmd)
        self.assertIn('COPY', sql_cmd, "执行失败:" + text)
        self.assertIn('4 rows', sql_cmd, "执行失败:" + text)

    def tearDown(self):
        text = '----step6:清理环境 expect:成功----'
        self.log.info(text)
        self.log.info('恢复参数默认值')
        mod_msg1 = \
            self.primary_sh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f'enableSeparationOfDuty='
                                          f'{self.default_value}')
        self.log.info(mod_msg1)
        self.assertTrue(mod_msg1, '执行失败:' + text)
        restart_msg = self.primary_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.primary_sh.get_db_cluster_status()
        self.log.info('删除用户')
        sql_cmd = self.primary_sh.execut_db_sql(
            f"drop user {self.user_name} cascade;")
        self.log.info(sql_cmd)
        self.log.info('删除文件')
        del_file = f'''rm -rf {self.file_path}'''
        self.log.info(del_file)
        self.common.get_sh_result(self.dbuserNode, del_file)
        cmd = f'if [ -f {self.file_path} ]; then echo "does exists"; ' \
            f'else echo "not exists"; fi'
        self.log.info(del_file)
        file_judgments = self.common.get_sh_result(self.dbuserNode, cmd)
        self.assertIn('not exists', file_judgments, "执行失败" + text)
        self.assertEqual(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                         '执行失败:' + text)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

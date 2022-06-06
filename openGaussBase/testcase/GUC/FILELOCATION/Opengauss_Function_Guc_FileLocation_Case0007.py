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
Case Type   : GUC
Case Name   : 使用ALTER SYSTEM SET修改数据库参数data_directory为不存在目录
Description :
        1.查询data_directory默认值
        2.创建测试目录
        3.使用ALTER SYSTEM SET修改数据库参数data_directory为不存在目录并
        重启数据库
        4.kill -9
        5.恢复参数默认值
        6.连接数据库执行ddl操作
        7.清理环境
Expect      :
        1.安装时指定，如果在安装时不指定，则默认不初始化数据库
        2.创建成功
        3.重启失败
        4.kill -9成功，数据库状态为Unavailable
        5.恢复成功
        6.执行成功
        7.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0007 start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.pri_root_node = Node('PrimaryRoot')
        self.com = Common()
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, 'cluster', 'dn1')
        self.new_dn1 = os.path.join(self.file_path, 'testdir')
        self.tb_name = "tb_guc_filelocation_case0007"

    def test_data_directory(self):
        text = '---step1:查询默认值;expect:安装时指定，' \
               '如果在安装时不指定，则默认不初始化数据库---'
        self.log.info(text)
        sql_cmd = self.com.show_param("data_directory")
        self.assertTrue(macro.DB_INSTANCE_PATH in sql_cmd, '执行失败:' + text)

        text = '---step2:创建测试目录;expect:创建成功---'
        self.log.info(text)
        touch_cmd = f'''mkdir -p {self.file_path};'''
        self.log.info(touch_cmd)
        msg = self.user_node.sh(touch_cmd).result()
        self.log.info(msg)
        self.assertEqual(msg, '', '执行失败:' + text)

        text = '---step3:使用alter system set设置data_directory为不存在目录' \
               '并重启数据库;expect:重启失败--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''alter system set \
            data_directory to '{self.new_dn1}'; ''')
        self.log.info(sql_cmd)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        self.assertFalse(msg, '执行失败:' + text)

        text = '---step4:kill -9;expect:kill -9成功，数据库状态为Unavailable-'
        self.log.info(text)
        self.com.kill_pid(self.pri_root_node, '9')
        result = self.pri_sh.get_db_cluster_status()
        self.assertIn("Unavailable", result, '执行失败:' + text)

        text = '---step5:恢复参数默认值;expect:恢复成功，数据库重启成功---'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"data_directory="
                                           f"'{macro.DB_INSTANCE_PATH}'")
        self.log.info(result)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '---step6:连接数据库执行ddl操作;expect:执行成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'drop table if exists '
                                            f'{self.tb_name};'
                                            f'create table {self.tb_name}'
                                            f'(id int);')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

    def tearDown(self):
        text = '---step6:清理环境;expect:清理环境完成---'
        self.log.info(text)
        rm_cmd = f'''rm -rf {self.file_path}'''
        self.log.info(rm_cmd)
        msg = self.user_node.sh(rm_cmd).result()
        self.log.info(msg)
        drop_cmd = self.pri_sh.execut_db_sql(f'drop table if exists '
                                             f'{self.tb_name};')
        self.log.info(drop_cmd)
        self.log.info('断言teardown成功')
        self.assertEqual('', msg, '执行失败:' + text)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd,
                      '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0007 finish-')

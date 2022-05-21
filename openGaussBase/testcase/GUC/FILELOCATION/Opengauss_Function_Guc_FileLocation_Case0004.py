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
Case Name   : 使用ALTER SYSTEM SET修改数据库参数data_directory
Description :
        1.查询data_directory默认值
        2.使用ALTER SYSTEM SET修改数据库参数data_directory为自定义路径
        并重启数据库
        3.kill -9
        4.恢复参数默认值
        5.连接数据库执行ddl操作
        6.清理环境
Expect      :
        1.安装时指定
        2.om方式重启失败
        3.kill -9成功，数据库状态为Unavailable
        4.恢复参数默认值成功，重启数据库成功
        5.执行成功
        6.清理环境完成
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Guc04(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-----os.path.basename(__file__)} start-----')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, 'cluster')
        self.pg_file = os.path.join(macro.DB_BACKUP_PATH,
                                    macro.DB_PG_CONFIG_NAME)
        self.new_dn1 = os.path.join(self.file_path, 'dn1')
        self.pri_root_node = Node('PrimaryRoot')
        self.com = Common()
        self.tb_name = "tb_guc_filelocation_case0004"

    def test_file_location(self):
        s1_text = '-----step1:查询默认值;expect:安装时指定-----'
        self.log.info(s1_text)
        sql_cmd = self.com.show_param("data_directory")
        self.assertTrue(macro.DB_INSTANCE_PATH in sql_cmd,
                        f'执行失败: {s1_text}')

        s2_text = '-----step2:使用ALTER SYSTEM SET修改数据库参数' \
                  'data_directory并重启数据库;expect:om方式重启失败-----'
        self.log.info(s2_text)
        sql_cmd = self.pri_sh.execut_db_sql(f"alter system set "
                                            f"data_directory to "
                                            f"'{self.new_dn1}';")
        self.log.info(sql_cmd)
        self.assertIn('ALTER SYSTEM SET', sql_cmd, f'执行失败: {s2_text}')
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        self.assertFalse(msg, f'执行失败: {s2_text}')

        s3_text = '-----step3:kill -9;expect:kill -9成功，' \
                  '数据库状态为Unavailable-----'
        self.log.info(s3_text)
        self.com.kill_pid(self.pri_root_node, '9')
        result = self.pri_sh.get_db_cluster_status()
        self.assertIn("Unavailable", result, f'执行失败: {s3_text}')

        s4_text = '-----step4:恢复参数默认值;expect:恢复成功，' \
                  '数据库重启成功-----'
        self.log.info(s4_text)
        guc_cmd = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"data_directory="
                                            f"'{macro.DB_INSTANCE_PATH}'")
        self.log.info(guc_cmd)
        restart_cmd = self.pri_sh.restart_db_cluster()
        self.log.info(restart_cmd)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        f'执行失败: {s4_text}')

        s5_text = '-----step5:连接数据库执行ddl操作;expect:执行成功-----'
        self.log.info(s5_text)
        sql_cmd = self.pri_sh.execut_db_sql(f'drop table if exists '
                                            f'{self.tb_name};'
                                            f'create table {self.tb_name}'
                                            f'(id int);')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      f'执行失败: {s5_text}')

    def tearDown(self):
        s6_text = '---step6:清理环境;expect:清理环境完成---'
        self.log.info(s6_text)
        rm_cmd = f"rm -rf {self.file_path}"
        self.log.info(rm_cmd)
        rm_expect = self.user_node.sh(rm_cmd).result()
        self.log.info(rm_expect)
        drop_cmd = self.pri_sh.execut_db_sql(f'drop table if exists '
                                             f'{self.tb_name};')
        self.log.info(drop_cmd)
        self.log.info('断言teardown成功')
        self.assertEqual(len(rm_expect), 0, f'执行失败: {s6_text}')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd,
                      f'执行失败: {s6_text}')
        self.log.info('-----os.path.basename(__file__)} end-----')

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
Case Name   : data_directory参数使用gs_guc reload设置
Description :
        1.查询data_directory默认值
        2.创建测试目录
        3.data_directory参数使用gs_guc reload设置为自定义路径
        4.查询data_directory参数值
        5.连接数据库执行ddl操作
        6.清理环境
Expect      :
        1.安装时指定，如果在安装时不指定，则默认不初始化数据库
        2.创建成功
        3.gs_guc命令执行成功
        4.参数值不变，POSTMASTER型参数使用gs_guc reload设置无效
        5.执行成功
        6.清理环境完成
             拷贝dn1目录失败
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
            '-Opengauss_Function_Guc_FileLocation_Case0002 start-')
        self.constant = Constant()
        self.com = Common()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, 'cluster')
        self.new_dn1 = os.path.join(self.file_path, 'dn1')
        self.tb_name = "tb_guc_filelocation_case0002"

    def test_data_directory(self):
        text = '---step1:查询默认值;expect:安装时指定，' \
               '如果在安装时不指定，则默认不初始化数据库---'
        self.log.info(text)
        sql_cmd = self.com.show_param("data_directory")
        self.assertTrue(macro.DB_INSTANCE_PATH in sql_cmd, '执行失败:' + text)

        text = '---step2:创建测试目录expect:创建成功---'
        self.log.info(text)
        touch_cmd = f"mkdir -p {self.file_path};"
        self.log.info(touch_cmd)
        msg = self.user_node.sh(touch_cmd).result()
        self.log.info(msg)
        self.assertEqual(msg, '', '执行失败:' + text)

        text = '---step3:使用gs_guc reload设置data_directory为自定义路径;' \
               'expect:gs_guc命令执行成功'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('reload',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"data_directory='{self.new_dn1}'")
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)

        text = '---step4:查询;expect:参数值不变---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show data_directory;')
        self.log.info(sql_cmd)
        self.assertEqual(macro.DB_INSTANCE_PATH,
                         sql_cmd.splitlines()[2].strip(), '执行失败:' + text)

        text = '---step5:连接数据库执行ddl操作;expect:执行成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'drop table if exists '
                                            f'{self.tb_name};'
                                            f'create table {self.tb_name}'
                                            f'(id int) ;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

    def tearDown(self):
        text = '---step6:清理环境;expect:清理环境完成---'
        self.log.info(text)
        rm_cmd = f"rm -rf {self.file_path}"
        self.log.info(rm_cmd)
        msg1 = self.user_node.sh(rm_cmd).result()
        self.log.info(msg1)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"data_directory="
                                           f"'{macro.DB_INSTANCE_PATH}'")
        self.log.info(result)
        msg2 = self.pri_sh.restart_db_cluster()
        self.log.info(msg2)
        status = self.pri_sh.get_db_cluster_status()
        drop_cmd = self.pri_sh.execut_db_sql(f'drop table if exists '
                                             f'{self.tb_name};')
        self.log.info(drop_cmd)

        self.log.info('断言teardown成功')
        self.assertEqual('', msg1, '执行失败:' + text)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd,
                      '执行失败:' + text)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0002 finish-')

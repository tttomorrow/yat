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
Case Name   : 使用gs_guc set方法设置参数current_schema为不存在的模式，建表查询
Description :
        1.查询current_schema默认值
        2.修改current_schema为不存在的模式
        3.建表并查询表模式
        4.恢复参数默认值
        5.重启数据库
        6.show参数值
        7.清理环境
Expect      :
        1.显示默认值为"$user",public
        2.修改成功
        3.表模式为public
        4.参数值恢复成功
        5.数据库重启成功
        6.参数值恢复成功
        7.清理环境完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_ClientConnection_Case0229start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.dbuser = Node('PrimaryDbUser')
        self.tb_name = "tb_guc_0229"
        self.sc_name = "sc_guc_0229"

    def test_current_schema(self):
        text = '---step1:查询默认值;expect:默认值"$user",public---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show current_schema;')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        text = '--step2:修改current_schema为不存在的模式;expect:修改成功--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"current_schema='{self.sc_name}'")
        self.assertTrue(result, '执行失败:' + text)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        text = '---step3:建表并查询表模式;expect:表模式为public---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f"drop table if exists "
                                            f"{self.tb_name} cascade;"
                                            f"create table {self.tb_name}"
                                            f"(id int);select schemaname,"
                                            f"tablename from pg_tables "
                                            f"where "
                                            f"tablename='{self.tb_name}'")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertIn('public', sql_cmd, '执行失败:' + text)

        text = '--step4:恢复参数默认值;expect:参数默认值恢复成功--'
        self.log.info(text)
        restore_cmd = f"sed -i 's/{self.sc_name}/\"$user\",public/g'  " \
                      f"{macro.DB_INSTANCE_PATH}/postgresql.conf"
        self.log.info(restore_cmd)
        find_msg = self.dbuser.sh(restore_cmd).result()
        self.log.info(find_msg)
        text = '--step5:重启数据库;expect:数据库重启成功--'
        self.log.info(text)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step6:show参数默认值;expect:参数值恢复成功--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'show current_schema;')
        self.log.info(sql_cmd)
        self.assertIn(self.res, sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '---step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f"drop table if exists "
                                            f"{self.tb_name} cascade;")
        self.log.info(sql_cmd)

        self.log.info(
            '-Opengauss_Function_Guc_ClientConnection_Case0229finish-')

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
Case Name   : 参数synchronous_commit值设为2，不停止备机，执行rollback
Description :
    1.将参数synchronous_commit设为2
    gs_guc reload -D /xx/dn1 -c "synchronous_commit = 2";
    2.重启备机
    gs_ctl stop -D /xx/dn1
    gs_ctl start -D /dxx/dn1 -M standby
    3.主机开启事务并建表并插入数据，然后执行rollback
    start transaction;
    drop table if exists tablename;
    create table tablename(id int);
    insert into tablename values(generate_series(1,100000));
    rollback;
    4.查询主备机表数据是否一致
     select count(*) from tablename;
    5.检查主机和备机的日志，日志文件大小是否一致
    6.删除表
    drop table tablename;
    7.恢复默认值
Expect      :
    1.参数设置成功
    2.备机重启成功
    3.主机开启事务并建表并插入数据，执行rollback成功
    4.表不存在
    5.主备机日志信息一致
    6.表删除成功
    7.恢复默认值
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

COMMONSH = CommonSH("PrimaryDbUser")


@unittest.skipIf(1 == COMMONSH.get_node_num(), "单机不执行")
class Guc(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Guc_WAL_Case0089_开始---')
        self.pri_com = CommonSH('PrimaryDbUser')
        self.sta_com = CommonSH("Standby1DbUser")
        self.pri_user = Node('PrimaryDbUser')
        self.sta_user = Node('Standby1DbUser')
        self.constant = Constant()
        self.common = Common()
        self.tb_name = "t_guc0089"
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'pg_xlog')

    def test_guc(self):
        text = '--step1.1.show参数默认值;expect:参数默认值正常显示--'
        self.log.info(text)
        self.default_value = self.common.show_param("synchronous_commit")

        text = '--step1.2.修改synchronous_commit值为2;expect:修改参数值成功--'
        self.log.info(text)
        guc_msg = self.pri_com.execute_gsguc('reload',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f"synchronous_commit=2")
        self.log.info(guc_msg)
        self.assertTrue(guc_msg, '执行失败:' + text)

        text = '--step1.3.show参数值;expect:参数值修改成功--'
        self.log.info(text)
        self.modify_value = self.common.show_param("synchronous_commit")
        self.assertIn('remote_apply', self.modify_value, '执行失败:' + text)

        text = '-----step2.重启备机;except:备机重启成功-----'
        self.log.info(text)
        result = self.sta_com.execute_gsctl("stop", "server stopped")
        self.log.info(result)
        result = self.sta_com.execute_gsctl("start", "server started",
                                            "-M standby")
        self.log.info(result)
        self.assertTrue(result, '执行失败' + text)

        text = '--step3.主机开启事务并建表并插入数据,之后执行rollback;expect:操作成功--'
        self.log.info(text)
        sql_cmd = f'''start transaction;
            drop table if  exists {self.tb_name};
            create table {self.tb_name} (id int);
            insert into {self.tb_name} values (generate_series(1,100000));
            select pg_sleep(30);
            rollback;
            '''
        self.log.info(sql_cmd)
        sql_pri = self.pri_com.execut_db_sql(sql_cmd)
        self.log.info(sql_pri)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, sql_pri,
                      '执行失败:' + text)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_pri,
                      '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_pri,
                      '执行失败:' + text)
        self.assertIn(self.constant.ROLLBACK_MSG, sql_pri,
                      '执行失败:' + text)

        text = '--step4.检查主备表信息;expect:表不存在--'
        self.log.info(text)
        sql_pri = self.pri_com.execut_db_sql(
            f'select count(*) from {self.tb_name};')
        self.log.info(sql_pri)
        sql_sta = self.sta_com.execut_db_sql(
            f'select count(*) from {self.tb_name};')
        self.log.info(sql_sta)
        self.assertIn(f'relation "{self.tb_name}" does not exist',
                      sql_pri, '执行失败:' + text)
        self.assertEqual(sql_pri, sql_sta, '执行失败:' + text)
        text = '--step5.检查主备日志信息;expect:日志信息一致--'
        self.log.info(text)
        find_cmd1 = f"ls -t {self.log_path}| head -1 "
        self.log.info(find_cmd1)
        find_msg1 = self.pri_user.sh(find_cmd1).result()
        self.log.info(find_msg1)
        du_cmd1 = f'cd {self.log_path};du -h {find_msg1};'
        self.log.info(du_cmd1)
        du_msg1 = self.pri_user.sh(du_cmd1).result()
        log1 = float(du_msg1.split()[0][:-1])
        self.log.info(log1)
        find_cmd2 = f"ls -t {self.log_path}| head -1 "
        self.log.info(find_cmd2)
        find_msg2 = self.sta_user.sh(find_cmd2).result()
        self.log.info(find_msg2)
        du_cmd2 = f'cd {self.log_path};du -h {find_msg2};'
        self.log.info(du_cmd2)
        du_msg2 = self.sta_user.sh(du_cmd2).result()
        log2 = float(du_msg2.split()[0][:-1])
        self.log.info(log2)
        self.assertEqual(log1, log2, '执行失败:' + text)

        text = '--step6.删除表;expect:删除成功--'
        self.log.info(text)
        sql_cmd = self.pri_com.execut_db_sql(
            f'drop table if  exists {self.tb_name};')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_cmd,
                      '执行失败:' + text)

    def tearDown(self):
        text = '--step7.1恢复默认值;expect:恢复成功--'
        self.log.info(text)
        set_cmd = self.pri_com.execute_gsguc('reload',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f"synchronous_commit="
                                             f"{self.default_value}")
        self.log.info(set_cmd)
        text = '--step7.2重启数据库;expect:重启数据库成功--'
        self.log.info(text)
        status = self.pri_com.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.common.show_param("synchronous_commit")
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info('---Opengauss_Function_Guc_WAL_Case0089_结束---')

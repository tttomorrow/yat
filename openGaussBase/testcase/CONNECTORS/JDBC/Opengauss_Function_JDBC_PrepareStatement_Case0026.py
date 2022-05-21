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
Case Type   : 数据库系统
Case Name   : MOT外表（含varchar类型字段）有存量数据场景下，JDBC预编译插入功能验证
Description :
    1.关闭增量检查点开关enable_incremental_checkpoint=off
    2.重启数据库生效
    3.创建含varchar类型字段的外表，并插入1条数据
    4.创建java配置文件
    5.编译java文件
    6.运行java预编译插入代码（insert10条数据）,执行两次
    7.查询外表数据
Expect      :
    1.关闭增量检查点开关，操作成功
    2.重启数据库生效，操作成功
    3.创建含varchar类型字段的外表，并插入1条数据；操作成功
    4.创建java配置文件成功
    5.编译java文件成功
    6.运行java预编译插入代码（insert10条数据）,执行两次，操作成功
    7.查询外表数据，总计21条
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


class JDBCPrepareStatement(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("----this is setup----")
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_root = Node(node='PrimaryRoot')
        self.target_path = os.path.join(macro.DB_BACKUP_PATH, "JDBC_test")
        self.properties = os.path.join(self.target_path,
                                       "jdbc_preparestat_Case0026.properties")
        self.java_name = "jdbc_PrepareStatement_Case0026"
        self.tb_name = "tb_jdbc_PrepareStatement_Case0026"
        self.com = Common()
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')

        step_txt = '----查询enable_incremental_checkpoint初始值----'
        self.log.info(step_txt)
        self.init_para = self.com.show_param("enable_incremental_checkpoint")

    def test_main(self):
        step_txt = '----step1:关闭增量检查点开关; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'enable_incremental_checkpoint=off')
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info('----step2:重启数据库生效; expect:重启成功----')
        restart = self.pri_sh.restart_db_cluster()
        self.assertTrue(restart, '执行失败:' + step_txt)

        step_txt = '----step3:创建含varchar类型字段的外表，并插入1条数据； expect:操作成功----'
        self.log.info(step_txt)
        create_sql = f"drop foreign table if exists {self.tb_name};" \
            f"create foreign TABLE {self.tb_name} " \
            f"(id int, aa varchar(10) ,id2 int);" \
            f"insert into {self.tb_name} values(11, '1a', 11);"
        result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, result,
                      "执行失败" + step_txt)
        self.assertIn('INSERT 0 1', result, "执行失败" + step_txt)

        step_txt = '----step4:创建配置文件; expect:创建成功----'
        self.log.info(step_txt)
        self.com.scp_file(self.pri_root,
                          f"{self.java_name}.java", self.target_path)
        result = self.pri_root.sh(f"touch {self.properties}").result()
        self.log.info(result)
        config = f'echo "password=' \
            f'{self.pri_dbuser.db_password}"> {self.properties}'
        self.pri_root.sh(config)
        config = f'echo "port={self.pri_dbuser.db_port}">> ' \
            f'{self.properties}'
        self.pri_root.sh(config)
        config = f'echo "hostname={self.pri_dbuser.db_host}">> ' \
            f'{self.properties}'
        self.pri_root.sh(config)
        config = f'echo "user={self.pri_dbuser.db_user}">> ' \
            f'{self.properties}'
        self.pri_root.sh(config)
        config = f'echo "dbname={self.pri_dbuser.db_name}">> ' \
            f'{self.properties}'
        self.pri_root.sh(config)
        config = f'echo "tbname={self.tb_name}">> {self.properties}'
        self.pri_root.sh(config)
        config = f'cat {self.properties}'
        result = self.pri_root.sh(config).result()
        self.log.info(result)
        self.assertTrue("password=" in result and "port=" in result
                        and "hostname=" in result and "user=" in result
                        and "dbname=" in result and "tbname=" in result,
                        "执行失败" + step_txt)

        step_txt = '----step5:编译java文件; expect:编译成功----'
        self.log.info(step_txt)
        self.pri_root.scp_put(macro.JDBC_PATH,
                              f"{self.target_path}/postgresql.jar")
        cmd = f"javac -encoding utf-8 -cp " \
            f"{os.path.join(self.target_path, 'postgresql.jar')} " \
            f"{os.path.join(self.target_path, f'{self.java_name}.java')}"
        self.log.info(cmd)
        result = self.pri_root.sh(cmd).result()
        self.log.info(result)
        self.assertEqual('', result, "执行失败" + step_txt)

        step_txt = '----step6:运行java预编译插入代码（insert10条数据）执行两次; expect:操作成功----'
        self.log.info(step_txt)
        java_cmd = f"java -cp " \
            f"{os.path.join(self.target_path, 'postgresql.jar')}" \
            f":{self.target_path} " \
            f"{self.java_name} -F {self.properties}"
        self.log.info(java_cmd)
        java_result = self.com.get_sh_result(self.pri_root, java_cmd)
        self.assertIn('插入成功', java_result, "执行失败" + step_txt)
        java_result = self.com.get_sh_result(self.pri_root, java_cmd)
        self.assertIn('插入成功', java_result, "执行失败" + step_txt)

        step_txt = '----step7: 查询外表数据; expect:查询成功，总计21条----'
        self.log.info(step_txt)
        tb_sql = f"select * from {self.tb_name} "
        result = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        self.assertIn('21 rows', result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        step8_txt = '----step8:清理mot外表; expect:清理成功----'
        self.log.info(step8_txt)
        drop_cmd = f"drop foreign table if exists {self.tb_name};checkpoint;"
        drop_result = self.pri_sh.execut_db_sql(drop_cmd)
        self.log.info(drop_result)

        step9_txt = '----step9:清理编译脚本; expect:清理成功----'
        self.log.info(step9_txt)
        file_rm_cmd = f'rm -rf {self.target_path};' \
            f'if [ -d {self.target_path} ]; ' \
            f'then echo "exists"; else echo "not exists"; fi'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_root.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        step10_txt = '----step10:还原增量检查点开关; expect:修改成功----'
        self.log.info(step10_txt)
        msg = self.pri_sh.execute_gsguc('set',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'enable_incremental_checkpoint'
                                        f'={self.init_para}')

        step11_txt = '----step11:重启数据库生效; expect:重启成功----'
        self.log.info(step11_txt)
        restart = self.pri_sh.restart_db_cluster()

        step_txt = '----teardown断言----'
        self.log.info(step_txt)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, drop_result,
                      "执行失败" + step8_txt)
        self.assertIn(self.constant.CHECKPOINT_SUCCESS_MSG, drop_result,
                      "执行失败" + step8_txt)
        self.assertEqual('not exists', file_rm_result, "执行失败" + step9_txt)
        self.assertTrue(msg, '执行失败:' + step10_txt)
        self.assertTrue(restart, '执行失败:' + step11_txt)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

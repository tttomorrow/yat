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
Case Name   : 预编译sql为删除数据，执行预编译sql语句过程中修改表结构-修改字段类型
Description :
    1.创建配置文件
    2.编译java文件
    3.运行java预编译代码（删除预编译重复执行）
    4.步骤3过程中，进行表结构变更-修改字段类型与预编译sql相关
    5.步骤3过程中，进行表结构变更-修改字段类型与预编译sql无关
    6.验证步骤3结果
Expect      :
    1.创建配置文件成功
    2.编译java文件成功
    3.运行java预编译代码（删除预编译重复执行），开始执行
    4.步骤3过程中，进行表结构变更-修改字段类型与预编译sql相关，修改成功
    5.步骤3过程中，进行表结构变更-修改字段类型与预编译sql无关，修改成功
    6.验证步骤3结果，正常执行完成
History     :
"""
import os
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class JDBCPrepareStatement(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_root = Node(node='PrimaryRoot')
        self.log.info("----this is setup----")
        self.log.info(
            '----Opengauss_Function_JDBC_PrepareStatement_Case0009:start----')
        self.target_path = os.path.join(macro.DB_BACKUP_PATH, "JDBC_test")
        self.properties = os.path.join(self.target_path,
                                       "jdbc_preparestat_Case0009.properties")
        self.java_name = "jdbc_PrepareStatement_Case0006_10"
        self.tb_name = "tb_jdbc_PrepareStatement_Case0009"
        self.com = Common()
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')


    def test_main(self):
        step_txt = '----step1:创建配置文件; expect:创建成功----'
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

        step_txt = '----step2:编译java文件; expect:编译成功----'
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

        step_txt = '----step3:运行java预编译代码（删除预编译重复执行）; expect:开始运行----'
        self.log.info(step_txt)
        java_cmd = f"java -cp " \
            f"{os.path.join(self.target_path, 'postgresql.jar')}" \
            f":{self.target_path} " \
            f"{self.java_name} -F {self.properties}"
        self.log.info(java_cmd)
        java_thread = ComThread(self.com.get_sh_result,
                                args=(self.pri_root, java_cmd))
        java_thread.setDaemon(True)
        java_thread.start()
        time.sleep(10)

        step_txt = '----step4:步骤3过程中，进行表结构变更-修改字段类型与预编译sql相关; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f'alter table {self.tb_name} ' \
            f'alter COLUMN c_customer_sk type int;\d {self.tb_name}'
        result = self.pri_sh.execut_db_sql(alter_sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_TABLE_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step5:步骤3过程中，进行表结构变更-修改字段类型与预编译sql无关； expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f'alter table {self.tb_name} ' \
            f'modify c_customer_bak1 int;\d {self.tb_name}'
        result = self.pri_sh.execut_db_sql(alter_sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_TABLE_MSG, result,
                      "执行失败" + step_txt)

        step_txt = '----step6:验证步骤3结果; expect:正常执行完成----'
        self.log.info(step_txt)
        java_thread.join(180)
        java_result = java_thread.get_result()
        suc_flag = "delete succeed!999"
        self.assertIn(suc_flag, java_result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is tearDown----')
        self.log.info('----清理环境----')
        ps_cmd = f"ps ux |grep {self.java_name}|grep -v grep|" \
            f"tr -s ' '|cut -d ' ' -f 2"
        self.log.info(ps_cmd)
        ps_result = self.pri_root.sh(ps_cmd).result()
        self.log.info(ps_result)
        if ps_result != '':
            self.log.info('----清理java进程----')
            kill_cmd = f"ps ux |grep {self.java_name}|grep -v grep|" \
                f"tr -s ' '|cut -d ' ' -f 2|xargs kill -9"
            self.log.info(kill_cmd)
            self.pri_root.sh(kill_cmd)

        cmd = f"drop table if exists {self.tb_name};"
        result = self.pri_sh.execut_db_sql(cmd)
        self.log.info(result)
        cmd = f"rm -rf {self.target_path}"
        self.log.info(cmd)
        self.pri_root.sh(cmd)
        self.log.info(
            '----Opengauss_Function_JDBC_PrepareStatement_Case0009:end----')

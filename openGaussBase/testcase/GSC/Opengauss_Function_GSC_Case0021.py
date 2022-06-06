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
Case Type   : GSC功能模块
Case Name   : 非线程池模式场景下，jdbc并发执行表ddl与select，验证是否存在缓存数据不一致情况
Description :
    1、修改enable_global_syscache为on;enable_thread_pool为off;
    2、重启数据库，使参数生效;
    3、创建表;
    4、创建配置文件;
    5、编译java文件;
    6、运行java代码(并发进行ddl，dml);
    7、查询表;
Expect      :
    1、修改enable_global_syscache为on;enable_thread_pool为off; 成功
    2、重启数据库，使参数生效; 重启成功
    3、创建表; 创建成功
    4、创建配置文件; 创建成功
    5、编译java文件; 编译成功
    6、运行java代码(并发进行ddl，dml); 操作成功
    7、查询表;查询成功
History     :
"""
import os
import re
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class GscTestCase(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("----this is setup----")
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.pri_dbuser = Node(node='PrimaryDbUser')
        self.pri_root = Node(node='PrimaryRoot')
        self.sh = CommonSH('PrimaryDbUser')
        self.target_path = os.path.join(macro.DB_BACKUP_PATH, "JDBC_test")
        self.properties = os.path.join(self.target_path,
                                       "jdbc_GSC_Case0020.properties")
        self.java_name = "jdbc_gsc_case0021"
        self.tb_name = "tb_gsc0021"
        self.com = Common()
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')

    def test_main(self):
        step_txt = '----step0:查看enable_global_syscache初始配置值;----'
        self.log.info(step_txt)
        self.init_para1 = self.com.show_param('enable_global_syscache')
        step_txt = '----step0:查看enable_thread_pool初始值;----'
        self.log.info(step_txt)
        self.init_para2 = self.com.show_param('enable_thread_pool')

        step_txt = '----step1:修改enable_global_syscache为on;' \
                   'enable_thread_pool为off; expect:成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= on")
        self.assertTrue(msg, '执行失败:' + step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_thread_pool= off")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step2:重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result)
        self.log.info('----查询参数----')
        self.new_para1 = self.com.show_param('enable_global_syscache')
        self.assertEqual(self.new_para1, 'on', '执行失败:' + step_txt)
        self.new_para2 = self.com.show_param('enable_thread_pool')
        self.assertEqual(self.new_para2, 'off', '执行失败:' + step_txt)

        step_txt = '----step3:创建表; expect:创建成功----'
        self.log.info(step_txt)
        create_tb_sql = f"create table {self.tb_name} " \
            f"(c_integer integer,c_tinyint tinyint," \
            f"c_smallint smallint,c_binary_integer binary_integer," \
            f"c_bigint bigint,c_numeric numeric(10,4)," \
            f"c_number number(10,4),c_smallserial smallserial)"
        create_result = self.sh.execut_db_sql(create_tb_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_result,
                      '执行失败:' + step_txt)

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

        step_txt = '----step6:运行java代码(并发进行ddl，dml); expect:操作成功----'
        self.log.info(step_txt)
        java_cmd = f"java -cp " \
            f"{os.path.join(self.target_path, 'postgresql.jar')}" \
            f":{self.target_path} " \
            f"{self.java_name} -F {self.properties}"
        self.log.info(java_cmd)
        java_result = self.com.get_sh_result(self.pri_root, java_cmd)
        self.suc_flag1 = '增加字段.*查询成功'
        self.suc_flag2 = '删除字段.*查询失败'
        self.err_flag = '异常'
        self.assertEqual(len(re.findall(self.suc_flag1, java_result)), 50,
                         "执行失败" + step_txt)
        self.assertEqual(len(re.findall(self.suc_flag1, java_result)), 50,
                         "执行失败" + step_txt)
        self.assertNotIn(self.err_flag, java_result, "执行失败" + step_txt)

        step_txt = '----step7: 查询表; expect:查询成功----'
        self.log.info(step_txt)
        tb_sql = f"select * from {self.tb_name} "
        result = self.pri_sh.execut_db_sql(tb_sql)
        self.log.info(result)
        self.assertIn('0 rows', result, "执行失败" + step_txt)

    def tearDown(self):
        step_txt = '----this is teardown----'
        self.log.info(step_txt)
        step1_txt = '----清理表; expect:删除成功----'
        self.log.info(step1_txt)
        drop_tb_sql = f"drop table if exists {self.tb_name} ;"
        drop_tb_result = self.sh.execut_db_sql(drop_tb_sql)
        self.log.info(drop_tb_result)

        step2_txt = '----清理编译脚本; expect:清理成功----'
        self.log.info(step2_txt)
        file_rm_cmd = f'rm -rf {self.target_path};' \
            f'if [ -d {self.target_path} ]; ' \
            f'then echo "exists"; else echo "not exists"; fi'
        self.log.info(file_rm_cmd)
        file_rm_result = self.pri_root.sh(file_rm_cmd).result()
        self.log.info(file_rm_result)

        step3_txt = '----恢复参数为初始值并查询; expect:设置成功----'
        self.log.info(step3_txt)
        msg1 = self.sh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"enable_global_syscache="
                                     f"{self.init_para1}")
        msg2 = self.sh.execute_gsguc('reload',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"enable_thread_pool="
                                     f"{self.init_para2}")
        step4_txt = '----重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step4_txt)
        restart_result = self.sh.restart_db_cluster()
        step5_txt = '----查询数据库状态; expect:状态正常----'
        self.log.info(step5_txt)
        status_result = self.sh.get_db_cluster_status('status')

        self.log.info(f'----{os.path.basename(__file__)}:end----')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_tb_result,
                      '执行失败:' + step1_txt)
        self.assertEqual('not exists', file_rm_result, "执行失败" + step2_txt)
        self.assertTrue(msg1, '执行失败:' + step3_txt)
        self.assertTrue(msg2, '执行失败:' + step3_txt)
        self.assertTrue(restart_result, '执行失败:' + step4_txt)
        self.assertTrue(status_result, '执行失败:' + step5_txt)

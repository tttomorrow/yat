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
Case Name   : enable_global_syscache参数异常值设置验证
Description :
    1、guc修改enable_global_syscache为数字2
    2、guc修改enable_global_syscache为字符test
    3、guc修改enable_global_syscache为空
    4、alter system方式修改enable_global_syscache为数字2
    5、修改postgresql.conf文件参数为空，重启数据库
    6、修改postgresql.conf文件参数为非法值，重启数据库
Expect      :
    1、guc修改enable_global_syscache为数字2，修改失败
    2、guc修改enable_global_syscache为字符test，修改失败
    3、guc修改enable_global_syscache为空，修改失败
    4、alter system方式修改enable_global_syscache为数字2
    5、修改postgresql.conf文件参数为空，重启数据库，重启失败，报错相应行参数有问题
    6、修改postgresql.conf文件参数为非法值，重启数据库，重启失败，报错非法值
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class GscTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        self.pri_dbuser = Node(node='PrimaryDbUser')

    def test_main(self):
        step_txt = '----step0:查看config_file配置值;----'
        self.log.info(step_txt)
        self.conf_file = self.com.show_param("config_file")
        self.conf_file_bak = self.conf_file + '_gsc0007'

        step_txt = '----step0:查看enable_global_syscache初始配置值;----'
        self.log.info(step_txt)
        self.init_para = self.com.show_param("enable_global_syscache")

        step_txt = '----step1:guc修改enable_global_syscache为数字2; expect:失败----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= 2")
        self.assertFalse(msg, '执行失败:' + step_txt)

        step_txt = '----step2:guc修改enable_global_syscache为字符类型; expect:失败----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= test")
        self.assertFalse(msg, '执行失败:' + step_txt)

        step_txt = '----step3:guc修改enable_global_syscache为空; expect:失败----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= ")
        self.assertFalse(msg, '执行失败:' + step_txt)

        step_txt = '----step4:alter system方式修改enable_global_syscache为数字2; ' \
                   'expect:失败----'
        self.log.info(step_txt)
        alter_sql = 'alter system set enable_global_syscache to 2;'
        result = self.sh.execut_db_sql(alter_sql)
        self.log.info(result)
        err_flag = 'ERROR:  parameter "enable_global_syscache" requires a ' \
                   'Boolean value'
        self.assertIn(err_flag, result, '执行失败:' + step_txt)

        step_txt = '----step5:修改postgresql.conf文件参数为空，重启数据库; ' \
                   'expect:重启失败----'
        self.log.info(step_txt)
        shell_cmd = f"cp {self.conf_file} {self.conf_file_bak} &&" \
            f"sed -i '$a enable_global_syscache=' {self.conf_file}"
        self.log.info(shell_cmd)
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        shell_cmd = f"grep -n 'enable_global_syscache' {self.conf_file}"
        self.log.info(shell_cmd)
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        row_nu = shell_result.splitlines()[-1].split(':')[0].strip()
        step_txt = '----step5:修改参数为空，重启数据库; expect:重启失败----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster(get_detail=True)
        err_flag = f'syntax error in file "{self.conf_file}" line {row_nu}'
        self.assertIn(err_flag, restart_result, '执行失败:' + step_txt)

        step_txt = '----step6:修改postgresql.conf文件参数为非法值，重启数据库; ' \
                   'expect:重启失败----'
        self.log.info(step_txt)
        shell_cmd = f"cp {self.conf_file_bak} {self.conf_file} &&" \
            f"sed -i '$a enable_global_syscache=123' {self.conf_file}"
        self.log.info(shell_cmd)
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        shell_cmd = f"grep -n 'enable_global_syscache' {self.conf_file}"
        self.log.info(shell_cmd)
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        step_txt = '----step6:修改参数为非法值，重启数据库; expect:重启失败----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster(get_detail=True)
        err_flag = '"enable_global_syscache" requires a Boolean value'
        self.assertIn(err_flag, restart_result, '执行失败:' + step_txt)

    def tearDown(self):
        step_txt = '----this is teardown----'
        self.log.info(step_txt)
        step1_txt = '----还原postgresql.conf文件，重启数据库; ' \
                    'expect:重启成功----'
        self.log.info(step1_txt)
        shell_cmd = f"cp {self.conf_file_bak} {self.conf_file} &&" \
            f"rm -rf {self.conf_file_bak}"
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        shell_cmd = f"grep -n 'enable_global_syscache' {self.conf_file}"
        self.log.info(shell_cmd)
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        restart_result = self.sh.restart_db_cluster()
        step2_txt = '----查询数据库状态; expect:状态正常----'
        self.log.info(step2_txt)
        status_result = self.sh.get_db_cluster_status('status')
        step3_txt = '----查询参数; expect:参数为初始值----'
        self.log.info(step3_txt)
        self.new_para = self.com.show_param("enable_global_syscache")

        self.log.info(f'----{os.path.basename(__file__)}:end----')
        self.assertTrue(restart_result, '执行失败:' + step_txt + step1_txt)
        self.assertTrue(status_result, '执行失败:' + step_txt + step2_txt)
        self.assertEqual(self.new_para, self.init_para,
                         '执行失败:' + step_txt + step3_txt)

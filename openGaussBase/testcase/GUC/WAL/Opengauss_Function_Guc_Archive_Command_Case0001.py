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
Case Type   : guc参数
Case Name   : 归档命令仅包含一条shell语句
Description :
    1.修改配置文件将日志归档模式打开
    2.重启数据库使参数设置生效
    3.查看归档日志模式
    4.配置归档路径和参数,执行select pg_switch_xlog();触发归档
    5.查看是否生成归档日志
    6.恢复默认值,删除归档目录
Expect      :
    1.配置文件中archive_mode设置完成
    2.重启数据库成功
    3.查看归档日志模式
    4.配置归档路径及参数archive_command成功
    5.WAL日志正常归档
    6.恢复默认值,删除归档目录
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
class Guctestcase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            "----Opengauss_Function_Guc_Archive_Command_Case0001_开始----")
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.rootNode = Node('PrimaryRoot')
        self.userNode = Node('dbuser')
        self.constant = Constant()
        self.com = Common()
        self.archive_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'archive')
        self.conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                  'postgresql.conf')


    def test_guc(self):
        text = '-----step1:修改配置文件将日志归档模式打开;expect:成功打开-----'
        self.log.info(text)
        self.default_value1 = self.com.show_param("archive_mode")
        self.log.info(self.default_value1)
        self.default_value2 = self.com.show_param("archive_command")
        self.log.info(self.default_value2)
        guc_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc set -N all -I all -c "archive_mode = on";'
        self.log.info(guc_cmd)
        guc_msg = self.userNode.sh(guc_cmd).result()
        self.log.info(guc_msg)
        self.assertIn("Success to perform gs_guc", guc_msg, '执行成功' + text)

        text = '-----step2:重启数据库使配置参数生效;expect:数据库重启成功-----'
        self.log.info(text)
        result = self.pri_sh.restart_db_cluster()
        self.log.info(result)
        result = self.pri_sh.get_db_cluster_status('detail')
        self.log.info(result)
        self.assertTrue("Degraded" in result or "Normal" in result,
                        '执行失败:' + text)

        text = '----------step3:查看归档日志模式:expect:模式设置成功----------'
        self.log.info(text)
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc check  ' \
            f'-N all ' \
            f'-I all ' \
            f'-c "archive_mode"'
        self.log.info(check_cmd)
        check_msg = self.userNode.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertIn('archive_mode=on', check_msg, '执行成功' + text)

        text = '--------step4:配置归档路径和参数:expect:执行成功----------'
        self.log.info(text)
        self.log.info('---4.1.创建归档路径---')
        mkdir_cmd = f'''if [ ! -d "{self.archive_path}" ]
                        then
                            mkdir {self.archive_path}
                        fi'''
        self.log.info(mkdir_cmd)
        mkdir_result = self.userNode.sh(mkdir_cmd).result()
        self.log.info(mkdir_result)
        self.log.info('---4.2.配置参数并触发归档---')
        alter_cmd = f'''alter system set archive_command to \
            'cp --remove-destination %p {self.archive_path}/%f';
            show archive_command;
            select pg_switch_xlog();
            '''
        excute_msg = self.pri_sh.execut_db_sql(alter_cmd)
        self.log.info(excute_msg)
        self.assertIn('1 row', excute_msg, '执行成功' + text)

        text = '----step5:查看是否生成归档日志;expect:归档成功----'
        self.log.info(text)
        du_cmd = f'''du -h {self.archive_path};'''
        self.log.info(du_cmd)
        du_msg = self.userNode.sh(du_cmd).result()
        self.log.info(du_msg)
        dumsg_list = du_msg.split()[0]
        self.log.info(dumsg_list)
        self.assertTrue(float(dumsg_list[:-1]) > 0, '执行成功' + text)

    def tearDown(self):
        text = '----step6:恢复默认值;expect:恢复成功----'
        self.log.info(text)
        guc_msg1 = self.pri_sh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"archive_mode="
                                              f"off")
        self.log.info(guc_msg1)
        sed_cmd = f"sed -i 's/archive_command/#archive_command/g' " \
            f"{self.conf_path};"
        guc_msg2 = self.userNode.sh(sed_cmd).result()
        self.log.info(guc_msg2)
        self.log.info('-----重启集群并检查数据库状态-----')
        result = self.pri_sh.restart_db_cluster()
        self.log.info(result)
        result = self.pri_sh.get_db_cluster_status('detail')
        self.log.info(result)
        self.default_value3 = self.com.show_param("archive_mode")
        self.log.info(self.default_value3)
        self.default_value4 = self.com.show_param("archive_command")
        self.log.info(self.default_value4)
        clear_cmd = f'source {macro.DB_ENV_PATH};' \
            f'chmod -R 700 {self.archive_path};' \
            f'sudo rm -drf {self.archive_path};'
        self.log.info(clear_cmd)
        clear_msg = self.rootNode.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.assertEqual('', clear_msg, '执行失败:' + text)
        self.assertTrue("Degraded" in result or "Normal" in result,
                        '执行失败' + text)
        self.assertEqual(self.default_value3, self.default_value1,
                        '执行失败:' + text)
        self.assertEqual(self.default_value4, self.default_value2,
                        '执行失败:' + text)

        self.log.info(
            "----Opengauss_Function_Guc_Archive_Command_Case0001finsh----")

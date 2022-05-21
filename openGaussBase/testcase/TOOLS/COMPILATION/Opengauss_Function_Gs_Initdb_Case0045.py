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
Case Type   : 系统内部使用工具
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--pwfile，指定的文件第一行为空，登陆数据库后需要修改密码
Description :
    1.在指定路径下创建一个文件，命名为file.txt(自定义)，文件第一行为空
    2.执行命令：gs_initdb -D [初始化数据库目录] --nodename=single  --pwfile=[file文件的路径]
    3.设置初始化数据库端口为系统未使用端口
    可使用lsof -i:55810命令校验端口使用情况
              lsof -i:55810
    gs_guc set -D [初始化数据库目录] -c port=[系统未使用端口]
    4.启动数据库：gs_ctl start -D [初始化数据库目录]
    5.连接数据库，执行语句：gsql -d postgres -p [系统未使用端口] -c 'select user';
    6.清理环境
    停止数据库：gs_ctl stop -D [初始化数据库目录]
    删除初始化密码文件：rm -rf [file文件的路径];
    删除初始化数据库：rm -rf [初始化数据库目录];
Expect      :
    1.创建成功
    2.初始化成功，[初始化数据库目录]下生成数据库文件
    3.设置端口成功
    4.数据库启动成功
    5.提示修改密码，修改密码后，语句执行成功
    6.清理成功
History     :
"""
import os
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('----Opengauss_Function_Gs_Initdb_Case0045开始执行----')
        self.primary_root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH,
                                     'datadir_gs_initdb_0045')
        self.pwfile = os.path.join(macro.DB_INSTANCE_PATH,
                                   'gs_initdb_0045.txt')
        self.postgresql_init = os.path.join(self.dir_path,
                                            macro.DB_PG_CONFIG_NAME)

    def test_standby(self):
        text = '----删除初始化目录----'
        self.log.info(text)
        dir_cmd = f"rm -rf {self.dir_path};"
        exec_msg = self.primary_root_node.sh(dir_cmd).result()
        self.log.info(exec_msg)

        step_txt = '----step1:创建文件，文件第一行为空 expect:创建成功----'
        self.log.info(step_txt)
        mod_msg = f"echo -e '\\n' > {self.pwfile}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        self.assertEqual(msg, '', '执行失败:' + step_txt)

        step_txt = '----step2:执行gs_initdb命令 expect:初始化成功，' \
                   '[初始化数据库目录]下生成数据库文件----'
        self.log.info(step_txt)
        initdb_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_initdb -D {self.dir_path} --nodename=single' \
            f' --pwfile={self.pwfile};' \
            f'ls {self.dir_path}'
        self.log.info(initdb_cmd1)
        initdb_res = self.primary_node.sh(initdb_cmd1).result()
        self.log.info(initdb_res)
        self.assertIn(self.constant.initdb_success_msg, initdb_res,
                      '执行失败:' + step_txt)
        self.assertTrue(
            macro.DB_PG_CONFIG_NAME in initdb_res and macro.PG_HBA_FILE_NAME
            in initdb_res, '执行失败:' + step_txt)

        text = "--step3:设置初始化数据库端口为系统未使用端口 expect:设置成功"
        self.log.info(text)
        port = self.com.get_not_used_port(self.primary_node)
        self.assertNotEqual(0, port, '执行失败:' + text)
        updata_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc set -D {self.dir_path} -c port={port};'
        self.log.info(updata_cmd)
        updata_result = self.primary_node.sh(updata_cmd).result()
        self.log.info(updata_result)
        self.assertIn('Success to perform gs_guc', updata_result,
                      '执行失败:' + text)

        step_txt = '----step4:启动数据库 expect:数据库启动成功----'
        self.log.info(step_txt)
        gaussdb_msg = f"source {macro.DB_ENV_PATH};" \
            f"gs_ctl start -D {self.dir_path}"
        self.log.info(gaussdb_msg)
        msg = self.primary_node.sh(gaussdb_msg).result()
        self.log.info(msg)
        self.assertIn(self.constant.REBUILD_SUCCESS_MSG, msg,
                      '执行失败:' + step_txt)

        step_txt = '----step5:连接数据库，执行语句 expect:提示修改密码，修改密码后，语句执行成功----'
        self.log.info(step_txt)
        updata_pw_cmd = f"alter role {self.primary_node.ssh_user} " \
            f"password '{macro.COMMON_PASSWD}';"
        gsql_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d postgres -p {port} -c "select user";' \
            f'gsql -d postgres -p {port} -c "{updata_pw_cmd}";' \
            f'gsql -d postgres -p {port} -c "select user";'
        self.log.info(gsql_cmd1)
        gsql_res = self.primary_node.sh(gsql_cmd1).result()
        self.log.info(gsql_res)
        self.assertIn(self.constant.gsql_error_msg, gsql_res,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, gsql_res,
                      '执行失败:' + step_txt)
        self.assertIn('1 row', gsql_res, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----step6:清理环境----')
        text_1 = '----停止数据库 expect:成功----'
        self.log.info(text_1)
        stop_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_ctl stop -D {self.dir_path}"
        self.log.info(stop_cmd)
        stop_result = self.primary_node.sh(stop_cmd).result()
        self.log.info(stop_result)

        text_2 = '----删除初始化密码文件和数据库目录 expect:成功----'
        self.log.info(text_2)
        del_msg = self.primary_root_node.sh(f'rm -rf {self.dir_path};'
                                            f'rm -f {self.pwfile}').result()
        self.log.info(del_msg)

        self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, stop_result,
                      '执行失败:' + text_1)
        self.assertEqual('', del_msg, '执行失败:' + text_2)
        self.log.info(
            '----Opengauss_Function_Gs_Initdb_Case0045执行完成----')

"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : 只导入已列举的函数（-P, --function=NAME单独使用）
Description :
    1.创建数据
    2.导出数据
    3.导入之前导出的数据
    4.清理环境
Expect      :
    1.创建数据
    2.导出数据
    3.导入之前导出的数据成功
    4.清理环境
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Log = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Log.info("--Opengauss_Function_Tools_gs_restore_Case0038开始执行--")
        self.constant = Constant()
        self.dbuser_node = Node('dbuser')
        self.root_user = Node('default')

    def test_server_tools1(self):
        Log.info("----------------------创建函数-----------------------")
        sql_cmd = f'''create function func1(i integer)
            returns integer
            as \$$
            begin
                    return i+1;
            end;
            \$$ language plpgsql;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, msg)

        sql_cmd = f'''create function func2(i integer)
            returns integer
            as \$$
            begin
                    return i+1;
            end;
            \$$ language plpgsql;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, msg)
        sql_cmd = f'''create function func3(i integer)
            returns integer
            as \$$
            begin
                    return i+1;
            end;
            \$$ language plpgsql;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, msg)

        Log.info("----------------导出tar格式文件-----------------")
        mkdir_cmd = f"mkdir /home/{self.primary_dbuser.dbuser}/test_restore/ ;"
        Log.info(mkdir_cmd)
        msg = self.root_user.sh(mkdir_cmd).result()
        Log.info(msg)
        dump_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_dump -p {self.dbuser_node.db_port} " \
            f"{self.dbuser_node.db_name} -f " \
            f"/home/test_restore/test2.tar -F t "
        Log.info(dump_cmd)
        msg = self.dbuser_node.sh(dump_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.GS_DUMP_SUCCESS_MSG, msg)

        Log.info("--------------导入之前导出的数据----------------")
        restore_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_restore  -p {self.dbuser_node.db_port} " \
            f"-d {self.dbuser_node.db_name} /home/test_restore/test2.tar " \
            f"-P 'func2(integer)' -c"
        Log.info(restore_cmd)
        msg = self.dbuser_node.sh(restore_cmd).result()
        Log.info(msg)
        self.assertIn(self.constant.RESTORE_SUCCESS_MSG, msg)

    def tearDown(self):
        Log.info("--------------------清理环境---------------------")
        sql_cmd = f'''drop function if exists func1;
            drop function if exists func2;
            drop function if exists func3;
            '''
        excute_cmd = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        Log.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        Log.info(msg)
        rm_cmd = f"rm -rf /home/test_restore"
        Log.info(rm_cmd)
        msg = self.root_user.sh(rm_cmd).result()
        Log.info(msg)
        Log.info("---Opengauss_Function_Tools_gs_restore_Case0038执行结束---")

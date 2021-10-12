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
Case Type   : 系统操作
Case Name   : 修改时区为UTC，分别省略session参数和添加session参数
Description :
        1.设置时区是UTC;查询时区值并查询当前时间
        2.恢复默认时区PRC；查询时区值并查询当前时间
        3.添加sessio参数，设置时区是UTC
        4.清理环境
Expect      :
        1.设置成功，当前北京时间的UTC时区时间（北京时间-8h）
        2.恢复为PRC；当前时区为+08
        3.设置成功
        4.清理环境完成
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0002开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_set(self):
        # 设置时区是UTC;查询时区值并查询当前时间，当前北京时间的UTC时区时间（北京时间-8h）
        sql_cmd1 = commonsh.execut_db_sql('''set time zone UTC;
                                      show timezone;
                                      select now();''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('UTC', sql_cmd1)
        self.assertIn('+00', sql_cmd1)
        # 恢复默认时区PRC;查询时区值并查询当前时间
        sql_cmd2 = commonsh.execut_db_sql('''reset time zone;
                                       show timezone;
                                       select now();''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.RESET_SUCCESS_MSG, sql_cmd2)
        self.assertIn('PRC', sql_cmd2)
        self.assertIn('+08', sql_cmd2)
        # 添加sessio参数，设置时区是UTC
        sql_cmd3 = commonsh.execut_db_sql('''set session time zone UTC;
                                      select now();''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.SET_SUCCESS_MSG, sql_cmd3)
        self.assertIn('+00', sql_cmd3)
        # 退出数据库重新连接,恢复默认时区值PRC
        sql_cmd3 = commonsh.execut_db_sql('''\\q''')
        logger.info(sql_cmd3)
        sql_cmd3 = ('''show timezone;''')
        excute_cmd1 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port}  -c "{sql_cmd3}"
                                  '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('PRC', msg1)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DML_Set_Case0002执行结束--------------------------')

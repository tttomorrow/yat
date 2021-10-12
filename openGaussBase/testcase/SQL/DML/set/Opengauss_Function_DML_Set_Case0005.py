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
Case Name   : 事务中，添加参数session设置时区后再提交事务，最后结束会话
Description :
        1.开启事务
        2.设置时区UTC
        3.查看当前北京时间的UTC时区时间
        4.提交事务
        5.回滚
        6.查询当前时间
        7.退出数据库重新连接
Expect      :
        1.事务开启成功
        2.设置成功
        3.显示时区+00
        4.提交事务成功
        5.回滚成功
        6.显示时区+00
        7.恢复默认时区值PRC
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
        logger.info('------------------------Opengauss_Function_DML_Set_Case0005开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_set(self):
        # 开启事务
        # 设置时区是UTC
        # 查看设置是否生效
        # 查看当前北京时间的UTC时区时间
        # 提交事务
        # 回滚
        # 查询当前时间
        sql_cmd1 = commonsh.execut_db_sql('''start transaction;
                                      set session time zone UTC;
                                      show time zone;
                                      select now();
                                      commit;
                                      rollback;
                                      select now();''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd1)
        self.assertIn(self.Constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('UTC', sql_cmd1)
        self.assertIn('+00', sql_cmd1)
        self.assertIn(self.Constant.COMMIT_SUCCESS_MSG, sql_cmd1)
        self.assertIn('NOTICE:  there is no transaction in progress', sql_cmd1)
        self.assertIn('+00', sql_cmd1)
        # 退出数据库重新连接,恢复默认时区值PRC
        sql_cmd2 = commonsh.execut_db_sql('''\\q''')
        logger.info(sql_cmd2)
        sql_cmd2 = ('''show timezone;''')
        excute_cmd1 = f'''
                         source {self.DB_ENV_PATH};
                         gsql -d {self.userNode.db_name} -p {self.userNode.db_port}  -c "{sql_cmd2}"'''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('PRC', msg1)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DML_Set_Case0005执行结束--------------------------')

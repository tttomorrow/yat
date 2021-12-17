"""
Case Type   : 序列
Case Name   : 主机创建序列，备机执行调用nextval函数，合理报错
Description :
        1.主机创建序列
        2.备机执行nextval函数
        3.删除序列
Expect      :
        1.创建序列成功
        2.合理报错，备机不支持执行该函数
        3.删除成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro
from yat.test import Node

logger = Logger()
Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class Sequence(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_DDL_Create_Sequence_Case0014开始执行----')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.constant = Constant()
        self.expect_res = 'ERROR:  Standby do not support nextval, ' \
                          'please do it in primary!'

    def test_create_sequence(self):
        logger.info('---步骤1:主机创建序列----')
        sql_cmd = '''drop sequence if exists serial_7;
            create sequence serial_7 increment by 2 maxvalue 5 cycle;
            '''
        excute_cmd = f'''source {self.DB_ENV_PATH} ;
        gsql -d {self.primary_node.db_name}\
            -p {self.primary_node.db_port}\
            -c "{sql_cmd}"
            '''
        logger.info(excute_cmd)
        msg = self.primary_node.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.constant.CREATE_SEQUENCE_SUCCESS_MSG, msg)
        logger.info('--步骤2:备机执行nextval函数，合理报错--')
        sql_cmd = '''select nextval('serial_7');'''
        excute_cmd = f'''source {self.DB_ENV_PATH} ;
            gsql -d {self.standby_node.db_name} \
            -p {self.standby_node.db_port}\
            -c "{sql_cmd}"
            '''
        logger.info(excute_cmd)
        msg = self.standby_node.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.expect_res, msg)

    def tearDown(self):
        logger.info('---步骤3:删除序列----')
        sql_cmd = '''drop sequence serial_7;'''
        excute_cmd = f'''source {self.DB_ENV_PATH} ;
            gsql -d {self.primary_node.db_name}\
            -p {self.primary_node.db_port} \
            -c "{sql_cmd}"
            '''
        logger.info(excute_cmd)
        msg = self.primary_node.sh(excute_cmd).result()
        logger.info(msg)
        logger.info(
            '-----Opengauss_Function_DDL_Create_Sequence_Case0014执行完成---')

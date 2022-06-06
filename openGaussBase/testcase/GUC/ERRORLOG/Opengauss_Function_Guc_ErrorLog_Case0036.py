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
Case Type   : GUC_ErrorLog
Case Name   : 设置参数log_rotation_size值为0，关闭基于容量的新日志文件的创建
Description :
    1.设置参数log_rotation_size值为0
    2.清空log_directory，重启数据库使$path下生成日志文件：
    3.构造日志信息文件大于20M，重启数据库，查看日志文件
Expect      :
    1.设置成功
    2.重启数据库成功，生成日志文件
    3.未生成新的日志文件，在原日志文件中追加新的日志信息
History     :
"""
import os
import re
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

from utils.Constant import Constant


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0036 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.primaryRoot = Node(node='PrimaryRoot')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'wftest')
        self.path_return = self.common.show_param('log_directory')
        self.statement = self.common.show_param('log_statement')
        self.rotation = self.common.show_param('log_rotation_size')
        self.table = 'tb_guc_errorlog_0036'
    
    def test_errorlog(self):
        text = '------修改log_directory路径------'
        self.logger.info(text)
        result = self.sh_primy.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'log_directory=\'{self.log_path}\'')
        self.logger.info(result)
        self.assertEqual(True, result, '执行失败' + text)

        text = '------修改log_statement的值------'
        self.logger.info(text)
        result = self.sh_primy.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'log_statement=mod')
        self.logger.info(result)
        self.assertEqual(True, result, '执行失败' + text)

        text = '------step1:设置参数log_rotation_size的值为0;expect:成功------'
        self.logger.info(text)
        result = self.sh_primy.execute_gsguc('reload',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f'log_rotation_size=0')
        self.logger.info(result)
        self.assertEqual(True, result, '执行失败' + text)
        
        text = '--step2:清空log_directory，重启数据库使$path下生成日志文件;' \
               'expect:成功--'
        self.logger.info(text)
        excute_cmd2 = f'rm -rf {self.log_path}/*;' \
            f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t stop && gs_om -t start'
        excute_msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(excute_msg2)
        excute_cmd3 = f'ls {self.log_path}'
        excute_msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(excute_msg3)
        assert1 = re.search(r"postgresql.*log", excute_msg3, re.S)
        self.assertTrue(assert1, '执行失败:' + text)
        
        self.logger.info('--step3:构造文件大小大于20MB,查看是否生成新的日志文件:'
                         'expect:成功--')
        excute_cmd4 = f'dd if=/dev/zero of={self.log_path}/{excute_msg3} ' \
            f'bs=1M count=30;'
        self.logger.info(excute_cmd4)
        excute_msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(excute_msg4)
        sql_cmd5 = f'drop table if exists {self.table};' \
            f'create table {self.table}(id int, name char(5));' \
            f'insert into {self.table} values(5, \'qsadc\');' \
            f'drop table {self.table};'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        self.logger.info(msg5)
        assert2 = re.search(r".*CREATE TABLE.*INSERT 0 1.*DROP TABLE",
                            msg5, re.S)
        self.assertTrue(assert2, '执行失败:' + text)
        text = '-------查看生成了新的日志文件-------'
        self.logger.info(text)
        excute_cmd6 = f'ls {self.log_path}'
        excute_msg6 = self.primaryRoot.sh(excute_cmd6).result()
        self.logger.info(excute_msg6)
        assert3 = re.search(r"postgresql.*log", excute_msg6, re.S)
        self.assertTrue(assert3, '执行失败:' + text)
    
    def tearDown(self):
        text1 = '--------1.恢复配置，清理环境--------'
        self.logger.info(text1)
        result1 = self.sh_primy.execute_gsguc('reload',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f'log_directory=\'{self.path_return}\'')
        self.logger.info(result1)
        result2 = self.sh_primy.execute_gsguc('reload',
                                      self.constant.GSGUC_SUCCESS_MSG,
                                      f'log_statement={self.statement}')
        self.logger.info(result2)
        result3 = self.sh_primy.execute_gsguc('reload',
                                      self.constant.GSGUC_SUCCESS_MSG,
                                      f'log_rotation_size={self.rotation}')
        self.logger.info(result3)
        text2 = '--------2.清理生成的日志文件--------'
        self.logger.info(text2)
        excute_cmd = f'rm -rf {self.log_path};'
        self.logger.info(excute_cmd)
        result4 = self.userNode.sh(excute_cmd).result()
        self.assertEqual(True, result1, '执行失败' + text1)
        self.assertEqual(True, result2, '执行失败' + text1)
        self.assertEqual(True, result3, '执行失败' + text1)
        self.assertEqual('', result4, '执行失败' + text1)
        self.logger.info('--Opengauss_Function_Guc_ErrorLog_Case0036 finish--')

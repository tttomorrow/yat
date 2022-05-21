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
Case Type   : 全文检索
Case Name   : ALTER TEXT SEARCH CONFIGURATION，用户权限测试（普通用户）,合理报错
Description :
        1.创建文本搜索配置
        2.创建词典
        3.创建用户
        4.普通用户增加文本搜索配置字串类型映射
        5.清理环境
Expect      :
        1.创建文本搜索配置成功
        2.创建词典成功
        3.创建用户
        4.合理报错
        5.清理环境完成
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class FullTextSearch(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Text_Search_Configuration_Case0036开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('dbuser')
        self.Constant = Constant()

    def test_common_user_permission(self):
        # 创建文本搜索配置
        sql_cmd1 = commonsh.execut_db_sql('''drop TEXT SEARCH CONFIGURATION if exists ngram2;
                                   CREATE TEXT SEARCH CONFIGURATION ngram2 (parser=ngram) WITH (gram_size = 2, grapsymbol_ignore = false);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_TEXT_SEARCH_CONFIGURATION, sql_cmd1)
        # 创建词典
        sql_cmd2 = commonsh.execut_db_sql('''DROP TEXT SEARCH DICTIONARY IF EXISTS pg_dict;
                                          CREATE TEXT SEARCH DICTIONARY pg_dict (TEMPLATE = Simple);''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant. CREATE_DICTIONARY_SUCCESS_MSG,sql_cmd2 )
        # 创建用户
        sql_cmd3 = commonsh.execut_db_sql(f'''drop user if exists pt cascade;
                                    create user pt password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd3)

        # 普通用户增加文本搜索配置字串类型映射,合理报错
        sql_cmd4 = '''ALTER TEXT SEARCH CONFIGURATION ngram2  ADD MAPPING FOR grapsymbol with pg_dict;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  pt -W '{macro.COMMON_PASSWD}' -c "{sql_cmd4}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  must be owner of text search configuration ngram2', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除文本搜索配置
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH CONFIGURATION ngram2 cascade;''')
        logger.info(SqlMdg)
        # 删除词典
        SqlMdg = commonsh.execut_db_sql('''DROP TEXT SEARCH DICTIONARY pg_dict cascade;''')
        logger.info(SqlMdg)
        # 删除用户
        SqlMdg = commonsh.execut_db_sql('''drop user pt cascade;''')
        logger.info(SqlMdg)
        logger.info('------------------------Opengauss_Function_Text_Search_Configuration_Case0036执行结束--------------------------')






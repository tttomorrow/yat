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
Case Name   : 删除词典，权限测试（普通用户）
Description :
    1.创建词典
    2.创建用户
    3.切换用户至test_pt，执行删除词典
    4.删除词典
    5.删除用户
Expect      :
    1.创建词典c成功
    2.用户创建成功
    3.合理报错
    4.删除词典成功
    5.删除用户成功
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
        logger.info("------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0050开始执行--------------------------")
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_dictionary(self):
        file_path = macro.DB_DictFile
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY if exists thesaurus_astro cascade;
        CREATE TEXT SEARCH DICTIONARY thesaurus_astro (
        TEMPLATE = thesaurus,
        DictFile = thesaurus_sample,
        Dictionary = pg_catalog.english_stem);''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_DICTIONARY_SUCCESS_MSG, SqlMdg)
        SqlMdg = commonsh.execut_db_sql(f'''drop user if exists test_pt cascade;
       create user test_pt password '{macro.COMMON_PASSWD}';''')
        logger.info(SqlMdg)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, SqlMdg)
        sql_cmd2 = '''drop TEXT SEARCH DICTIONARY thesaurus_astro cascade;'''
        excute_cmd1 = f'''
                                source {self.DB_ENV_PATH};
                                gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_pt -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                                '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  must be owner of text search dictionary thesaurus_astro', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        SqlMdg = commonsh.execut_db_sql('''drop TEXT SEARCH DICTIONARY thesaurus_astro cascade;
                                        drop user test_pt cascade;''')
        logger.info(SqlMdg)
        logger.info('------------------------Opengauss_BaseFunc_Full_Text_Search_dictionary_0050执行结束--------------------------')

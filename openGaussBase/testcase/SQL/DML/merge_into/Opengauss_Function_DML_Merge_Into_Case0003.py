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
Case Type   : merge_into 权限测试
Case Name   : revoke用户目标表的update和insert权限，执行merge_into操作
Description :
    1.创建用户
    2.建表并插入数据
    3.revoke用户u_mergeinto_03对目标表的update和insert权限
    4.u_mergeinto_03用户对表执行merge into操作
    5.清理环境
Expect      :
    1.建表成功且数据插入成功
    2.用户创建成功
    3.权限revoke成功
    4.merge into操作失败，合理报错
    5.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class MergeInto(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.userNode = Node('PrimaryDbUser')
        self.logger.info('Opengauss_Function_DML_Merge_Into_Case0003'
                         '开始执行')
        self.constant = Constant()
        self.commonsh = CommonSH('PrimaryDbUser')
        self.tb_name1 = 't_mergeinto_03_01'
        self.tb_name2 = 't_mergeinto_03_02'
        self.user = 'u_mergeinto_03'

    def test_mergeinto_permission(self):
        text1 = '--step1:创建用户;expect:成功--'
        self.logger.info(text1)
        sql_cmd1 = self.commonsh.execut_db_sql(f'''
        drop user if exists {self.user} cascade;
        create user {self.user} password '{macro.COMMON_PASSWD}'; ''')
        self.logger.info(sql_cmd1)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG,
                      sql_cmd1, '执行失败:' + text1)

        text2 = '--step2:创建测试表并对测试表插入数据;expect:成功--'
        self.logger.info(text2)
        sql_cmd2 = self.commonsh.execut_db_sql(f'''
        drop table if exists  {self.tb_name1};
        drop table if exists  {self.tb_name2};
        create table {self.tb_name1}(product_id integer,
                    product_name varchar2(60),category varchar2(60));
        insert into {self.tb_name1} values (1501, 'vivitar 35mm', 
                                                        'electrncs');
        insert into {self.tb_name1} values (1502, 'olympus is50', 
                                                        'electrncs');
        insert into {self.tb_name1} values (1600, 'play gym',  'toys');
        insert into {self.tb_name1} values (1601, 'lamaze', 'toys');
        insert into {self.tb_name1} values (1666, 'harry potter', 
                                                            'dvd');
        create table {self.tb_name2}(product_id integer,
                    product_name varchar2(60),category varchar2(60));
        insert into {self.tb_name2} values (1502, 'olympus camera',
                                                        'electrncs');
        insert into {self.tb_name2} values (1601, 'lamaze','toys');
        insert into {self.tb_name2} values (1666, 'harry potter', 
                                                            'toys');
        insert into {self.tb_name2} values (1700, 'wait interface',
                                                            'books');                                                                                      
        ''', sql_type=f' -U {self.user} -W {macro.COMMON_PASSWD}')
        self.logger.info(sql_cmd2)
        self.assertTrue(
            sql_cmd2.count('CREATE TABLE') == 2, '执行失败:' + text2)
        self.assertTrue(sql_cmd2.count('INSERT') == 9, '执行失败:' + text2)

        text3 = '--step3:revoke用户对目标表的update和insert权限;expect:成功--'
        self.logger.info(text3)
        sql_cmd3 = self.commonsh.execut_db_sql(f'''
        revoke update,insert on {self.tb_name1} from {self.user};
        ''', sql_type=f' -U {self.user} -W {macro.COMMON_PASSWD}')
        self.logger.info(sql_cmd3)
        self.assertIn(self.constant.REVOKE_SUCCESS_MSG, sql_cmd3,
                      '执行失败:' + text3)

        text4 = '--step4:进行merge into操作;expect:失败--'
        self.logger.info(text4)
        sql_cmd4 = f'''merge into {self.tb_name1} t1 
        using {self.tb_name2} t2 on (t1.product_id = t2.product_id)
        when matched then
        update set t1.product_name = t2.product_name, 
        t1.category = t2.category where t1.product_name != 'play gym'
        when not matched then
        insert values (t2.product_id, t2.product_name, t2.category)
        where t2.category = 'books';'''
        sql_cmd5 = self.commonsh.execut_db_sql(sql_cmd4,
                        sql_type=f'-U {self.user} -W {macro.COMMON_PASSWD}')
        self.logger.info(sql_cmd5)
        self.assertIn('ERROR:  permission denied for relation ' \
                      't_mergeinto_03_01', sql_cmd5, '执行失败:' + text4)

    def tearDown(self):
        text5 = '--step5:清理环境;expect:成功-------'
        self.logger.info(text5)
        sql_cmd6 = self.commonsh.execut_db_sql(f'''
        drop table {self.tb_name1};
        drop table {self.tb_name2};
         ''', sql_type=f' -U {self.user} -W {macro.COMMON_PASSWD}')
        self.logger.info(sql_cmd6)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_cmd6,
                      '执行失败:' + text5)
        sql_cmd7 = self.commonsh.execut_db_sql(f'\
        drop user if exists {self.user} cascade;')
        self.logger.info(sql_cmd7)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd7,
                      '执行失败:' + text5)
        self.logger.info('Opengauss_Function_DML_Merge_Into_Case0003'
                         '执行结束')

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
Case Type   : Do
Case Name   : 执行匿名代码块，指定解析代码的程序语言为plpgsql
Description :
    1、创建表，并查看指定语言是否支持内联块
    2、指定解析代码的程序语言为plpgsql，利用do执行代码块
    3、查看数据
    4、清理环境;
Expect      :
    1、创建表成功，查看指定语言支持成功；
    2、执行成功；
    3、查看数据成功；
    4、清理环境成功；
History     :
"""

import unittest
import sys
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class DCL_Do_test(unittest.TestCase):

    def setUp(self):
        self.sh_primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()

    def test_dcl_do(self):
        logger.info("-----Opengauss_Function_DCL_Do_Case0001开始执行-----")
        logger.info("======前置条件，创建表，并查看指定语言是否支持内联块======")
        sql_cmd1 = f'''
                    drop table if exists do_test;
                    create table do_test(id int,name varchar(10));
                    --为0代表不支持
                    select laninline from pg_language where lanname='plpgsql';
                    '''
        msg1 = self.sh_primysh.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, msg1)
        self.assertNotEqual('0', msg1.splitlines()[-2])

        logger.info("======指定解析代码的程序语言为plpgsql，利用do执行代码块======")
        sql_cmd2 = f'''
                    do language plpgsql
                    \$\$
                    declare
                    sql_str varchar(100);
                    new_do_test do_test%rowtype;
                    begin
                        for i in 0..5 loop
                            insert into do_test values(i,'case' || i);
                        end loop;
                        sql_str = 'select * into new_do_test 
                        from do_test where id<3;';
                        execute immediate sql_str;
                    end
                    \$\$;
                    '''
        msg2 = self.sh_primysh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG, msg2)

        logger.info("======查看数据，代码块是否执行成功======")
        sql_cmd3 = f'''
                    --查看数据
                    select * from do_test;
                    select * from new_do_test;
                   '''
        msg3 = self.sh_primysh.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.assertIn('case0', msg3)

    def tearDown(self):
        logger.info('======清理环境======')
        sql_cmd4 = f'''
                    drop table do_test;
                    drop table new_do_test;
                   '''
        msg4 = self.sh_primysh.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        logger.info('-----Opengauss_Function_DCL_Do_Case0001执行结束-----')
        self.assertTrue(msg4.count(self.constant.DROP_TABLE_SUCCESS) == 2,
                        '清理环境失败')

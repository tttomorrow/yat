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
Case Type   : 列存表支持主键、唯一索引
Case Name   : 开启delta表功能，指定阈值为1000，插入小于1000数据量，删除索引后，再次插入大于1000数据
Description :
    1、开启列存delta表功能，重启数据库;
       gs_guc set -N all -D {dn1} -c "enable_delta_store = on"
    2、创建列存表，指定deltarow_threshold阈值为1000;
    3、创建唯一索引;
    4、插入小于1000数据，数据唯一且非空值;
    5、删除唯一索引，再次插入已存在数据;
    6、清理环境;
Expect      :
    1、设置参数成功，重启数据库成功;
    2、创建列存表、指定阈值为10000成功;
    3、创建唯一索引成功;
    4、插入数据成功;
    5、删除索引成功，插入数据成功;
    6、清理环境成功;
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.comsh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.table_name = 't_unique_index_column_0067'
        self.index_name = 'i_unique_index_column_0067'
        self.log.info('------SetUp:检查数据库状态是否正常------')
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_column_unique_index(self):
        self.log.info('---Opengauss_Function_DDL_Column_Unique_Index_Case0067'
                      '执行执行---')
        text = '------step1:检查参数，修改配置，并重启数据库; expect:成功------'
        self.log.info(text)
        self.config_item = 'enable_delta_store=on'
        check_res = self.comsh.execut_db_sql(f'''show enable_delta_store;''')
        if 'on' != check_res.splitlines()[-2].strip():
            self.comsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     self.config_item)
            self.comsh.restart_db_cluster()
            result = self.comsh.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result,
                            '执行失败' + text)

        self.log.info('------查看参数修改是否成功------')
        alter_res = self.comsh.execut_db_sql(f'''show enable_delta_store;''')
        self.log.info(alter_res)
        self.assertTrue('on' in alter_res.splitlines()[-2].strip())

        text = '----step2 & step3:创建列存表，指定deltarow_threshold阈值为1000,创建唯一索引;' \
               'expect:step2 & step3 执行成功----'
        self.log.info(text)
        sql_cmd1 = f'''drop table if exists {self.table_name};
            create table {self.table_name}(id int) 
            with(orientation=column,deltarow_threshold=1000);
            create unique index {self.index_name} 
            on {self.table_name} using btree(id);
            '''
        self.log.info(sql_cmd1)
        sql_res1 = self.comsh.execut_db_sql(sql_cmd1)
        self.log.info(sql_res1)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in sql_res1
                        and self.constant.CREATE_INDEX_SUCCESS in sql_res1,
                        '执行失败' + text)

        text = '------step4:插入小于1000数据,数据唯一且非空; expect:成功------'
        self.log.info(text)
        sql_cmd2 = f'''insert into {self.table_name} 
            values(generate_series(1,999));'''
        self.log.info(sql_cmd2)
        sql_res2 = self.comsh.execut_db_sql(sql_cmd2)
        self.log.info(sql_res2)
        self.assertTrue(self.constant.INSERT_SUCCESS_MSG in sql_res2,
                        '执行失败' + text)

        text = '------step5:删除唯一索引,插入已存在数据; expect:插入数据成功------'
        self.log.info(text)
        sql_cmd3 = f'''drop index {self.index_name};
            insert into {self.table_name} values(generate_series(1,999));'''
        self.log.info(sql_cmd3)
        sql_res3 = self.comsh.execut_db_sql(sql_cmd3)
        self.log.info(sql_res3)
        self.assertTrue(self.constant.DROP_INDEX_SUCCESS_MSG in sql_res3
                        and self.constant.INSERT_SUCCESS_MSG in sql_res3,
                        '执行失败' + text)

    def tearDown(self):
        self.log.info('------step6:清理环境; expect:成功------')
        drop_cmd = f'''drop table {self.table_name} cascade;'''
        self.log.info(drop_cmd)
        drop_res = self.comsh.execut_db_sql(drop_cmd)
        self.log.info(drop_res)

        self.config_item = 'enable_delta_store=off'
        recov_res = self.comsh.execut_db_sql(f'''show enable_delta_store;''')
        if 'off' != recov_res.splitlines()[-2].strip():
            self.comsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     self.config_item)
            self.comsh.restart_db_cluster()
            result = self.comsh.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)
        self.log.info('---Opengauss_Function_DDL_Column_Unique_Index_Case0067'
                      '执行结束---')

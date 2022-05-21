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
Case Type   : merge_into
Case Name   : 目标表为ustore表，进行merge into操作
Description :
    1.修改 enable_default_ustore_table=on
    2.创建目标表和源表并插入数据
    3.进行merge into操作
    4.查询更新后的结果
    5.清理环境
Expect      :
    1.修改成功
    2.创建表成功
    3.merge into成功
    4.查询成功
    5.清理环境成功
History     :
"""

import unittest
import os
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common


class MergeInto(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f"-----{os.path.basename(__file__)} start-----")
        self.commonsh = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        status = self.commonsh.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.default_value = self.common.show_param(
            'enable_default_ustore_table')
        self.tb_name1 = 't_dml_mergeinto_18_01'
        self.tb_name2 = 't_dml_mergeinto_18_02'

    def test_mergeinto_ustore(self):
        text = '--step1:修改 enable_default_ustore_table=on;expect:成功--'
        self.log.info(text)
        if "on" not in self.default_value:
            res = self.commonsh.execute_gsguc(
                "set", self.constant.GSGUC_SUCCESS_MSG,
                f"enable_default_ustore_table=on")
            self.log.info(res)
            status = self.commonsh.restart_db_cluster()
            self.log.info(status)
            res = self.commonsh.execut_db_sql(
                f"show enable_default_ustore_table;")
            self.log.info(res)
            self.assertEqual("on", res.splitlines()[-2].strip(), "执行失败" + text)

        text = '--step2:创建测试表并对测试表插入数据;expect:成功--'
        self.log.info(text)
        sql_cmd = f'''
        drop table if exists {self.tb_name1};
        drop table if exists {self.tb_name2};
        create table {self.tb_name1}(id integer, name varchar(60), 
        hobbies varchar(60));
        create table {self.tb_name2}(id integer, name varchar(60), 
        hobbies varchar(60));
        insert into {self.tb_name1} values(0,'a','a0'),(1,'a','a1'),
        (2,'key','a2');
        insert into {self.tb_name2} values(1,'b','b1'),(2,'b','b2'),
        (3,'b','key');
        '''
        res = self.commonsh.execut_db_sql(sql_cmd)
        self.log.info(res)
        self.assertEqual(res.count(self.constant.TABLE_DROP_SUCCESS), 2,
                         "执行失败：" + text)
        self.assertEqual(res.count(self.constant.TABLE_CREATE_SUCCESS), 2,
                         "执行失败：" + text)
        self.assertEqual(res.count(self.constant.INSERT_SUCCESS_MSG), 2,
                      "执行失败：" + text)

        text = '--step3:进行merge into操作;expect:成功--'
        self.log.info(text)
        sql_cmd = f'''merge into {self.tb_name1} tb1 using {self.tb_name2} tb2 
        on (tb1.id = tb2.id)
        when matched then
        update set tb1.name = tb2.name, tb1.hobbies=tb2.hobbies 
        where tb1.name !='key'
        when not matched then
        insert values (tb2.id, tb2.name, tb2.hobbies) 
        where tb2.hobbies='key';'''
        res = self.commonsh.execut_db_sql(sql_cmd)
        self.log.info(res)
        self.assertEqual('MERGE 2', res, "执行失败:" + text)

        text = '--step4:查询更新后的结果 ;expect: 成功--'
        self.log.info(text)
        res = self.commonsh.execut_db_sql(
            f'select * from {self.tb_name1} order by id;')
        self.log.info(res)
        self.assertEqual('4 rows',
                         res.splitlines()[-1].replace("(", "").replace(")", "")
                         , "执行失败" + text)

    def tearDown(self):
        text = '--step5:清理环境;expect:成功-------'
        self.log.info(text)
        drop_res = self.commonsh.execut_db_sql(f'''
        drop table if exists {self.tb_name1};
        drop table if exists {self.tb_name2};
        ''')
        self.log.info(drop_res)
        restores_default_value = self.commonsh.execute_gsguc(
            "set", self.constant.GSGUC_SUCCESS_MSG,
             f"enable_default_ustore_table={self.default_value}")
        self.log.info(restores_default_value)
        self.commonsh.restart_db_cluster()
        self.assertEqual(drop_res.count(self.constant.TABLE_DROP_SUCCESS), 2,
                         "执行失败：" + text)
        self.assertTrue(restores_default_value, "执行失败:" + text)
        self.log.info(f"-----{os.path.basename(__file__)} end-----")


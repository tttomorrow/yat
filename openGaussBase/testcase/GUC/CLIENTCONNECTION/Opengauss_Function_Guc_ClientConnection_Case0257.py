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
Case Type   : GUC
Case Name   : 修改参数gin_fuzzy_search_limit,观察预期结果
Description :
        1.查询gin_fuzzy_search_limit默认值
        2.修改参数值为123
        3.创建表并建gin索引
        4.查询表的查询计划
        5.清理环境
Expect      :
        1.显示默认值为0
        2.修改成功
        3.创建成功
        4.查询计划走索引扫描
        5.清理环境成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_ClientConnection_Case0257start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = "t_guc_0309"
        self.id_name = "i_guc_0309"

    def test_gin_fuzzy_search_limit(self):
        text = '---step1:查询默认值;expect:默认值0---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show gin_fuzzy_search_limit;')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()

        text = '--step2:修改参数值为123;expect:修改成功--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"gin_fuzzy_search_limit=123")
        self.assertTrue(result,  '执行失败:' + text)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        text = '---step3:创建表并建gin索引;expect:创建成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists 
            {self.tb_name};
            create table {self.tb_name}(id int, first_name text, 
            last_name text);
            insert into {self.tb_name} select id, md5(random()::text), 
            md5(random()::text) from (select * from generate_series(1,5000) 
            as id) as x;
            insert into {self.tb_name} values(2, 'America is a rock band, 
            formed in England ', 'America');
            drop index if exists {self.id_name};
            create index {self.id_name}  on {self.tb_name} using 
            gin(to_tsvector('english', first_name));''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        text = '---step4:查询计划;expect:走索引扫描---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''explain select * from 
            {self.tb_name} where to_tsvector('english', first_name) 
            @@ to_tsquery('english', 'formed');''')
        self.log.info(sql_cmd)
        self.assertIn('Bitmap Index Scan', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '---step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists 
            {self.tb_name};''')
        self.log.info(sql_cmd)
        sql_cmd = self.pri_sh.execut_db_sql('show gin_fuzzy_search_limit;')
        self.log.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[2].strip():
            msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'gin_fuzzy_search_limit'
                                            f'={self.res}')
            self.log.info(msg)
            msg = self.pri_sh.restart_db_cluster()
            self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0309finish-')

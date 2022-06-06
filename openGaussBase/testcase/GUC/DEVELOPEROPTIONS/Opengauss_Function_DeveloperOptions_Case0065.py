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
Case Name   : 使用gs_guc set方法设置参数analysis_options为on(HASH_CONFLICT),
             观察预期结果
Description :
        1.查询analysis_options默认值
        2.修改参数值为on(LLVM_COMPILE)并重启数据库
        3.建表且插入数据
        4.使用explain语句查询
        5.删表并恢复参数默认值
Expect      :
        1.显示默认值为ALL,on(),
        off(LLVM_COMPILE,HASH_CONFLICT,STREAM_DATA_CHECK)，
         不开启任何定位功能
        2.设置成功,显示
        ALL,on(HASH_CONFLICT),off(LLVM_COMPILE,STREAM_DATA_CHECK)
        3.建表且插入数据成功
        4.查询成功
        5.删表且恢复默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class DeveloperOptions(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '-----Opengauss_Function_DeveloperOptions_Case0065start----')
        self.constant = Constant()

    def test_analysis_options(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show analysis_options;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:修改参数值并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "analysis_options = 'on(HASH_CONFLICT)'")
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查询修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('show analysis_options;')
        LOG.info(sql_cmd)
        self.assertIn('ALL,on(HASH_CONFLICT),'
                      'off(LLVM_COMPILE,STREAM_DATA_CHECK)', sql_cmd)
        LOG.info('--步骤4:建表并插入数据--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_065;
            create table test_065(id int, name text);
            insert into test_065 values(1,'a'),(2,'b'),(3,'c');
            drop table if exists test_065_bak;
            create table test_065_bak(id int, dep_name text);
            insert into test_065_bak values(1,'a'),(5,'b'),(6,'c'); 
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd)
        LOG.info('--步骤5:使用explain 语句查询表--')
        sql_cmd = commonsh.execut_db_sql('''explain select * from test_065 
            where  not exists 
            (select * from test_065_bak where test_065.id=test_065_bak.id);
            ;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.EXPLAIN_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:清理环境--')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_065;
            drop table if exists test_065_bak;
            ''')
        LOG.info(sql_cmd)
        sql_cmd = commonsh.execut_db_sql('show analysis_options;')
        LOG.info(sql_cmd)
        if 'off(ALL)' != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"analysis_options='off(ALL)'")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show analysis_options;')
        LOG.info(sql_cmd)
        LOG.info(
            '------Opengauss_Function_DeveloperOptions_Case0065finish-----')

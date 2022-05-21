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
Case Type   : 数据库系统
Case Name   : 列存表创建psort索引
Description :
    1.创建表
    2.创建索引
    3.插入数据
    4.查询索引类型
    5.解析查询
    6.创建表达式索引
    7.创建本地临时表
    8.创建部分索引
Expect      :
    1.创建表成功
    2.创建索引成功
    3.插入数据成功
    4.索引类型为psort
    5.使用索引
    6.创建索引失败
    7.创建成功
    8.创建失败
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class RecoveryDelay(unittest.TestCase):
    commshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("---Opengauss_Function_DDL_Index_Case0245 start--")
        self.constant = Constant()
        self.tb_name = 'tb_col'
        self.tb_name_tmp = 'tb_col_tmp'
        self.idx = 'tb_idx'

    def test_index(self):

        self.log.info('--------1.创建表-------')
        sql = f"drop table if exists {self.tb_name};" \
            f"create table {self.tb_name}(id int,name varchar) " \
            f"WITH (ORIENTATION = column);"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)

        self.log.info('--------2.创建索引-------')
        sql = f"create index {self.idx} on tb_col(id);"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, result)

        self.log.info('--------3.插入数据------')
        sql = f"insert into {self.tb_name} " \
            f"values(generate_series(1,200),'ttt');"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('INSERT', result)

        self.log.info('--------4.查询索引类型------')
        sql = f"\d+ {self.tb_name}"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('psort', result)

        self.log.info('--------5.解析查询------')
        sql = f"SET ENABLE_SEQSCAN=off;" \
            f"explain select * from {self.tb_name} where id>198;"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.idx, result)

        self.log.info('--------6.创建表达式索引------')
        sql = f'create index exp_idx on {self.tb_name} ' \
            f'using psort(upper(name));'
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('not support index expressions', result)

        self.log.info('--------7.创建本地临时表8.创建部分索引------')
        sql = f'create temp table {self.tb_name_tmp}(id int,name varchar) ' \
            f'WITH (ORIENTATION = column);' \
            f'create index part_idx on {self.tb_name_tmp} ' \
            f'using psort(id) where id>300;'
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)
        self.assertNotIn(self.constant.CREATE_INDEX_SUCCESS_MSG, result)

        self.log.info('--------9.创建本地临时表10.创建表达式索引------')
        sql = f'create temp table {self.tb_name_tmp}(id int,name varchar) ' \
            f'WITH (ORIENTATION = column);' \
            f'create index part_idx on {self.tb_name_tmp} ' \
            f'using psort(upper(name));'
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, result)
        self.assertIn('not support index expressions', result)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')

        self.log.info('--------删除表-------')
        sql = f"drop table if exists {self.tb_name} cascade;" \
            f"drop table if exists {self.tb_name_tmp} cascade;"
        result = self.commshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info("---Opengauss_Function_DDL_Index_Case0245 end--")
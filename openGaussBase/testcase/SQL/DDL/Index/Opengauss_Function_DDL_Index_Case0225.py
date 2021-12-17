'''
Case Type： 功能
Case Name：使用concurrently创建部分索引，部分索引范围为同时插入数据
Descption:
1.创建表，并插入数据
3.创建部分在线索引
4.创建索引的同时对表插入数据
5.使用索引查询
6.查询插入数据
'''
import unittest
from yat.test import Node
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.ComThread import ComThread


class Concurrently(unittest.TestCase):
    primary_sh = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.dbPrimaryDbUser = Node(node='PrimaryDbUser')
        self.log = Logger()
        self.Constant = Constant()
        self.tblname = 'ddl_index_case0225'
        self.idxname = 'ddl_index_case0225_idx'
        self.log.info('----------------------Opengauss_Function_ddl_index_case0225.py start---------------------------')

    def test_in_select(self):
        self.log.info('-------------------create table--------------------------------')
        result = self.primary_sh.execut_db_sql(f'DROP TABLE IF EXISTS {self.tblname};CREATE TABLE {self.tblname}(id INT);')
        self.log.info(result)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, result)
        self.log.info('-------------------insert data--------------------------------')
        result = self.primary_sh.execut_db_sql(f'INSERT INTO {self.tblname} SELECT * FROM  generate_series(1,8000000) ;')
        self.log.info(result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, result)

        self.log.info('-----------------create index-----------------------------')
        sql = f'select current_time;create index concurrently {self.idxname} on {self.tblname}(id) where id > 200000000;select current_time;'
        create_index_thread = ComThread(self.primary_sh.execut_db_sql, args=(sql, ''))
        create_index_thread.setDaemon(True)
        create_index_thread.start()

        self.log.info('-----------------insert table-----------------------------')
        before_time = self.dbPrimaryDbUser.sh("date +'%s'").result()
        result = self.primary_sh.execut_db_sql(f'INSERT INTO {self.tblname} SELECT * FROM  generate_series(200000000,200000999) ;')
        after_time = self.dbPrimaryDbUser.sh("date +'%s'").result()
        self.log.info(result)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, result)
        # 计算执行时间
        total_time = int(after_time) - int(before_time)
        self.log.info(f'before_time is : {before_time}')
        self.log.info(f'after_time is : {after_time}')

        self.log.info('-----------------check create index result-----------------------------')
        create_index_thread.join(10 * 60)
        create_idx_result = create_index_thread.get_result()
        self.log.info(create_idx_result)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, create_idx_result)
        before_create_time = create_idx_result.splitlines()[2].strip()
        after_create_time = create_idx_result.splitlines()[-2].strip()
        self.log.info(f'before_create_time is {before_create_time}')
        self.log.info(f'after_create_time is {after_create_time}')
        create_time_H = before_create_time.split(':')[0]
        create_time_M = before_create_time.split(':')[1]
        create_time_S = before_create_time.split(':')[2].split('.')[0]
        create_time_H1 = after_create_time.split(':')[0]
        create_time_M1 = after_create_time.split(':')[1]
        create_time_S1 = after_create_time.split(':')[2].split('.')[0]
        create_index_time = int(create_time_H1) * 60 * 60 + int(create_time_M1) * 60 + int(create_time_S1) - int(
            create_time_H) * 60 * 60 - int(create_time_M) * 60 - int(create_time_S)
        self.log.info(f'create_index_time is {create_index_time}')
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS, create_idx_result)
        # 若阻塞查询时间必然比创建索引时间大
        self.assertTrue(create_index_time - total_time)

        self.log.info('-----------------show idx-----------------------------')
        result = self.primary_sh.execut_db_sql(
            f'SET ENABLE_SEQSCAN=off;explain SELECT * FROM {self.tblname} where id = 7000000;')
        self.log.info(result)
        self.assertNotIn(self.idxname, result)
        result = self.primary_sh.execut_db_sql(
            f'SET ENABLE_SEQSCAN=off;explain SELECT * FROM {self.tblname} where id = 200000999;')
        self.log.info(result)
        self.assertIn(self.idxname, result)

        self.log.info('-----------------check insert date-----------------------------')
        result = self.primary_sh.execut_db_sql(
            f'SET ENABLE_SEQSCAN=off;SELECT count(*) FROM {self.tblname} where id>200000000;')
        self.log.info(result)
        self.assertIn('999', result)

    def tearDown(self):
        self.log.info('----------------this is tearDown------------------------------------')
        self.log.info('----------------drop table------------------------------------')
        result = self.primary_sh.execut_db_sql(f'drop table if exists {self.tblname};')
        self.log.info(result)

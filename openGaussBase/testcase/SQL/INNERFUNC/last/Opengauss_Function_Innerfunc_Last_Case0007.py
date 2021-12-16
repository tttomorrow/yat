"""
Case Type   : 服务端工具
Case Name   : last函数返回最后一个输入，若无输入，则返回一个空行：mot表
Description :
    1.创建外表
    2.表中未插入数据，使用last函数，返回一个空行
    3.给表中插入数据
    4.与group by，order by，having  结合使用
    5.输入包含null，并排序(nulls last)
    6.与函数嵌套使用
    7.清理环境
Expect      :
    1.创建外表成功
    2.表中未插入数据，使用last函数，返回一个空行
    3.给表中插入数据成功
    4.与group by，order by，having  结合使用，返回结果正确
    5.输入包含null，并排序(nulls last)，返回结果正确
    6.与函数嵌套使用，返回结果正确
    7.清理环境成功
History     :
"""

import unittest
import sys


from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Jsonb(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.primysh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.log.info('----------检查参数，修改配置，并重启数据库----------')
        self.config_item = 'enable_incremental_checkpoint=off'
        check_res = self.primysh.execut_db_sql(
            f'''show enable_incremental_checkpoint;''')
        if 'off' != check_res.split('\n')[-2].strip():
            self.primysh.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG, self.config_item)
            self.primysh.restart_db_cluster()
            result = self.primysh.get_db_cluster_status()
            self.assertTrue('Degraded' in result or 'Normal' in result)

    def test_mot_table_last(self):
        self.log.info('---Opengauss_Function_Innerfunc_Last_Case0007开始执行---')
        self.log.info('-------------1.创建mot表--------------')
        self.sql_cmd = f'''drop foreign table if exists student;
            drop foreign table if exists score;
            create foreign table student(
            s_id integer(20),
            s_name varchar(20) ,
            s_birth date,s_sex varchar(10));
            create foreign table score(
            s_id integer(20),
            c_id  integer(20),
            s_score float(3));            
            '''
        self.log.info(self.sql_cmd)
        msg1 = self.primysh.execut_db_sql(self.sql_cmd)
        self.log.info(msg1)
        self.assertIn(self.constant.CREATE_FOREIGN_SUCCESS_MSG, msg1)

        self.log.info('----2.未插入数据时，使用last函数，返回一个空行----')
        self.sql_cmd = f'''select last(s_name) from student;
            select last(s_name), last(s_id) from student;
            select last(s_score) from score;
            select last(c_id), last(s_score) from score;        
            '''
        self.log.info(self.sql_cmd)
        msg2 = self.primysh.execut_db_sql(self.sql_cmd)
        self.log.info(msg2)
        self.assertIn('1 row', msg2)

        self.log.info('----3.给表中插入数据----')
        self.sql_cmd = f'''insert into student values (1,'zhaolei',null,'男');
            insert into student values (2,'zhoumei','1991-12-01','女');
            insert into student values (3,'zhuzhu','1991-06-01','男');
            insert into student values (4,'lilei','1992-05-01','男');
            insert into student values (null,'lihua','1991-03-01','男');
            insert into student values (1,'zhangsan','1992-08-01','男');
            insert into student values (2,'sunjin','1991-09-01','女');
            insert into student values (3,'wangwu','1992-10-01','女');
            insert into student values (4,null,'1990-11-01','女');
            insert into student values (5,'ninghao','1993-12-01','女');
            insert into score values(1, 101, 69.5),(1, 101, 80);
            insert into score values(2, 102, 70),(2, 102, 82);
            insert into score values(3, 103, 71),(3, 103, 93);
            insert into score values(4, 104, 85),(4, 104, 85);
            insert into score values(5, 105, 73),(5, 105, 91);
            insert into score values(1, 106, null);
            insert into score values(2, 107, 75);
            insert into score values(3, null, 78);
            insert into score values(4, 109, 86);
            insert into score values(null, 110, 99);      
            '''
        self.log.info(self.sql_cmd)
        msg3 = self.primysh.execut_db_sql(self.sql_cmd)
        self.log.info(msg3)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg3)

        self.log.info('----4.与group by，order by，having  结合使用----')
        self.sql_cmd = f'''select  last(s_name order by s_id) from student;
            select s_name, last(s_id) as id from student 
            group by s_name order by s_name;
            select s_id, last(s_name) from student group by s_id 
            having s_id > 2 order by s_id;
            select sc.s_id,last(sc.s_score) from score as sc ,
            student as st where st.s_sex = '女' 
            group by sc.s_id order by sc.s_id;
            select sc.s_id,last(st.s_name) from score as sc 
            inner join student as st on sc.s_id = st.s_id
            where st.s_sex = '女'group by sc.s_id order by sc.s_id;       
            '''
        self.log.info(self.sql_cmd)
        msg4 = self.primysh.execut_db_sql(self.sql_cmd)
        self.log.info(msg4)
        self.assertIn('lihua', msg4)
        self.assertIn('10 rows', msg4)
        self.assertIn('3 rows', msg4)
        self.assertIn('6 rows', msg4)
        self.assertIn('4 rows', msg4)

        self.log.info('----5.使用nulls last排序----')
        self.sql_cmd = f'''
            select last(s_name order by s_id nulls last) from student;
            select s_name, last(s_birth order by s_birth  nulls last) 
            from student group by s_name order by s_name;  
            select s_id, last(s_score order by s_score desc  NULLS last) 
            from score group by s_id;
            select c_id, last(s_score order by s_score desc  NULLS last) 
            from score group by c_id having c_id > 102 order by c_id;
            select st.s_id,last(s_score order by s_score NULLS last) 
            from score as sc inner join student as st on sc.s_id = st.s_id
            where st.s_sex = '女' group by st.s_id order by st.s_id;
            '''
        self.log.info(self.sql_cmd)
        msg5 = self.primysh.execut_db_sql(self.sql_cmd)
        self.log.info(msg5)
        self.assertIn('lihua', msg5)
        self.assertIn('10 rows', msg5)
        self.assertIn('6 rows', msg5)
        self.assertIn('7 rows', msg5)
        self.assertIn('4 rows', msg5)

        self.log.info('----6.与函数嵌套使用----')
        self.sql_cmd = f'''
            select char_length(last(s_name order by s_name)) from student;
            select isfinite(last(s_birth order by s_birth)) from student;
            select ceil(last(s_score order by s_score)) from score;      
            '''
        self.log.info(self.sql_cmd)
        msg6 = self.primysh.execut_db_sql(self.sql_cmd)
        self.log.info(msg6)
        self.assertIn('6', msg6)
        self.assertIn('t', msg6)
        self.assertIn('99', msg6)

    def tearDown(self):
        self.log.info('----------7.清理环境，删除创建的mot表----------')
        self.sql_cmd = f'''drop foreign table student cascade;
            drop foreign table score cascade;
            '''
        msg7 = self.primysh.execut_db_sql(self.sql_cmd)
        self.log.info(msg7)
        self.log.info('--Opengauss_Function_Innerfunc_Last_Case0007执行结束--')

-- @testpoint: interval分区,SELECT WHERE与比较操作符等联用

drop table if exists test9;

create table test9(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month')
(
	partition test9_p1 values less than ('2020-01-01')
)enable row movement;

-- 插入数据
insert into test9 values (1,'aaa',1,'2019-12-31',true,'aaa',1.1);  
insert into test9 values (2,'bbb',2,'2020-01-01',false,'bbb',2.2); 
insert into test9 values (3,'ccc',3,'2020-01-31',true,'ccc',3.3);  
insert into test9 values (4,'ddd',4,'2020-02-01',false,'ddd',4.4); 
insert into test9 values (5,'eee',5,'2020-02-29',true,'eee',5.5);  
insert into test9 values (6,'ddd',6,'2020-03-01',false,'ddd',4.4); 
insert into test9 values (7,'eee',7,'2020-03-31',true,'eee',5.5);  
insert into test9 values (8,'ddd',8,'2020-04-01',false,'ddd',4.4); 
insert into test9 values (9,'eee',9,'2020-04-30',true,'eee',5.5);  

-- 查看分区表信息
select relname, parttype, partstrategy, boundaries, reltablespace, intervaltablespace, interval, transit
from pg_partition where parentid = (select oid from pg_class where relname = 'test9') order by relname;

-- select where
select * from test9 partition(test9_p1) where col_4 < timestamp'2020-01-01';  
select * from test9 partition(sys_p1) where col_4 < timestamp'2020-03-01';    
select * from test9 where col_4 < timestamp'2020-03-01';    
select * from test9 partition(sys_p1) where col_4 > timestamp'2020-03-01';    
select * from test9 where col_4 > timestamp'2020-03-01';    
select * from test9 partition(sys_p4) where col_4 > timestamp'2020-03-01';    
select * from test9 partition(sys_p4) where col_4 = timestamp'2020-04-01';    
select * from test9 partition(sys_p4) where col_4 = timestamp'2020-03-01';    

-- 查看各分区中数据
select * from test9 partition (test9_p1)order by col_4;
select * from test9 partition (sys_p1)order by col_4;
select * from test9 partition (sys_p2)order by col_4;
select * from test9 partition (sys_p3)order by col_4;
select * from test9 partition (sys_p4)order by col_4;

drop table if exists test9;
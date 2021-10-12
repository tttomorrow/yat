-- @testpoint: interval分区,删除分区数据

drop table if exists test8;

create table test8(
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
	partition test8_p1 values less than ('2020-02-29')
);

-- 插入数据
insert into test8 values (1,'aaa',1,'2019-02-28',true,'aaa',1.1);
insert into test8 values (2,'bbb',2,'2020-02-28',false,'bbb',2.2);
insert into test8 values (3,'ccc',3,'2020-02-29',true,'ccc',3.3);
insert into test8 values (4,'ddd',4,'2021-02-28',false,'ddd',4.4);
insert into test8 values (5,'eee',5,'2022-02-28',true,'eee',5.5);
insert into test8 values (6,'fff',6,'2023-02-28',false,'fff',6.6);
insert into test8 values (7,'fff',7,'2024-02-29',false,'fff',6.6);

-- 查看分区表信息
select relname, parttype, partstrategy, boundaries, reltablespace, intervaltablespace, interval, transit
from pg_partition where parentid = (select oid from pg_class where relname = 'test8') order by relname;

-- 删除数据
delete from test8 where col_4 < timestamp'2021-12-01';

-- 查看各分区中数据
select * from test8 partition (test8_p1)order by col_4;
select * from test8 partition (sys_p1)order by col_4;
select * from test8 partition (sys_p2)order by col_4;
select * from test8 partition (sys_p3)order by col_4;
select * from test8 partition (sys_p4)order by col_4;
select * from test8 partition (sys_p5)order by col_4;

-- 查看分区表信息
select relname, parttype, partstrategy, boundaries, reltablespace, intervaltablespace, interval, transit
from pg_partition where parentid = (select oid from pg_class where relname = 'test8') order by relname;

drop table if exists test8;
-- @testpoint: interval分区,DISABLE ROW MOVEMENT,更新数据落在其他分区时合理报错
drop table if exists table1;

create table table1(
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
	partition table1_p1 values less than ('2020-01-01')
)disable row movement;

insert into table1 values (1,'aaa',1,'2019-12-31',true,'aaa',1.1);
insert into table1 values (2,'bbb',2,'2020-01-01',false,'bbb',2.2);
insert into table1 values (3,'ccc',3,'2020-02-01',true,'ccc',3.3);
insert into table1 values (4,'ddd',4,'2020-03-01',false,'ddd',4.4);
insert into table1 values (5,'eee',5,'2020-04-01',true,'eee',5.5);

select relname, parttype, partstrategy, boundaries, reltablespace, intervaltablespace, interval, transit
from pg_partition where parentid = (select oid from pg_class where relname = 'table1') order by relname;

select * from table1 partition (table1_p1)order by col_4;
select * from table1 partition (sys_p1)order by col_4;
select * from table1 partition (sys_p2)order by col_4;
select * from table1 partition (sys_p3)order by col_4;
select * from table1 partition (sys_p4)order by col_4;

--更新数据落在其他分区,更新失败
update table1 set col_4='2020-05-01' where col_4='2020-01-01';

select * from table1 partition (table1_p1)order by col_4;
select * from table1 partition (sys_p1)order by col_4;
select * from table1 partition (sys_p2)order by col_4;
select * from table1 partition (sys_p3)order by col_4;
select * from table1 partition (sys_p4)order by col_4;
select * from table1 partition (sys_p5)order by col_4;

drop table if exists table1;
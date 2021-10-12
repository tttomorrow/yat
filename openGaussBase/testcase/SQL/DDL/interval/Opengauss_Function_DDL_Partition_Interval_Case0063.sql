-- @testpoint: interval分区,INSERT数据,间隔为1hour,对边界值进行测试
drop table if exists table1;

create table table1(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 timestamp without time zone not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 hour')
(
	partition table1_p1 values less than ('2020-01-01 00:59:59')
);

insert into table1 values (1,'aaa',1,'2019-12-31 23:59:59',true,'aaa',1.1);
insert into table1 values (2,'bbb',2,'2020-01-01 00:00:00',false,'bbb',2.2);
insert into table1 values (6,'fff',6,'2020-01-05 00:00:00',false,'fff',6.6);
insert into table1 values (3,'ccc',3,'2020-01-01 01:00:00',true,'ccc',3.3);
insert into table1 values (4,'ddd',4,'2020-01-01 01:59:58',false,'ddd',4.4);
insert into table1 values (4,'ddd',4,'2020-01-01 01:59:59',false,'ddd',4.4);
insert into table1 values (4,'ddd',4,'2020-01-01 02:00:00',false,'ddd',4.4);

select relname, parttype, partstrategy, boundaries,reltablespace,intervaltablespace,interval,transit
from pg_partition where parentid = (select oid from pg_class where relname = 'table1') order by relname;

select * from table1 partition (table1_p1)order by col_4;
select * from table1 partition (sys_p1)order by col_4;
select * from table1 partition (sys_p2)order by col_4;
select * from table1 partition (sys_p3)order by col_4;

update table1 set col_4='2020-01-01 00:59:59' where col_1=6;
update table1 set col_4='2020-01-01 01:00:00' where col_1=3;
update table1 set col_4='2020-01-01 01:59:59' where col_1=4;

select relname, parttype, partstrategy, boundaries,reltablespace,intervaltablespace,interval,transit
from pg_partition where parentid = (select oid from pg_class where relname = 'table1') order by relname;
	
select * from table1 partition (table1_p1)order by col_4;
select * from table1 partition (sys_p1)order by col_4;
select * from table1 partition (sys_p2)order by col_4;
select * from table1 partition (sys_p3)order by col_4;

drop table if exists table1;
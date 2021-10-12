-- @testpoint: interval分区,INSERT数据,间隔为4 months,对边界值进行测试
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
interval ('4 months') 
(
	partition table1_p1 values less than ('2020-01-01')
);
	
insert into table1 values (1,'aaa',1,'2019-12-31',true,'aaa',1.1);
insert into table1 values (6,'fff',6,'2024-01-01',false,'fff',6.6);
insert into table1 values (2,'bbb',2,'2020-01-01',false,'bbb',2.2);
insert into table1 values (7,'fff',7,'2023-12-31',false,'fff',6.6);
insert into table1 values (3,'ccc',3,'2020-12-31',true,'ccc',3.3);
insert into table1 values (4,'ddd',4,'2021-01-01',false,'ddd',4.4);
insert into table1 values (8,'eee',8,'2026-01-01',true,'eee',5.5);
insert into table1 values (9,'eee',9,'2027-02-01',true,'eee',5.5);
insert into table1 values (10,'eee',10,'2028-03-01',true,'eee',5.5);
insert into table1 values (11,'eee',11,'2029-04-01',true,'eee',5.5);
insert into table1 values (12,'eee',12,'2030-05-01',true,'eee',5.5);

select relname, parttype, partstrategy, boundaries, reltablespace, intervaltablespace, interval, transit
from pg_partition where parentid = (select oid from pg_class where relname = 'table1') order by relname;
	
select * from table1 partition (table1_p1)order by col_4;
select * from table1 partition (sys_p1)order by col_4;
select * from table1 partition (sys_p2)order by col_4;
select * from table1 partition (sys_p3)order by col_4;
select * from table1 partition (sys_p4)order by col_4;
select * from table1 partition (sys_p5)order by col_4;
select * from table1 partition (sys_p6)order by col_4;
select * from table1 partition (sys_p7)order by col_4;
select * from table1 partition (sys_p8)order by col_4;
select * from table1 partition (sys_p9)order by col_4;
select * from table1 partition (sys_p10)order by col_4;

update table1 set col_4='2020-04-30' where col_1=8;
update table1 set col_4='2020-05-01' where col_1=9;
update table1 set col_4='2020-08-31' where col_1=10;
update table1 set col_4='2020-09-01' where col_1=11;

select relname, parttype, partstrategy, boundaries, reltablespace, intervaltablespace, interval, transit
from pg_partition where parentid = (select oid from pg_class where relname = 'table1') order by relname;
	
select * from table1 partition (table1_p1)order by col_4;
select * from table1 partition (sys_p1)order by col_4;
select * from table1 partition (sys_p2)order by col_4;
select * from table1 partition (sys_p3)order by col_4;
select * from table1 partition (sys_p4)order by col_4;
select * from table1 partition (sys_p5)order by col_4;
select * from table1 partition (sys_p6)order by col_4;
select * from table1 partition (sys_p7)order by col_4;
select * from table1 partition (sys_p8)order by col_4;
select * from table1 partition (sys_p9)order by col_4;
select * from table1 partition (sys_p10)order by col_4;
select * from table1 partition (sys_p11)order by col_4;

drop table if exists table1;
-- @testpoint: interval分区,ALTER TABLE TRUNCATE PARTITION清理表分区的数据
drop table if exists xhy_test;

create table xhy_test( 
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
	partition xhy_test_p1 values less than ('2020-02-29')
);
	
-- 插入数据
insert into xhy_test values (1,'aaa',1,'2019-02-28',true,'aaa',1.1);
insert into xhy_test values (2,'bbb',2,'2020-02-28',false,'bbb',2.2);
insert into xhy_test values (3,'ccc',3,'2020-02-29',true,'ccc',3.3);
insert into xhy_test values (4,'ddd',4,'2021-02-28',false,'ddd',4.4);
insert into xhy_test values (5,'eee',5,'2022-02-28',true,'eee',5.5);
insert into xhy_test values (6,'fff',6,'2023-02-28',false,'fff',6.6);
insert into xhy_test values (7,'fff',7,'2024-02-29',false,'fff',6.6);

-- @查看分区表信息
select relname, parttype, partstrategy, boundaries, reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'xhy_test') order by relname;
	
-- 查看各分区中数据
select * from xhy_test partition (xhy_test_p1)order by col_4;
select * from xhy_test partition (sys_p1)order by col_4;
select * from xhy_test partition (sys_p2)order by col_4;
select * from xhy_test partition (sys_p3)order by col_4;
select * from xhy_test partition (sys_p4)order by col_4;
select * from xhy_test partition (sys_p5)order by col_4;

-- truncate partition
alter table xhy_test truncate partition xhy_test_p1;
alter table xhy_test truncate partition sys_p2;
alter table xhy_test truncate partition sys_p5;
-- 查看各分区中数据
select * from xhy_test partition (xhy_test_p1)order by col_4;
select * from xhy_test partition (sys_p1)order by col_4;
select * from xhy_test partition (sys_p2)order by col_4;
select * from xhy_test partition (sys_p3)order by col_4;
select * from xhy_test partition (sys_p4)order by col_4;
select * from xhy_test partition (sys_p5)order by col_4;

drop table if exists xhy_test;
-- @testpoint: interval分区,创建时声明like子句,源表是普通表,新表是分区表,指定INCLUDING STORAGE

drop table if exists common_table_001;
drop table if exists partition_table_001;

-- 创建普通表作为分区表like的源表
create table common_table_001(
col_1 smallint primary key check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int unique,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float
);
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2'
and attrelid = (select oid from pg_class where relname='common_table_001');

alter table common_table_001 alter col_2 set storage main;
-- like指定INCLUDING STORAGE
create table partition_table_001(
like common_table_001 including storage)
partition by range (col_4)
interval ('1 year')
(
	partition partition_p1 values less than ('2018-01-01'),
	partition partition_p2 values less than ('2019-01-01'),
	partition partition_p3 values less than ('2020-01-01')
);

-- 验证storage被继承
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2'
and attrelid = (select oid from pg_class where relname='common_table_001');
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2'
and attrelid = (select oid from pg_class where relname='partition_table_001');

insert into partition_table_001 values (3,'ccc',3,'2018-04-23',true,'ccc',3.3);
insert into partition_table_001 values (4,'ddd',4,'2019-05-23',false,'ddd',4.4);
insert into partition_table_001 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into partition_table_001 values (6,'fff',6,'2021-07-23',false,'fff',6.6);

drop table if exists common_table_001;
drop table if exists partition_table_001;
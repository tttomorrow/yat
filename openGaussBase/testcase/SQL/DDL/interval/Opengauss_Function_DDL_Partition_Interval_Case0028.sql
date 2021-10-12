-- @testpoint: interval分区,创建时声明like子句,新表是分区表,指定INCLUDING RELOPTIONS，源表是列存表时合理报错

drop table if exists common_table_001;
drop table if exists partition_table_001;
drop table if exists partition_table_003;
drop table if exists partition_table_004;

-- 创建普通表作为分区表like的源表
create table common_table_001(
col_1 smallint primary key check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int unique,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float
)with(fillfactor=10);

-- like指定including reloptions
create table partition_table_001(
like common_table_001 including reloptions)
partition by range (col_4)
interval ('1 year')
(
	partition partition_p1 values less than ('2018-01-01'),
	partition partition_p2 values less than ('2019-01-01'),
	partition partition_p3 values less than ('2020-01-01')
);

-- 创建列存表作为分区表like的源表
create table partition_table_003(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)with (orientation = column);

-- like指定including reloptions
create table partition_table_004(
like partition_table_003 including reloptions
)
partition by range (col_4)
interval ('1 month')
(
	partition partition_table_001_p1 values less than ('2020-03-01'),
	partition partition_table_001_p2 values less than ('2020-04-01'),
	partition partition_table_001_p3 values less than ('2020-05-01')
);

drop table if exists common_table_001;
drop table if exists partition_table_001;
drop table if exists partition_table_003;
drop table if exists partition_table_004;
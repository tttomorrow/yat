-- @testpoint: interval分区,分区方式partition_start_end_item的语法校验，合理报错
drop table if exists partition_table_001;

-- 未遵循：每个partition_start_end_item中的START值（如果有的话，下同）必须小于其END值；
create table partition_table_001(
col_1 smallint check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int,
col_4 date primary key,
col_5 boolean,
col_6 nchar(30),
col_7 float
)partition by range (col_4)
interval ('1 month')
(partition partition_p1 start ('2023-11-01') end ('2019-02-06 00:00:00') every ('1 month'));

-- 未遵循：相邻的两个partition_start_end_item，第一个的END值必须等于第二个的START值；
create table partition_table_001(
col_1 smallint check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int,
col_4 date primary key,
col_5 boolean,
col_6 nchar(30),
col_7 float
)partition by range (col_4)
interval ('1 month')
(partition partition_p1 start ('2018-11-01') end ('2019-02-06 00:00:00') every ('1 month'),
partition partition_p2 start ('2021-11-01') end ('2023-02-06 00:00:00') every ('1 month'));

-- 未遵循：每个partition_start_end_item中的EVERY值必须是正向递增的，且必须小于（END-START）值；
create table partition_table_001(
col_1 smallint check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int,
col_4 date primary key,
col_5 boolean,
col_6 nchar(30),
col_7 float
)partition by range (col_4)
interval ('1 month')
(partition partition_p1 start ('2018-11-01') end ('2019-02-06 00:00:00') every ('10 years'));


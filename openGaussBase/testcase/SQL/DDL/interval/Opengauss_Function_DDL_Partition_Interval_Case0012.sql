-- @testpoint: interval分区,同时指定多个分区键,合理报错
drop table if exists partition_table_001;

create table partition_table_001( 
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean, 
col_6 nchar(30),
col_7 float,
col_8 date,
col_9 date
)
partition by range (col_4,col_8,col_9)
interval ('1 month') 
(
	partition partition_table_001_p1 values less than ('2020-03-01'),
	partition partition_table_001_p2 values less than ('2020-04-01'),
	partition partition_table_001_p3 values less than ('2020-05-01')
);

drop table if exists partition_table_001;

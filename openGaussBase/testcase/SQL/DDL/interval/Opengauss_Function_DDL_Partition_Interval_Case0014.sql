-- @testpoint: interval分区,分区表包含唯一键，但唯一键不是分区键，合理报错
-- @DETAIL:  Columns of PRIMARY KEY/UNIQUE constraint Must contain partition KEY
drop table if exists partition_table_001;

create table partition_table_001( 
col_1 smallint unique,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean, 
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month') 
(
	partition partition_table_001_p1 values less than ('2020-03-01'),
	partition partition_table_001_p2 values less than ('2020-04-01'),
	partition partition_table_001_p3 values less than ('2020-05-01')
);

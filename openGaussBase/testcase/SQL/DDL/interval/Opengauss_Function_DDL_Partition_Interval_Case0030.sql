-- @testpoint: interval分区,创建时声明like子句,源表及新表都是分区表，指定including partition,新表再指定partition by时合理报错
drop table if exists partiton_table_001;
drop table if exists partiton_table_002;

create table partiton_table_001(
col_1 smallint,
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
	partition partiton_table_001_p1 values less than ('2020-03-01'),
	partition partiton_table_001_p2 values less than ('2020-04-01'),
	partition partiton_table_001_p3 values less than ('2020-05-01')
);

-- ERROR:  unsupport "like clause including partition" for partitioned table
create table partiton_table_002(
like partiton_table_001 including partition
)
partition by range (col_4)
interval ('1 month')
(
	partition partiton_table_001_p1 values less than ('2020-03-01'),
	partition partiton_table_001_p2 values less than ('2020-04-01'),
	partition partiton_table_001_p3 values less than ('2020-05-01')
);

drop table if exists partiton_table_001;
drop table if exists partiton_table_002;
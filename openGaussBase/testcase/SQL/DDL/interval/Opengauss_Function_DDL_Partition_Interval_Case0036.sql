-- @testpoint: interval分区,在创建分区表时START END与LESS THAN语法混合使用,合理报错
drop table if exists partition_table_001;
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
(partition partition_p1 start ('2018-11-01') end ('2019-02-06') every ('1 month'),
partition partition_p2 values less than ('2018-01-01'),
partition partition_p3 values less than ('2018-01-01'));
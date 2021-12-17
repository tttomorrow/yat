-- @testpoint: interval分区,partition_name作为分区名称前缀时，其长度不要超过57字节，超过时自动截断
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
(partition partition_name_1234567890123456789012345678901234567890nnn
start ('2018-11-01') end ('2019-02-06 00:00:00') every ('1 month'));
select char_length('partition_name_1234567890123456789012345678901234567890nn');
drop table if exists partition_table_001;
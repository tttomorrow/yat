-- @testpoint: interval分区,创建分区表索引：LOCAL索引,未指定全部索引分区时合理报错

drop index if exists pt_idx_001;
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
interval ('1 month') 
(
	partition table1_p1 values less than ('2020-03-01'),
	partition table1_p2 values less than ('2020-04-01'),
	partition table1_p3 values less than ('2020-05-01')
);

-- LOCAL索引不支持部分索引
create index pt_idx_001 on table1(col_4) local
(
    partition col_4_index1,
    partition col_4_index2
); 

drop index if exists pt_idx_001;
drop table if exists table1;
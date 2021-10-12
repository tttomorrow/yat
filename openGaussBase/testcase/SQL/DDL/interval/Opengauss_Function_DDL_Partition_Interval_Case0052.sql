-- @testpoint: interval分区,创建分区表索引：GLOBAL索引
drop index if exists global_idx_3;
drop index if exists global_idx_4;
drop table if exists table1;

create table table1(
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
	partition table1_p1 values less than ('2020-03-01'),
	partition table1_p2 values less than ('2020-04-01'),
	partition table1_p3 values less than ('2020-05-01')
);

--创建global分区索引
create index global_idx_3 on table1(col_3) global;

--不指定关键字，默认创建global分区索引
create index global_idx_4 on table1(col_4);

drop index if exists global_idx_3;
drop index if exists global_idx_4;
drop table if exists table1;
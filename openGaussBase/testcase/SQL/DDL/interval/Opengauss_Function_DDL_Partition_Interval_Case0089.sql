-- @testpoint: interval分区,ALTER TABLE为指定分区表添加分区时合理报错
drop table if exists mytb9;

create table mytb9( 
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
	partition mytb9_p1 values less than ('2020-02-29')
);

alter table mytb9 add partition mytb9_p2 values less than ('2021-02-29');

drop table if exists mytb9;
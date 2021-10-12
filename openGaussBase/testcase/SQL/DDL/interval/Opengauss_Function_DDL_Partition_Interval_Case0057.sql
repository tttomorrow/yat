-- @testpoint: interval分区,不支持列存表，合理报错
drop table if exists partiton_table_001;

create table partiton_table_001(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)with (orientation = column)
partition by range (col_4)
interval ('1 month')
(
	partition partiton_table_001_p1 values less than ('2020-03-01'),
	partition partiton_table_001_p2 values less than ('2020-04-01'),
	partition partiton_table_001_p3 values less than ('2020-05-01')
);
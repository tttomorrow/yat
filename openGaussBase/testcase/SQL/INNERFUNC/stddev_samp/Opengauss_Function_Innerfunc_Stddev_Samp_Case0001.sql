-- @testpoint: 入参为数值类型的列，分组求标准差
drop table if exists test1;
create table test1(col_1 bigint, col_2 smallint, col_3 integer, col_4 real, col_5 double precision, col_6 numeric);
select stddev_samp(col_1), stddev_samp(col_2), stddev_samp(col_3), stddev_samp(col_4), stddev_samp(col_5), stddev_samp(col_6) from test1;
drop table if exists test1;
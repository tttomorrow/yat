-- @testpoint: 入参为数值类型的列，分组求标准差
drop table if exists test1;
create table test1(col_1 bigint, col_2 smallint, col_3 integer, col_4 real, col_5 double precision, col_6 numeric);
insert into test1 values(-9223372036854775808, -32768, -2147483648, 3.4e-38, 1E-30, 123456.12354);
insert into test1 values(-99999999999999, -30379, -99999999, 9.89, 1, 37.89);
insert into test1 values(9223372036854775807, 32767, 2147483647, 3.4e+38, 1E+38, 9999999999999999999.999999999999999);
select stddev_samp(col_1), stddev_samp(col_2), stddev_samp(col_3), stddev_samp(col_4), stddev_samp(col_5), stddev_samp(col_6) from test1;
drop table if exists test1;
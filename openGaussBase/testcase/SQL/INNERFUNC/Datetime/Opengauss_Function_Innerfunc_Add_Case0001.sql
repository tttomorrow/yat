-- @testpoint: 时间和日期操作符+，date与没有明确单位的整数相加
drop table if exists test_date01;
create table test_date01 (col1 date);
insert into test_date01 values ('2020-1-30');
select col1:: date + integer '7'  from test_date01;
drop table if exists test_date01;
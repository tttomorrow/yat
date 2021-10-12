-- @testpoint: 时间和日期操作符*，入参给reltime正负混合的时间间隔字符串
drop table if exists test_date01;
create table test_date01 (col1 reltime);
insert into test_date01 values ('-2 YEARS +5 MONTHS 10 DAYS');
select double precision '1.5' * col1  from test_date01;
select '10' * col1  from test_date01;
drop table if exists test_date01;
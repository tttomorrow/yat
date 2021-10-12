-- @testpoint: 时间和日期操作符*，入参给reltime正的时间间隔字符串
drop table if exists test_date01;
create table test_date01 (col1 reltime);
insert into test_date01 values ('1 years 1 mons 8 days 12:00:00');
select double precision '1.5' * col1  from test_date01;
select '10' * col1  from test_date01;
drop table if exists test_date01;
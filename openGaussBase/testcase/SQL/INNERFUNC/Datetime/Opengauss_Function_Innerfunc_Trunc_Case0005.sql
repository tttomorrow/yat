-- @testpoint: trunc函数入参给小数的年月日
drop table if exists test_date01;
create table test_date01 (clo1 interval);
insert into test_date01 values ('2.1 years 3.7 months 3 days 1.5 hours 1.5 minute 1.5 s');
select trunc(clo1) from test_date01;
SELECT trunc(interval '2.9 years 3 months 3.4 days 1.5 hours 1.5 minute 1.5 s');
drop table if exists test_date01;
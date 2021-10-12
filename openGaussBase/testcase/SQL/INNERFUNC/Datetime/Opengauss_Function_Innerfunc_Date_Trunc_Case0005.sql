-- @testpoint: date_trunc 函数入参给小数的时分秒
drop table if exists test_date01;
create table test_date01 (clo1 interval);
insert into test_date01 values ('2 years 3 months 3 days 1.5 hours 1.5 minute 1.5 s');
select date_trunc('hour', clo1) from test_date01;
SELECT date_trunc('hour', interval '2 years 3 months 3 days 1.5 hours 1.5 minute 1.5 s');
select date_trunc('minute', clo1) from test_date01;
SELECT date_trunc('minute', interval '2 years 3 months 3 days 1.5 hours 1.5 minute 1.5 s');
select date_trunc('second', clo1) from test_date01;
SELECT date_trunc('second', interval '2 years 3 months 3 days 1.5 hours 1.5 minute 1.5 s');
drop table if exists test_date01;
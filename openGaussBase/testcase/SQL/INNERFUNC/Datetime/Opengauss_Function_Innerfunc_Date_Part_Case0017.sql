-- @testpoint: date_part函数入参为POSTGRES格式表示的没有时分秒的时间段，获取时分秒
drop table if exists test_date01;
create table test_date01 (clo1 interval);
insert into test_date01 values ('2 years 3 months 3 days');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', interval '2 years 3 months 3 days');
select date_part('minute', clo1) from test_date01;
SELECT date_part('minute', interval '2 years 3 months 3 days');
select date_part('second', clo1) from test_date01;
SELECT date_part('second', interval '2 years 3 months 3 days');
drop table if exists test_date01;
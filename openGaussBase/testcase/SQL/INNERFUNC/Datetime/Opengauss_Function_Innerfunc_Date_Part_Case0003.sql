-- @testpoint: date_part函数入参给interval类型的时间段
drop table if exists test_date01;
create table test_date01 (clo1 interval);
insert into test_date01 values ('-2 YEARS +5 MONTHS 10 DAYS');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', interval '-2 YEARS +5 MONTHS 10 DAYS');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', interval '-2 YEARS +5 MONTHS 10 DAYS');
select date_part('year', clo1) from test_date01;
SELECT date_part('year', interval '-2 YEARS +5 MONTHS 10 DAYS');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', interval '-2 YEARS +5 MONTHS 10 DAYS');
drop table if exists test_date01;
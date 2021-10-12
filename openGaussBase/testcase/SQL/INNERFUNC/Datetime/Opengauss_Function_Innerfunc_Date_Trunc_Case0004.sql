-- @testpoint: date_trunc 函数入参给reltime类型的时间段，取值采用POSTGRES格式表示
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('-2 YEARS +5 MONTHS 10 DAYS');
select date_trunc('month', clo1) from test_date01;
SELECT date_trunc('month', reltime '-2 YEARS +5 MONTHS 10 DAYS');
select date_trunc('day', clo1) from test_date01;
SELECT date_trunc('day', reltime '-2 YEARS +5 MONTHS 10 DAYS');
select date_trunc('year', clo1) from test_date01;
SELECT date_trunc('year', reltime '-2 YEARS +5 MONTHS 10 DAYS');
select date_trunc('hour', clo1) from test_date01;
SELECT date_trunc('hour', reltime '-2 YEARS +5 MONTHS 10 DAYS');
drop table if exists test_date01;
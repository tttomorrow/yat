-- @testpoint: date_part函数入参给reltime类型的时间段,取值采用ISO-8601格式表示，包含日期和时间部分
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('P-1.1Y10M');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', reltime 'P-1.1Y10M');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', reltime 'P-1.1Y10M');
select date_part('year', clo1) from test_date01;
SELECT date_part('year', reltime 'P-1.1Y10M');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', reltime 'P-1.1Y10M');
drop table if exists test_date01;
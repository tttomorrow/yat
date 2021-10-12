-- @testpoint: date_part函数入参给reltime类型的时间段
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('-13 months -10 hours');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', reltime '-13 months -10 hours');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', reltime '-13 months -10 hours');
select date_part('year', clo1) from test_date01;
SELECT date_part('year', reltime '-13 months -10 hours');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', reltime '-13 months -10 hours');
drop table if exists test_date01;
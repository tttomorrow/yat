-- @testpoint: date_part函数入参给reltime类型的时间段,取值采用ISO-8601格式表示，只包含时间部分
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('-12H');
select date_part('m', clo1) from test_date01;
SELECT date_part('m', reltime '-12H');
select date_part('s', clo1) from test_date01;
SELECT date_part('s', reltime '-12H');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', reltime '-12H');
drop table if exists test_date01;
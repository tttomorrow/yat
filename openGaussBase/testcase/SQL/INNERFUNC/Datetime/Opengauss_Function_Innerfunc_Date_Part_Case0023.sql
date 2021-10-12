-- @testpoint: date_part给reltime类型的时间段取值负数
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('-365');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', reltime '-365');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', reltime '-365');
drop table if exists test_date01;
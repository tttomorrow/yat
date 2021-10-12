-- @testpoint: date_part给reltime类型的时间段取值小数
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('31.25');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', reltime '31.25');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', reltime '31.25');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', reltime '31.25');
drop table if exists test_date01;
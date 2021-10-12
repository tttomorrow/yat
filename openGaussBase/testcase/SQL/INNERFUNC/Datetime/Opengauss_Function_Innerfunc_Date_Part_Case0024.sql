-- @testpoint: date_part给reltime类型，取值采用POSTGRES格式表示
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('1 years 1 mons 8 days 12:00:00');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', reltime '1 years 1 mons 8 days 12:00:00');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', reltime '1 years 1 mons 8 days 12:00:00');
select date_part('year', clo1) from test_date01;
SELECT date_part('year', reltime '1 years 1 mons 8 days 12:00:00');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', reltime '1 years 1 mons 8 days 12:00:00');
drop table if exists test_date01;
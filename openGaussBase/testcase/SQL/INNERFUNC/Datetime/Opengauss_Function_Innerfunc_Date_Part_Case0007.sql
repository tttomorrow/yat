-- @testpoint: date_part函数入参给date类型，包含时间和日期
drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('2018-05-14 14:09:04.127444+08');
select date_part('m', clo1) from test_date01;
SELECT date_part('m', date '2018-05-14 14:09:04.127444+08');
select date_part('s', clo1) from test_date01;
SELECT date_part('s', date '2018-05-14 14:09:04.127444+08');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', date '2018-05-14 14:09:04.127444+08');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', date '2018-05-14 14:09:04.127444+08');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', date '2018-05-14 14:09:04.127444+08');
select date_part('year', clo1) from test_date01;
SELECT date_part('year', date '2018-05-14 14:09:04.127444+08');
drop table if exists test_date01;
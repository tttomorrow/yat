-- @testpoint: date_trunc 函数入参给timestamp without time zone
drop table if exists test_date01;
create table test_date01 (clo1 timestamp without time zone );
insert into test_date01 values ('2013-12-11');
select date_trunc('m', clo1) from test_date01;
SELECT date_trunc('m', timestamp without time zone  '2013-12-11');
select date_trunc('s', clo1) from test_date01;
SELECT date_trunc('s', timestamp without time zone  '2013-12-11');
select date_trunc('hour', clo1) from test_date01;
SELECT date_trunc('hour', timestamp without time zone  '2018-05-14 14:09:04.127444');
select date_trunc('month', clo1) from test_date01;
SELECT date_trunc('month', timestamp without time zone '2018-05-14 14:09:04.127444');
select date_trunc('day', clo1) from test_date01;
SELECT date_trunc('day', timestamp without time zone '2018-05-14 14:09:04.127444');
select date_trunc('year', clo1) from test_date01;
SELECT date_trunc('year', timestamp without time zone '2018-05-14 14:09:04.127444');
drop table if exists test_date01;
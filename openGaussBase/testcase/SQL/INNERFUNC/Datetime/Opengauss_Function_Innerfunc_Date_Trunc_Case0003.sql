-- @testpoint: date_trunc 函数入参给date
drop table if exists test_date01;
create table test_date01 (clo1 date );
insert into test_date01 values ('2013-12-11 pst');
select date_trunc('m', clo1) from test_date01;
SELECT date_trunc('m', date  '2013-12-11 pst');
select date_trunc('s', clo1) from test_date01;
SELECT date_trunc('s', date  '2013-12-11 pst');
select date_trunc('hour', clo1) from test_date01;
SELECT date_trunc('hour', date  '2018-05-14 14:09:04.127444+08');
select date_trunc('month', clo1) from test_date01;
SELECT date_trunc('month', date '2018-05-14 14:09:04.127444+08');
select date_trunc('day', clo1) from test_date01;
SELECT date_trunc('day', date '2018-05-14 14:09:04.127444+08');
select date_trunc('year', clo1) from test_date01;
SELECT date_trunc('year', date '2018-05-14 14:09:04.127444+08');
drop table if exists test_date01;
-- @testpoint: date_part函数入参给timestamp with time zone
drop table if exists test_date01;
create table test_date01 (clo1 timestamp with time zone );
insert into test_date01 values ('2013-12-11 pst');
select date_part('m', clo1) from test_date01;
SELECT date_part('m', timestamp with time zone  '2013-12-11 pst');
select date_part('s', clo1) from test_date01;
SELECT date_part('s', timestamp with time zone  '2013-12-11 pst');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', timestamp with time zone  '2018-05-14 14:09:04.127444+08');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', timestamp with time zone '2018-05-14 14:09:04.127444+08');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', timestamp with time zone '2018-05-14 14:09:04.127444+08');
select date_part('year', clo1) from test_date01;
SELECT date_part('year', timestamp with time zone '2018-05-14 14:09:04.127444+08');
drop table if exists test_date01;
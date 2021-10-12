-- @testpoint: date_part函数入参给time with time zone
drop table if exists test_date01;
create table test_date01 (clo1 time with time zone);
insert into test_date01 values ('21:21:21 pst');
select date_part('m', clo1) from test_date01;
SELECT date_part('m', time with time zone '21:21:21 pst');
select date_part('s', clo1) from test_date01;
SELECT date_part('s', time with time zone '21:21:21 pst');
select date_part('hour', clo1) from test_date01;
SELECT date_part('hour', time with time zone '21:21:21 pst');
drop table if exists test_date01;
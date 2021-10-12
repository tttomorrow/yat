-- @testpoint: trunc函数入参给timestamp with time zone
drop table if exists test_date01;
create table test_date01 (clo1 timestamp with time zone );
insert into test_date01 values ('2013-12-11 pst');
insert into test_date01 values ('2018-05-14 14:09:04.127444+08');
select trunc( clo1) from test_date01;
SELECT trunc(timestamp with time zone  '2013-12-11 pst');
drop table if exists test_date01;
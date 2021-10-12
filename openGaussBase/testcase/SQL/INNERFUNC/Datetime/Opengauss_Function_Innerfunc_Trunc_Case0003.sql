-- @testpoint: trunc函数入参给date类型
drop table if exists test_date01;
create table test_date01 (clo1 date );
insert into test_date01 values ('2013-12-11 pst');
insert into test_date01 values ('2018-05-14 14:09:04.127444+08');
select trunc(clo1) from test_date01;
SELECT trunc(date  '2013-12-11 pst');
drop table if exists test_date01;
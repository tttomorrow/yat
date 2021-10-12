-- @testpoint: trunc函数入参给timestamp without time zone
drop table if exists test_date01;
create table test_date01 (clo1 timestamp without time zone );
insert into test_date01 values ('2013-12-11');
insert into test_date01 values ('2018-05-14 14:09:04.127444');
select trunc(clo1) from test_date01;
SELECT trunc(timestamp  '2001-02-16 20:38:40');
drop table if exists test_date01;
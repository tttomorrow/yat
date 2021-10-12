-- @testpoint: EXTRACT函数传入date类型，source为EPOCH边界值不带时区，获取自1970-01-01 00:00:00-00 UTC以来的秒数
drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('1970-01-01 00:00:00 ');
select EXTRACT(EPOCH FROM clo1) from test_date01;
SELECT EXTRACT(EPOCH FROM date '1970-01-01 00:00:00 ');
SELECT EXTRACT(EPOCH FROM date '1970-01-01 00:00:00 ');
SELECT EXTRACT(EPOCH FROM date '1970-01-01 00:00:00');
drop table if exists test_date01;
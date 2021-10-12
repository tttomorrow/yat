-- @testpoint: 从IME类型数据（am/pm）中获取hour
drop table if exists test_date01;
create table test_date01 (clo1 TIME with time zone);
insert into test_date01 values ('11:00:00+08 AM');
select EXTRACT(HOUR FROM clo1) from test_date01;
SELECT EXTRACT(HOUR FROM TIME '8:00:00 PM');
drop table if exists test_date01;
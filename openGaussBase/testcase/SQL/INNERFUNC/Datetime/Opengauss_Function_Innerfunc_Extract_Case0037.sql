-- @testpoint: 从TIME类型数据（带时区与不带时区）中获取hour
drop table if exists test_date01;
create table test_date01 (clo1 TIME with time zone);
insert into test_date01 values ('23:00:00+08');
select EXTRACT(HOUR FROM clo1) from test_date01;
SELECT EXTRACT(HOUR FROM TIME '00:00:00');
drop table if exists test_date01;
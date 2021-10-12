-- @testpoint: 从INTERVAL类型数据（带时区与不带时区）中获取hour
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL);
insert into test_date01 values ('36 hours 88 m');
select EXTRACT(HOUR FROM clo1) from test_date01;
SELECT EXTRACT(HOUR FROM INTERVAL '3 months 24 hours');
drop table if exists test_date01;
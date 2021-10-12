-- @testpoint: 从reltime类型数据（带时区与不带时区）中获取hour
drop table if exists test_date01;
create table test_date01 (clo1 reltime);
insert into test_date01 values ('-13 months -10 hours');
select EXTRACT(HOUR FROM clo1) from test_date01;
SELECT EXTRACT(HOUR FROM reltime 'P-1.1Y10M');
drop table if exists test_date01;
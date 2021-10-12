-- @testpoint: EXTRACT 时间格式为INTERVAL时没有天或者天数为0时获取day
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL );
insert into test_date01 values ('3 months');
select EXTRACT(DAY FROM clo1) from test_date01;
SELECT EXTRACT(DAY FROM INTERVAL '40 years 3 months');
drop table if exists test_date01;
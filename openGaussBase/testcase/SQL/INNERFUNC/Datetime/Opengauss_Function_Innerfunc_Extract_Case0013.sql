-- @testpoint: EXTRACT 时间格式为INTERVAl小数的年份除以10
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL);
insert into test_date01 values ('12.5 years');
select EXTRACT(DECADE FROM clo1) from test_date01;
SELECT EXTRACT(DECADE FROM INTERVAL '12.5 years');
drop table if exists test_date01;
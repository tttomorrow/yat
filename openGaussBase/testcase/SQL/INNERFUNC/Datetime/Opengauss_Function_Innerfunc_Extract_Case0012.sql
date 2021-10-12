-- @testpoint: EXTRACT函数从INTERVAl类型中提取小时
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL);
insert into test_date01 values ('P0001-02-03T04:05:06');
insert into test_date01 values ('1-4');
select EXTRACT(hour FROM clo1) from test_date01;
SELECT EXTRACT(hour FROM INTERVAL '1-2');
SELECT EXTRACT(hour FROM INTERVAL '3 4:05:06');
SELECT EXTRACT(hour FROM INTERVAL '1 year 2 months 3 days 4 hours 5 minutes 6 seconds');
SELECT EXTRACT(hour FROM INTERVAL 'P1Y2M3DT4H5M6S');
SELECT EXTRACT(hour FROM INTERVAL 'P0001-02-03T04:05:06');
select EXTRACT(hour FROM clo1) from test_date01;
drop table if exists test_date01;
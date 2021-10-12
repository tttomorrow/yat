-- @testpoint: EXTRACT函数传入source为interval，获取时间间隔的总秒数
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL );
insert into test_date01 values ('1 s ');
select EXTRACT(EPOCH FROM clo1) from test_date01;
SELECT EXTRACT(EPOCH FROM INTERVAL  '1 year 2 months 5 days 3 hours 2 m 8 s');
SELECT EXTRACT(EPOCH FROM INTERVAL  '10000s');
drop table if exists test_date01;
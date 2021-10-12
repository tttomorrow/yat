-- @testpoint: EXTRACT函数传入source为interval，不带秒部分，获取时间间隔的总秒数
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL );
insert into test_date01 values ('60');
select EXTRACT(EPOCH FROM clo1) from test_date01;
SELECT EXTRACT(EPOCH FROM INTERVAL  '31.25');
SELECT EXTRACT(EPOCH FROM INTERVAL  '1 years 1 mons 8 days 12:00:00');
drop table if exists test_date01;
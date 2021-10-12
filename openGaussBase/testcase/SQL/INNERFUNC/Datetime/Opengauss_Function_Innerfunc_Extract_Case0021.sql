--  @testpoint: EXTRACT 每年的第几天返回 每年的最后一天（平年闰年） timestamp和date
drop table if exists test_date01;
create table test_date01 (clo1 timestamp);
insert into test_date01 values ('2020-03-01 00:00:00');
select EXTRACT(DOY FROM clo1) from test_date01;
SELECT EXTRACT(DOY FROM timestamp '0001-03-01 00:00:00');
SELECT EXTRACT(DOY FROM date '1600-12-31 00:00:00');
SELECT EXTRACT(DOY FROM date '2021-12-31 00:00:00');
SELECT EXTRACT(DOY FROM date '9999-12-31 00:00:00');
drop table if exists test_date01;
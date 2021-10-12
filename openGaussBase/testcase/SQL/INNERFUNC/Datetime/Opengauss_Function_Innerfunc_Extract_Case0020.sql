--  @testpoint: EXTRACT 每年的第几天返回 每年的第一天 timestamp和date
drop table if exists test_date01;
create table test_date01 (clo1 timestamp);
insert into test_date01 values ('9999-01-01 00:00:00');
select EXTRACT(DOY FROM clo1) from test_date01;
SELECT EXTRACT(DOY FROM timestamp '0001-01-01 00:00:00');
SELECT EXTRACT(DOY FROM date '9999-01-01 00:00:00');
SELECT EXTRACT(DOY FROM date '9999-01-02 00:00:00');
drop table if exists test_date01;
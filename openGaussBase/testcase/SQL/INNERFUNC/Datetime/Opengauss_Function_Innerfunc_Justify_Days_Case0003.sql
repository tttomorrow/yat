--  @testpoint: justify_days 小时超过24
drop table if exists test_date01;
create table test_date01 (clo1 interval );
insert into test_date01 values ('1 year 33 months 30 days 55 hours 3 m 4 s');
select JUSTIFY_HOURS(clo1) from test_date01;
SELECT JUSTIFY_HOURS(interval  '1 year 33 months 30 days 55 hours 3 m 4 s');
drop table if exists test_date01;
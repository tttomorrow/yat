--  @testpoint: isfinite time类型的参数不带时区
drop table if exists test_date01;
create table test_date01 (clo1 time without time zone);
insert into test_date01 values ('21:28:30');
select isfinite(clo1) from test_date01;
SELECT isfinite(time without time zone  '21:28:30');
drop table if exists test_date01;
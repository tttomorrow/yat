--  @testpoint: isfinite 年月日不带时区
drop table if exists test_date01;
create table test_date01 (clo1 date );
insert into test_date01 values ('2013-12-11');
select isfinite(clo1) from test_date01;
SELECT isfinite(date  '2013-12-11');
drop table if exists test_date01;
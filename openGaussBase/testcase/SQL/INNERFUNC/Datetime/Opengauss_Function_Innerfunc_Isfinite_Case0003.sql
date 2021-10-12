--  @testpoint: isfinite 年月日时分秒不带时区
drop table if exists test_date01;
create table test_date01 (clo1 date );
insert into test_date01 values ('2018-03-08 18:55:33');
select isfinite(clo1) from test_date01;
SELECT isfinite(date  '2018-03-08 18:55:33');
drop table if exists test_date01;
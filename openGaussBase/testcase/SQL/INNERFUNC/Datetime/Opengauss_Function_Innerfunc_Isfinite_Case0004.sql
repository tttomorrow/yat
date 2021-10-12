--  @testpoint: isfinite 年月日时分秒带时区
drop table if exists test_date01;
create table test_date01 (clo1 date );
insert into test_date01 values ('2018-05-14 14:09:04.127444+08');
select isfinite(clo1) from test_date01;
SELECT isfinite(date  '2018-05-14 14:09:04.127444+08');
drop table if exists test_date01;
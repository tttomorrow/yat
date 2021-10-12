--  @testpoint: isfinite 无效时间
drop table if exists test_date01;
create table test_date01 (clo1 date );
insert into test_date01 values ('infinity');
select isfinite(clo1) from test_date01;
SELECT isfinite(date  'infinity');
drop table if exists test_date01;
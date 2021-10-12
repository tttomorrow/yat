--  @testpoint: isfinite timestamp无效日期
drop table if exists test_date01;
create table test_date01 (clo1 timestamp with time zone );
insert into test_date01 values ('infinity');
select isfinite(clo1) from test_date01;
SELECT isfinite(timestamp with time zone  'infinity');
drop table if exists test_date01;
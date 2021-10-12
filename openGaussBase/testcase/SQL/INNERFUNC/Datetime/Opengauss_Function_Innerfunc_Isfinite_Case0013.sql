--  @testpoint: isfinite interval 时间段
drop table if exists test_date01;
create table test_date01 (clo1 interval );
insert into test_date01 values ('1 year 33 months 1.5 hours 3 m 4 s');
select isfinite(clo1) from test_date01;
SELECT isfinite(interval  '1 year 33 months 1.5 hours 3 m 4 s');
drop table if exists test_date01;
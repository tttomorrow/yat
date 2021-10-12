--  @testpoint: isfinite reltime 时间段
drop table if exists test_date01;
create table test_date01 (clo1 reltime );
insert into test_date01 values ('60');
select isfinite(clo1) from test_date01;
SELECT isfinite(reltime  '60');
drop table if exists test_date01;
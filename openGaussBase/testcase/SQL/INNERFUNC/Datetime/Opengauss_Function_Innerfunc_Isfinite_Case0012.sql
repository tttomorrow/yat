--  @testpoint: isfinite SMALLDATETIME
drop table if exists test_date01;
create table test_date01 (clo1 SMALLDATETIME );
insert into test_date01 values ('2003-04-12 04:05:06');
select isfinite(clo1) from test_date01;
SELECT isfinite(SMALLDATETIME  '2003-04-12 04:05:06');
drop table if exists test_date01;
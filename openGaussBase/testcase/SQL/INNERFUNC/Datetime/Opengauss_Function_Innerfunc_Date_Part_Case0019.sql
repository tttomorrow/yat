-- @testpoint: date_part函数给浮点数的年月日
drop table if exists test_date01;
create table test_date01 (clo1 interval);
insert into test_date01 values ('1.5 years 1.5 months 1.5 days');
select date_part('year', clo1) from test_date01;
SELECT date_part('year', interval '1.5 years 1.5 months 1.5 days');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', interval '1.5 years 1.5 months 1.5 days');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', interval '1.5 years 1.5 months 1.5 days');
drop table if exists test_date01;
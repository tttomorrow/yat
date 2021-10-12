-- @testpoint: date_part函数年份月份取模验证
drop table if exists test_date01;
create table test_date01 (clo1 interval);
insert into test_date01 values ('2 years 25 months 55 days');
select date_part('year', clo1) from test_date01;
SELECT date_part('year', interval '2 years 25 months 55 days');
select date_part('month', clo1) from test_date01;
SELECT date_part('month', interval '2 years 25 months 55 days');
select date_part('day', clo1) from test_date01;
SELECT date_part('day', interval '2 years 25 months 55 days');
drop table if exists test_date01;
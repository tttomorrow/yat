--  @testpoint: EXTRACT 时间格式为INTERVAL时取day小数
drop table if exists test_date01;
create table test_date01 (clo1 INTERVAL );
insert into test_date01 values ('3.5 months');
select EXTRACT(DAY FROM clo1) from test_date01;
SELECT EXTRACT(DAY FROM INTERVAL '40 days 3.5 months');
drop table if exists test_date01;
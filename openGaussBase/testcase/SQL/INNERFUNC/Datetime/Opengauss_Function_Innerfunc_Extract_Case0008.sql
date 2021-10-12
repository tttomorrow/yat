-- @testpoint: EXTRACT 时间格式为time时取day合理报错
drop table if exists test_date01;
create table test_date01 (clo1 time without time zone );
insert into test_date01 values ('2001-01-31 00:00:00');
select EXTRACT(DAY FROM clo1) from test_date01;
drop table if exists test_date01;
-- @testpoint: 时间和日期操作符+，time与时间间隔相加
drop table if exists test_date01;
create table test_date01 (col1 time);
insert into test_date01 values ('04:59:59');
select time '04:59:59' + interval '3 hours'    from test_date01;
drop table if exists test_date01;
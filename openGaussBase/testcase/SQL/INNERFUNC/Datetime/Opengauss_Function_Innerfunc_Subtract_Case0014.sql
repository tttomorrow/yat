-- @testpoint: date类型时间间隔相减
drop table if exists test_date01;
create table test_date01 (col1 date);
insert into test_date01 values ('2020-1-1');
select date '2019-1-6' -  col1  from test_date01;
drop table if exists test_date01;
-- @testpoint: 时间和日期相减
drop table if exists test_date01;
create table test_date01 (col1 date);
insert into test_date01 values ('2020-4-1');
select col1:: date - time '03:00'   from test_date01;
drop table if exists test_date01;
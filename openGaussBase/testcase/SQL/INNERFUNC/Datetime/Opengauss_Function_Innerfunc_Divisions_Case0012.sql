-- @testpoint: reltime整数时间段除以负数
drop table if exists test_date01;
create table test_date01 (col1 reltime);
insert into test_date01 values ('60');
select  col1/-10  from test_date01;
drop table if exists test_date01;
-- @testpoint: 时间和日期操作符*，reltime乘以负数
drop table if exists test_date01;
create table test_date01 (col1 reltime);
insert into test_date01 values ('60');
select '-10' * col1  from test_date01;
drop table if exists test_date01;
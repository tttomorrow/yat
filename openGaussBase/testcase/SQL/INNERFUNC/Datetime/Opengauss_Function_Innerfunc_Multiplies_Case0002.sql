-- @testpoint: 时间和日期操作符*，分钟间隔与整数相乘
drop table if exists test_date01;
create table test_date01 (col1 interval);
insert into test_date01 values ('10 m');
select 6 * col1  from test_date01;
select 145 * col1  from test_date01;
drop table if exists test_date01;
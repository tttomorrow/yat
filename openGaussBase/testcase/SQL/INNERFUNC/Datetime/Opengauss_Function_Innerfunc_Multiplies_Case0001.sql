-- @testpoint: 时间和日期操作符*，秒间隔与整数相乘
drop table if exists test_date01;
create table test_date01 (col1 interval);
insert into test_date01 values ('10 second');
select 6 * col1  from test_date01;
select 361 * col1  from test_date01;
drop table if exists test_date01;
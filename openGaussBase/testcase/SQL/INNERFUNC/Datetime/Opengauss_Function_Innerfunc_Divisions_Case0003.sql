-- @testpoint: 小时间隔与整数相除
drop table if exists test_date01;
create table test_date01 (col1 interval);
insert into test_date01 values ('1 h');
select col1/2  from test_date01;
select col1/3  from test_date01;
drop table if exists test_date01;
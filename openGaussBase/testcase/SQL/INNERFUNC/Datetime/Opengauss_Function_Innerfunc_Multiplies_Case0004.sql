-- @testpoint: 时间和日期操作符*，年月日与整数分别相乘
drop table if exists test_date01;
create table test_date01 (col1 interval);
insert into test_date01 values ('1 day');
insert into test_date01 values ('1 month');
insert into test_date01 values ('1 year');
select 145 * col1  from test_date01;
drop table if exists test_date01;
-- @testpoint: 年月日与整数相除
drop table if exists test_date01;
create table test_date01 (col1 interval);
insert into test_date01 values ('1 day');
insert into test_date01 values ('1 month');
insert into test_date01 values ('1 year');
select col1/2  from test_date01;
select col1/3  from test_date01;
drop table if exists test_date01;
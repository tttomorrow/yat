-- @testpoint: 闰年2月的验证
drop table if exists test_date01;
create table test_date01 (col1 date);
insert into test_date01 values ('1600-3-1');
select col1:: date - interval '1 hour'  from test_date01;
select col1:: date - interval '1 day'  from test_date01;
drop table if exists test_date01;
-- @testpoint: reltime负的时间间隔字符串与整数、浮点数相除
drop table if exists test_date01;
create table test_date01 (col1 reltime);
insert into test_date01 values ('-13 months -10 hours');
select col1 / double precision '1.5' from test_date01;
select col1/2  from test_date01;
drop table if exists test_date01;
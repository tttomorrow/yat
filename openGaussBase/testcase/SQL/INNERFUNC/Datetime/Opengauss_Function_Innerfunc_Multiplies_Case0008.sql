-- @testpoint: 时间和日期操作符*，入参给reltime时间间隔负数
drop table if exists test_date01;
create table test_date01 (col1 reltime);
insert into test_date01 values ('-365');
select double precision '1.5' * col1  from test_date01;
select '10' * col1  from test_date01;
drop table if exists test_date01;
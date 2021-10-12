-- @testpoint: 时间和日期操作符*，入参给reltimeISO-8601格式表示时间段
drop table if exists test_date01;
create table test_date01 (col1 reltime);
insert into test_date01 values ('-12H');
select double precision '1.5' * col1  from test_date01;
select '10' * col1  from test_date01;
drop table if exists test_date01;
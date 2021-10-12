-- @testpoint: 时间和日期操作符+，reltime类型与time类型相加
drop table if exists test_date01;
create table test_date01 (col1 reltime);
insert into test_date01 values ('60');
select col1 + time '19:00:01'   from test_date01;
drop table if exists test_date01;
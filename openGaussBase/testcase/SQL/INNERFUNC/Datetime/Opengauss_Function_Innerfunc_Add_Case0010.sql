-- @testpoint: 时间和日期操作符+，timestamp带时区与time类型相加
drop table if exists test_date01;
create table test_date01 (col1 timestamp with time zone);
insert into test_date01 values ('2003-04-12 04:59:00 pst');
select col1 + time '19:01' from test_date01;
drop table if exists test_date01;
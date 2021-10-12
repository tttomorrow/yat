-- @testpoint: 未含时区定义说明，边界值测试

drop table if exists test_time15;
create table test_time15 (name time);
insert into test_time15 values ('00:00:00.000000');
insert into test_time15 values ('23:59:59.999999');
select * from test_time15;
drop table if exists test_time15;
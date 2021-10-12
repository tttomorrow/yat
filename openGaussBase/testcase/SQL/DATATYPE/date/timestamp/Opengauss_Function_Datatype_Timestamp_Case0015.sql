-- @testpoint: 无效边界值测试，合理报错

drop table if exists test_timestamp15;
create table test_timestamp15 (name timestamp);
insert into test_timestamp15 values (to_timestamp('0000-00-00 00:00:00.000000','yyyy-mm-dd hh24:mi:ss.ff'));
insert into test_timestamp15 values (to_timestamp('9999-12-32 23:59:59.999999','yyyy-mm-dd hh24:mi:ss.ff'));
select * from test_timestamp15;
drop table if exists test_timestamp15;
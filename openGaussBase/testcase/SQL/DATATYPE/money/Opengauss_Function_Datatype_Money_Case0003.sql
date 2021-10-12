-- @testpoint: 插入负数值

drop table if exists test_money03;
create table test_money03 (name money);
insert into test_money03 values (-123.123);
insert into test_money03 values (-123);
select * from test_money03;
drop table test_money03;
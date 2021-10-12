-- @testpoint: 插入浮点数

drop table if exists test_money02;
create table test_money02 (name money);
insert into test_money02 values (123.123);
insert into test_money02 values (0.123);
insert into test_money02 values (9.032);
select * from test_money02;
drop table test_money02;
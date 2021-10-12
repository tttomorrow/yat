-- @testpoint: 输入无效数值,合理报错

drop table if exists test_money07;
create table test_money07 (name money);
insert into test_money07 values (12a12);
insert into test_money07 values (abc);
drop table test_money07;
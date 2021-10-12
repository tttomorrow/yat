--  @testpoint:设置default约束是可以推迟，创建失败
drop table if exists test_1;
create table test_1 (id int default deferrable ,name char(20));
drop table test_1;
--  @testpoint:设置unique约束是可以推迟，创建成功
drop table if exists test_1;
create table test_1 (id int unique deferrable ,name char(20));
drop table test_1;
--设置default约束是可以推迟，创建失败
--  @testpoint:临时表定义行访问控制策略，合理报错
--创建本地临时表
drop table if exists test_policy8 cascade;
create TEMPORARY table test_policy8(id int,usr varchar(20));
--创建行访问控制策略,合理报错ERROR:  do not support row level security policy on temp table "test_policy8"
drop POLICY if exists pol8 ON test_policy8;
CREATE POLICY pol8 ON test_policy8 FOR update TO PUBLIC USING (usr = current_user);
--创建全局临时表
drop table if exists test_policy9 cascade;
create global TEMPORARY table test_policy9(id int,usr varchar(20));
--创建行访问控制策略,成功，只有本地临时表不支持创建行访问控制策略
drop POLICY if exists pol9 ON test_policy9;
CREATE POLICY pol9 ON test_policy9 FOR update TO PUBLIC USING (usr = current_user);
--删除表
drop table if exists test_policy8 cascade;
drop table if exists test_policy9 cascade;
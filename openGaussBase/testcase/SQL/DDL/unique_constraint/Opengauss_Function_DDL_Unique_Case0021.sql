-- @testpoint: 使用alter...drop删除约束
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint021;
create table test_unique_constraint021 (id_p int not null unique, lastname varchar(255) not null, firstname varchar(255), address varchar(255), city varchar(255));
--通过系统表查询约束名等信息
select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint021');
--删除约束
alter table test_unique_constraint021 drop constraint test_unique_constraint021_id_p_key;
--通过系统表再次查询约束名等信息，约束名不存在
select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint021');
--删表
drop table if exists test_unique_constraint021;
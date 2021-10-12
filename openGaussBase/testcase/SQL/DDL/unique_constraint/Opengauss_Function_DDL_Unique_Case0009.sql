-- @testpoint: 创建单个字段的多列约束
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint009;
create table test_unique_constraint009 (id_p int not null unique, lastname varchar(255) not null unique,
firstname varchar(255), address varchar(255), city varchar(255));
--通过系统表查询约束信息
 select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint009') order by conname;
--删表
 drop table if exists test_unique_constraint009;
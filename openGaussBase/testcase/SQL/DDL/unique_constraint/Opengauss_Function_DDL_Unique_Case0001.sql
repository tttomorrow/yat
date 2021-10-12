-- @testpoint: 创建表,指定唯一约束,不带约束名
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint001;
create table test_unique_constraint001 (id_p int not null, lastname varchar(255) not null, firstname varchar(255),
 address varchar(255), city varchar(255),unique (id_p));
--通过系统表查询约束信息
 select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint001');
--删表
 drop table if exists test_unique_constraint001;
-- @testpoint: 创建约束，分别使用列约束和表约束
-- @modify at: 2020-11-23
--建表，指定唯一约束列重复
drop table if exists test_unique_constraint003;
create table test_unique_constraint003 (id_p int not null unique, lastname varchar(255) not null,
firstname varchar(255), address varchar(255), city varchar(255),constraint uc_personid unique (id_p) );
--通过系统表查询约束信息
 select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint003');
--删表
 drop table if exists test_unique_constraint003;
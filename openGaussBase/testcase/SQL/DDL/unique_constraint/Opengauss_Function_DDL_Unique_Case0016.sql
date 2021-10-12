-- @testpoint: alter重复增加唯一约束
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint016;
create table test_unique_constraint016 (id_p int not null, lastname varchar(255) not null, firstname varchar(255),
address varchar(255), city varchar(255),unique (id_p));
--增加唯一约束
alter table test_unique_constraint016 add unique (id_p);
--通过系统表查询约束信息
 select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint016') order by conname;
--删表
 drop table if exists test_unique_constraint016;
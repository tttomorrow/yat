-- @testpoint: 建表后，使用alter多次增加单列约束
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint013;
create table test_unique_constraint013 (id_p int not null, lastname varchar(255) not null,
firstname varchar(255), address varchar(255), city varchar(255));
--增加约束
alter table test_unique_constraint013 add unique (id_p);
--再次增加约束
alter table test_unique_constraint013 add unique (id_p);
--通过系统表查询约束信息
 select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint013') order by conname;
--删表
 drop table if exists test_unique_constraint013;
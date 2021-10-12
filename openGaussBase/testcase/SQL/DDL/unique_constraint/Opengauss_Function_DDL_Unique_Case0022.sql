-- @testpoint: 使用alter...drop删除约束，违反约束，合理报错
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint022;
create table test_unique_constraint022 (id_p int not null, lastname varchar(255) not null, firstname varchar(255), address varchar(255), city varchar(255),constraint uc_personid unique (id_p));
--插入数据，成功
insert into test_unique_constraint022 values(1,'mary','','','');
--唯一约束创建后不能插入相同数值，合理报错
insert into test_unique_constraint022 values(1,'mary','','','');
--查询约束名
select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint022');
--删除约束
alter table test_unique_constraint022 drop constraint uc_personid;
--再次查询约束名，不存在
select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint022');
--删表
drop table if exists test_unique_constraint022;

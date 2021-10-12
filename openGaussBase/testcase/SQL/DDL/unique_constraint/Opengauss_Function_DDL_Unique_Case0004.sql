-- @testpoint: 创建不带约束名字的联合唯一约束，违反联合唯一约束，合理报错
-- @modify at: 2020-11-23
--建表成功
drop table if exists test_unique_constraint004;
create table test_unique_constraint004 (id_p int not null unique, lastname varchar(255) not null, firstname varchar(255), address varchar(255), city varchar(255),unique (id_p,lastname));
--插入数据，成功
insert into test_unique_constraint004 values(1,'mary','','','');
insert into test_unique_constraint004 values(2,'mary','','','');
--插入数据，失败
insert into test_unique_constraint004 values(2,'mary','','','');
--通过系统表查询约束信息
 select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint004') order by conname;
--删表
 drop table if exists test_unique_constraint004;
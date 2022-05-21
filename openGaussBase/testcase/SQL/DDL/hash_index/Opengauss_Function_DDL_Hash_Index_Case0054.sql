-- @testpoint: 测试创建哈希索引时，索引模式名与表的模式名是否相同对创建哈希索引的影响，部分step合理报错

--创建模式
drop schema if exists sch1;
create schema sch1;
drop schema if exists sch2;
create schema sch2;

--创建表
drop table if exists sch1.t_hash_index_0054;
create table sch1.t_hash_index_0054(id01 int, id02 int) with(orientation=row);

--创建哈希索引(索引模式名与表相同)
create index sch1.i_hash_index_0054_01 on sch1.t_hash_index_0054 using hash(id01);
--创建哈希索引(索引模式名与表不相同)
create index sch2.i_hash_index_0054_02 on sch1.t_hash_index_0054 using hash(id02);

--删除哈希索引
drop index if exists sch1.i_hash_index_0054_01;
drop index if exists sch2.i_hash_index_0054_02;

--删除模式
drop schema if exists sch1 cascade;
drop schema if exists sch2 cascade;

--删除表、表空间
drop table sch1.t_hash_index_0054 cascade;
-- @testpoint: 测试create index在创建哈希索引时，表的模式名存在与否的影响，默认情况下表的模式名为public，部分step合理报错

--创建模式名
drop schema if exists sch1;
create schema sch1;

--创建表
drop table if exists sch1.t_hash_index_0053;
create table sch1.t_hash_index_0053(id01 int, in02 char) with(orientation=row);

--创建哈希索引(模式名存在)
create index sch1.i_hash_index_0053_01 on sch1.t_hash_index_0053 using hash(id01);
--创建哈希索引(模式名不存在)
create index sch2.i_hash_index_0053_02 on sch1.t_hash_index_0053 using hash(id02);

--删除哈希索引
drop index if exists sch1.i_hash_index_0053_01;

--删除表、表空间
drop table sch1.t_hash_index_0053 cascade;


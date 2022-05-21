-- @testpoint: 测试使用模式修饰表名与否对创建哈希索引的影响，部分step合理报错

--创建模式
drop schema if exists sch1;
create schema sch1;

--创建表
drop table if exists sch1.t_hash_index_0056;
create table sch1.t_hash_index_0056(id01 int, id02 int) with(orientation=row);

--创建哈希索引(使用模式修饰)
create index i_hash_index_0056_01 on sch1.t_hash_index_0056 using hash(id01);
--创建哈希索引(未使用模式修饰)
create index i_hash_index_0056_02 on t_hash_index_0056 using hash(id02);

--删除哈希索引
drop index if exists i_hash_index_0056_01;
drop index if exists i_hash_index_0056_02;

--删除表、表空间
drop table sch1.t_hash_index_0056 cascade;
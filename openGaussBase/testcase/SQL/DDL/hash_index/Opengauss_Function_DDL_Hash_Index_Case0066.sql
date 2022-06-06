-- @testpoint: 测试创建哈希索引时，表空间名存在与否的影响，部分step合理报错

--创建表空间
drop tablespace if exists ts_hash_index_0066_01;
create tablespace ts_hash_index_0066_01 relative location 'tablespace01/row_space01';

--创建表
drop table if exists t_hash_index_0066;
create table t_hash_index_0066
(
    id01 char(20),
    id02 char(20)
) 
with(orientation=row);

--创建哈希索引(表空间名存在)
create index t_hash_index_0066_01 on t_hash_index_0066 using hash(id01) tablespace ts_hash_index_0066_01;

--创建哈希索引(表空间名不存在)
create index t_hash_index_0066_02 on t_hash_index_0066 using hash(id02) tablespace ts_hash_index_0066_02;

--删除哈希索引
drop index if exists t_hash_index_0066_01;
drop index if exists t_hash_index_0066_02;

--删除表、表空间
drop table t_hash_index_0066 cascade;
drop tablespace ts_hash_index_0066_01;
-- @testpoint: 测试创建哈希索引时，调用函数带括号与不带括号的影响

--创建表
drop table if exists t_hash_index_0059;
create table t_hash_index_0059
(
    id01 char(20),
    id02 char(20)
) 
with(orientation=row);

--创建哈希索引(调用函数，不带括号)
create index i_hash_index_0059_01 on t_hash_index_0059 using hash(substr(id01,1,5));

--创建哈希索引(调用函数，带括号)
create index i_hash_index_0059_02 on t_hash_index_0059 using hash((substr(id02,1,5)));

--删除哈希索引
drop index if exists i_hash_index_0059_01;
drop index if exists i_hash_index_0059_02;

--删除表、表空间
drop table t_hash_index_0059 cascade;


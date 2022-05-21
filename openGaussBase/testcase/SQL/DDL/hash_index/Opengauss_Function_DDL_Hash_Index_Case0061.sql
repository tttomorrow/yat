-- @testpoint: 创建哈希索引时，表达式带不带括号的影响

--创建表
drop table if exists t_hash_index_0061;
create table t_hash_index_0061
(
    id01 int,
    id02 int
) 
with(orientation=row);

--创建哈希索引(表达式不带括号)
create index i_hash_index_0061_01 on t_hash_index_0061 using hash((id01*10));

--创建哈希索引(表达式带括号)
create index i_hash_index_0061_02 on t_hash_index_0061 using hash((id02*10));

--删除哈希索引
drop index if exists i_hash_index_0061_01;
drop index if exists i_hash_index_0061_02;

--删除表、表空间
drop table t_hash_index_0061 cascade;

-- @testpoint: 测试表名存在与否对创建哈希索引的影响，部分step合理报错

--创建表
drop table if exists t_hash_index_0057;
create table t_hash_index_0057(id01 int, id02 int) with(orientation=row);

--创建哈希索引(表名存在)
create index i_hash_index_0057_01 on t_hash_index_0057 using hash(id01);
--创建哈希索引(表名不存在)
create index i_hash_index_0057_02 on row_tab02 using hash(id02);

--删除哈希索引
drop index if exists i_hash_index_0057_01;
drop index if exists i_hash_index_0057_02;

--删除表、表空间
drop table t_hash_index_0057 cascade;

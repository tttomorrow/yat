-- @testpoint: 测试哈希索引是否支持修改存储参数

--创建表
drop table if exists t_hash_index_0035;
create table t_hash_index_0035(id01 char, id02 char) with(orientation=row);

--创建哈希索引
create index i_hash_index_0035 on t_hash_index_0035 using hash(id01);

--修改哈希索引(存储参数)
alter index i_hash_index_0035 set(fillfactor=75);
alter index i_hash_index_0035 set(fillfactor=45);

--删除哈希索引
drop index i_hash_index_0035;

--删除表、表空间
drop table t_hash_index_0035 cascade;
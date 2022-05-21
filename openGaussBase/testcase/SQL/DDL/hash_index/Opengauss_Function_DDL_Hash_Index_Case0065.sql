-- @testpoint: 测试创建哈希索引时，是否支持where表达式

--创建表
drop table if exists t_hash_index_0065;
create table t_hash_index_0065
(
    id01 int not null,
    id02 char(20)
) 
with(orientation=row);

--创建哈希索引(是否支持where)
create index i_hash_index_0065_01 on t_hash_index_0065 using hash(id01) where id01>10;
create index i_hash_index_0065_02 on t_hash_index_0065 using hash(id01) where id01 in('8','9');

--删除哈希索引
drop index if exists i_hash_index_0065_01;
drop index if exists i_hash_index_0065_02;

--删除表、表空间
drop table t_hash_index_0065 cascade;

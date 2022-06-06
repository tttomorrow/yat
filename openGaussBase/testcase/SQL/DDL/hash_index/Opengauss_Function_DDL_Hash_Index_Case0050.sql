-- @testpoint: 测试create index concurrently关键字创建哈希索引及与insert 结合使用，部分step合理报错

--创建表
drop table if exists t_hash_index_0050;
create table t_hash_index_0050(id01 int,id02 int,id03 char(20)) with(orientation=row);

--创建哈希索引(单索引)
create index concurrently i_hash_index_0050_01 on t_hash_index_0050 using hash(id01);
--创建哈希索引(多个索引)
create index concurrently i_hash_index_0050_02,i_hash_index_0050_03 on t_hash_index_0050 using btree(id02,id03);
create index concurrently i_hash_index_0050_02,i_hash_index_0050_03 on t_hash_index_0050 using hash(id02,id03);
--删除哈希索引
drop index if exists i_hash_index_0050_01;
drop index if exists i_hash_index_0050_02;
drop index if exists i_hash_index_0050_03;

--删除表、表空间
drop table t_hash_index_0050 cascade;
--------------------------------------------
/*与insert操作联合使用*/
drop table if exists t_hash_index_0050;
create table t_hash_index_0050(id01 int,id02 int,id03 char(20)) with(orientation=row);

--创建哈希索引(单索引)
create index concurrently i_hash_index_0050_01 on  t_hash_index_0050 using hash(id01);
insert into t_hash_index_0050 select random()*10, random()*3, 'XXX' from generate_series(1,5000);
--删除哈希索引
drop index if exists i_hash_index_0050_01;
--删除表、表空间
drop table t_hash_index_0050 cascade;

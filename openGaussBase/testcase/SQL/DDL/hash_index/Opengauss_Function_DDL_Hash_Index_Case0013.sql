-- @testpoint: 创建hash索引后，查询表的ctid后进行聚簇排序，合理报错
--创建哈希索引
drop table if exists t_hash_index_0013;
create table t_hash_index_0013 (id int, sex varchar default 'male');
insert into t_hash_index_0013 values(10,default),(8,default),(9,default),(7,default),(6,default),(3,default),(4,default),(5,default);
drop index if exists i_hash_index_0013 ;
create index i_hash_index_0013 on t_hash_index_0013 using hash (id);
--查询,数据的原始ctid是插入数据的顺序
select ctid,* from  t_hash_index_0013;
--执行聚簇排序，合理报错（目前只有btree索引支持聚簇排序）
cluster t_hash_index_0013 using i_hash_index_0013;
--清理环境
drop table if exists t_hash_index_0013;
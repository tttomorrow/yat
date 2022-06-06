-- @testpoint: Hash分区表结合生成列（generated）生成列作为分区键 合理报错

--step1：创建hash分区表 expect：合理报错
drop table if exists partition_hash_tab;
create table if not exists partition_hash_tab
(id        int,
 p_id    int generated always as ( id+1 ) stored)
partition by hash(p_id)
(partition p1,
 partition p2);
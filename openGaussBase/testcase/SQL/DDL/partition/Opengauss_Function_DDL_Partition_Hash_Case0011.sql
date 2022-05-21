-- @testpoint: hash分区表，支持的功能 row movement
--创建hash分区表,指定参数row movement
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int,p_name varchar,p_age int)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3) enable row movement;

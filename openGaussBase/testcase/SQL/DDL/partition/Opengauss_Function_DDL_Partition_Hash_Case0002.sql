-- @testpoint: 创建普通hash分区表，验证分区键支持个数，多列合理报错

--分区键仅支持单列（1个）
drop table if exists partition_hash_tab01;
create table partition_hash_tab01(p_id int,p_name varchar,p_age int)
partition by hash(p_id)
(partition part_1,
 partition part_2,
 partition part_3);

 --分区键指定多个列，合理报错
drop table if exists partition_hash_tab02;
create table partition_hash_tab02(p_id int,p_name varchar,p_age int)
partition by hash(p_id,p_name)
(partition part_1,
 partition part_2,
 partition part_3);

--清理环境
drop table if exists partition_hash_tab01;
drop table if exists partition_hash_tab02;

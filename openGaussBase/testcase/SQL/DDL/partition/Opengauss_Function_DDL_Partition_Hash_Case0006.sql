-- @testpoint: 创建普通hash分区表，验证不支持的数据类型，合理报错

--不支持的数据类型：float
drop table if exists partition_hash_tab_t1;
create table partition_hash_tab_t1(p_id float,p_name char)
partition by hash(p_id)
(partition part_1,
 partition part_2);

--不支持的数据类型：bool
drop table if exists partition_hash_tab_t2;
create table partition_hash_tab_t2(p_id int,p_name char,p_status bool)
partition by hash(p_status)
(partition part_1,
 partition part_2);

--不支持的数据类型：二进制类型
drop table if exists partition_hash_tab_t3;
create table partition_hash_tab_t3(p_id raw,p_name char,p_date date)
partition by hash(p_id)
(partition part_1,
 partition part_2);

--不支持的数据类型，几何类型
drop table if exists partition_hash_tab_t4;
create table partition_hash_tab_t2(p_id int,p_name char,p_dir point)
partition by hash(p_dir)
(partition part_1,
 partition part_2);

--清理环境
--No need to clean
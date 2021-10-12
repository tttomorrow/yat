-- @testpoint: hash分区表，修改分区，合理报错

--创建hash分区表
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int,p_name varchar,p_age int)
partition by hash(p_id)
(partition p1,
 partition p2,
 partition p3);

--删除分区,合理报错
alter table partition_hash_tab drop partition p2;

--增加分区，合理报错
alter table partition_hash_tab add partition p4;

--合并分区，合理报错
alter table partition_hash_tab merge partition p2,p3 into partition p1;

--清理环境
drop table partition_hash_tab;
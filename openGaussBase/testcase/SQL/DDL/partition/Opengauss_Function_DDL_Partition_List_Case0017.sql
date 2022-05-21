-- @testpoint: list分区表，不支持的功能合成分区，合理报错

--step1:创建list分区表 expect成功
drop table if exists t_partition_list_0017;
create table t_partition_list_0017(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30));

 --step2:合并分区，expect失败
 alter table t_partition_list_0017 MERGE PARTITIONS p1,p2 INTO PARTITION p31;

 --step3:清理环境，expect成功
 drop table t_partition_list_0017;
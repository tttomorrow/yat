-- @testpoint: 分区个数大于1时删除分区

--step1:创建分区表，expect成功
drop table if exists t_partition_list_0031;
create table t_partition_list_0031(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--step2:删除分区，expect成功
ALTER TABLE t_partition_list_0031 DROP PARTITION part_3;

--step3:查看分区信息，expect成功
 SELECT t1.relname, partstrategy, boundaries FROM pg_partition t1, pg_class t2 WHERE t1.parentid = t2.oid AND t2.relname = 't_partition_list_0031' AND t1.parttype = 'p' order by relname ASC;


--step4:清理环境，expect成功
drop table t_partition_list_0031;
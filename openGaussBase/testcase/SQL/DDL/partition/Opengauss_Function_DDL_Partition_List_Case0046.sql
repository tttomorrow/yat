-- @testpoint: 分区个数小于64时添加分区

--step1:.创建list分区表;expect:成功
drop table if exists t_partition_list_0046;
create table t_partition_list_0046(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--step2:添加分区;expect:成功
 alter table t_partition_list_0046 add partition part_4 values (40);

--step3:查看分区表数据;expect:成功
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 't_partition_list_0046' and t1.parttype = 'p' order by relname asc;

--step4:清理环境;expect:成功
drop table t_partition_list_0046;


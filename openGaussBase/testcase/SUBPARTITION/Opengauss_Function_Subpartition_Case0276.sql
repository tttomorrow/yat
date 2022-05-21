-- @testpoint: range_range二级分区表：split,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0276;
drop tablespace if exists ts_subpartition_0276;
create tablespace ts_subpartition_0276 relative location 'subpartition_tablespace/subpartition_tablespace_0276';

--test1: alter table  split 指定值分割
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0276
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0276
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0276 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step4: 修改二级分区表，split一级分区; expect:合理报错
alter table t_subpartition_0276 split partition for (5) at (8) into ( partition add_p_01 , partition add_p_02 );
--step5: 修改二级分区表，split二级分区; expect:合理报错
alter table t_subpartition_0276 split subpartition for (5) at (8) into ( subpartition add_p_01 , subpartition add_p_02 );

--test2: alter table  split 不指定分割点
--step6: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0276;
create   table if not exists t_subpartition_0276
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0276
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step7: 修改二级分区表，split非default一级分区值; expect:合理报错
alter table t_subpartition_0276 split partition for (5) into  
(partition add_p_01 values less than( 2 ),partition add_p_02 values less than(10));
--step8: 修改二级分区表，split非default二级分区值; expect:合理报错
alter table t_subpartition_0276 split subpartition for (5) into  
(subpartition add_p_01 values less than( 2 ),subpartition add_p_02 values less than(10));
--step9: 修改二级分区表，split非default一级分区; expect:合理报错
alter table t_subpartition_0276 split partition p_range_1 into  
(partition add_p_01 values less than( 2 ),partition add_p_02 values less than(10));
--step10: 修改二级分区表，split非default二级分区; expect:合理报错
alter table t_subpartition_0276 split subpartition p_range_1_1 into (subpartition add_p_01 values less than( 2 ),subpartition add_p_02 values less than(5));

--test3: alter table  split --指定单个分割点（切割点的大小位于正在被切割的分区的分区键范围内）
--step11: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0276;
create   table if not exists t_subpartition_0276
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0276
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step12: 插入数据; expect:成功
insert into t_subpartition_0276 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0276 values(11,1,1,1),(14,4,4,4),(15,5,5,5),(18,8,8,8),(19,9,9,9);
--step13: 分区键创建索引; expect:成功
create index on t_subpartition_0276(col_1,col_2) local;
--step14: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0276') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0276')) b where a.parentid = b.oid order by a.relname;
--step15: 修改二级分区表，对一级分区split; expect:合理报错
alter table t_subpartition_0276 split partition p_range_1 at(2) into (partition add_p_01 ,partition add_p_02);
--step16: 修改二级分区表，指定多点split; expect:合理报错
alter table t_subpartition_0276 split subpartition p_range_1_1  at(2,4)  into (subpartition add_p_01 ,subpartition add_p_02);
--step17: 修改二级分区表，split单点二级分区; expect:成功
alter table t_subpartition_0276 split subpartition p_range_1_1  at(2)  into (subpartition add_p_01 ,subpartition add_p_02);

--step18: 查询数据; expect:合理报错
select * from t_subpartition_0276 subpartition(p_range_1_1);
--step19: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0276 subpartition(add_p_01);
--step20: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0276 subpartition(add_p_02);

--step21: 修改二级分区表，对split后的分区进行分区; expect:成功
alter table t_subpartition_0276 split subpartition add_p_02  at(4)  into (subpartition add_p_011 ,subpartition add_p_022);
--step22: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0276') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0276')) b where a.parentid = b.oid order by a.relname;

--step23: 查询数据; expect:成功
select * from t_subpartition_0276 subpartition(add_p_01);
--step24: 查询数据; expect:合理报错
select * from t_subpartition_0276 subpartition(add_p_02);
--step25: 查询数据; expect:成功
select * from t_subpartition_0276 subpartition(add_p_011);
--step26: 查询数据; expect:成功
select * from t_subpartition_0276 subpartition(add_p_022);

--step27: 清理环境; expect:成功
drop table if exists t_subpartition_0276;
drop tablespace if exists ts_subpartition_0276;
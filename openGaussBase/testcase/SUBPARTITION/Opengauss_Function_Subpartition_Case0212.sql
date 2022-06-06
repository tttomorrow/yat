-- @testpoint: range_list二级分区表：split,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0212;
drop tablespace if exists ts_subpartition_0212;
create tablespace ts_subpartition_0212 relative location 'subpartition_tablespace/subpartition_tablespace_0212';

--test1: alter table  split 指定值分割
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0212
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0212
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0212 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step4: 修改二级分区表,split一级分区; expect:合理报错
alter table t_subpartition_0212 split partition for (5) at (8) into ( partition add_p_01 , partition add_p_02 );
--step5: 修改二级分区表,split二级分区; expect:合理报错
alter table t_subpartition_0212 split subpartition for (5) at (8) into ( subpartition add_p_01 , subpartition add_p_02 );

--test2: alter table  split 不指定分割点
--step6: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0212;
create table if not exists t_subpartition_0212
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0212
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step7: 修改二级分区表,split非default一级分区值; expect:合理报错
alter table t_subpartition_0212 split partition for (5) into  
(partition add_p_01 values less than( 2 ),partition add_p_02 values less than(10));
--step8: 修改二级分区表,split非default二级分区值; expect:合理报错
alter table t_subpartition_0212 split subpartition for (5) into  
(subpartition add_p_01 values less than( 2 ),subpartition add_p_02 values less than(10));
--step9: 修改二级分区表,split非default一级分区; expect:合理报错
alter table t_subpartition_0212 split partition p_range_1 into  
(partition add_p_01 values less than( 2 ),partition add_p_02 values less than(10));
--step10: 修改二级分区表,split非default二级分区; expect:合理报错
alter table t_subpartition_0212 split subpartition p_list_1_1 into (subpartition add_p_01 values less than( 2 ),subpartition add_p_02 values less than(5));

--test3: alter table  split --指定单个分割点(切割点的大小位于正在被切割的分区的分区键范围内)
--step11: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0212;
create table if not exists t_subpartition_0212
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0212
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step12: 插入数据; expect:成功
insert into t_subpartition_0212 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0212 values(11,1,1,1),(14,4,4,4),(15,5,5,5),(18,8,8,8),(19,9,9,9);
--step13: 分区键创建索引; expect:成功
create index on t_subpartition_0212(col_1,col_2) local;
--step14: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0212') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0212')) b where a.parentid = b.oid order by a.relname;
--step15: 修改二级分区表,对一级分区split; expect:合理报错
alter table t_subpartition_0212 split partition p_range_1 at(2) into (partition add_p_01 ,partition add_p_02);
--step16: 修改二级分区表,指定多点split; expect:合理报错
alter table t_subpartition_0212 split subpartition p_list_1_1  at(2,4) into (subpartition add_p_01 ,subpartition add_p_02);
--step17: 修改二级分区表,指定单点split; expect:合理报错
alter table t_subpartition_0212 split subpartition p_list_1_1  at(2) into (subpartition add_p_01 ,subpartition add_p_02);
--step18: 修改二级分区表,split非default二级分区; expect:合理报错
alter table t_subpartition_0212 split subpartition p_list_1_1  values(4) into (subpartition add_p_01 ,subpartition add_p_02);
--step19: 修改二级分区表,split default二级分区; expect:成功
alter table t_subpartition_0212 split subpartition p_list_1_2  values(4) into (subpartition add_p_01 ,subpartition add_p_02);

--step20: 查询数据; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0212') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0212')) b where a.parentid = b.oid order by a.relname;
--step21: 插入数据; expect:成功
insert into t_subpartition_0212 values(-20,4,4,4);
--step22: 查询指定一级分区数据; expect:成功
select * from t_subpartition_0212 partition(p_range_1);
--step23: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0212 subpartition(add_p_01);
--step24: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0212 subpartition(add_p_02);
--step25: 二级分区键创建索引; expect:成功
create index ind_01 on t_subpartition_0212(col_2) local;
--step26: 查询分区信息; expect:成功,有数据
select relname,parttype,partstrategy,indisusable,interval from pg_partition where relname='p_list_4_1_col_2_idx';

--step27: 插入数据; expect:成功
insert into t_subpartition_0212 values(-20,3,4,4);
--step28: 二级分区键创建索引; expect:成功
select * from t_subpartition_0212 subpartition(add_p_02);

--step29: 清理环境; expect:成功
drop table if exists t_subpartition_0212;
drop tablespace if exists ts_subpartition_0212;
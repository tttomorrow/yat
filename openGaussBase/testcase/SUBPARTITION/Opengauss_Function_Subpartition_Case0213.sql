-- @testpoint: range_list二级分区表：split分割点与所在分区不符/多个分割点,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0213;
drop tablespace if exists ts_subpartition_0213;
create tablespace ts_subpartition_0213 relative location 'subpartition_tablespace/subpartition_tablespace_0213';

--test1: alter table  split --指定多个分割点(切割点的大小位于正在被切割的分区的分区键范围内)
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0213
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0213
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
--step3: 分区键创建索引; expect:成功
create index ind_01 on t_subpartition_0213(col_2) local;
--step4: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0213') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0213')) b where a.parentid = b.oid order by a.relname;
--step5: 修改二级分区表,对二级分区split,和其他分区数据重叠; expect:合理报错
alter table t_subpartition_0213 split subpartition p_list_1_2  values(-1) into (subpartition add_p_01 ,subpartition add_p_02);
--step6: 修改二级分区表,对二级分区split和其他分区数据不重叠; expect:成功
alter table t_subpartition_0213 split subpartition p_list_1_2  values(1,2,3,4,5) into (subpartition add_p_01 ,subpartition add_p_02);

drop table if exists t_subpartition_0213;
create table if not exists t_subpartition_0213
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0213
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
--step7: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0213') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0213')) b where a.parentid = b.oid order by a.relname;
--step8: 插入数据; expect:成功
insert into t_subpartition_0213 values(-20,4,4,4);
--step9: 分区键创建索引; expect:成功
create index ind_01 on t_subpartition_0213(col_1,col_2) local;
--step10: 插入数据; expect:成功
insert into t_subpartition_0213 values(-1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(-19,9,9,9);
insert into t_subpartition_0213 values(1,8,1,1),(4,7,4,4),(5,8,5,5),(8,9,8,8),(9,9,9,9);
--step11: 查询分区信息; expect:成功,有数据
select relname,parttype,partstrategy,indisusable,interval from pg_partition where relname='p_list_4_1_col_1_col_2_idx';

--step12: 修改二级分区表,对二级分区split; expect:合理报错
alter table t_subpartition_0213 split subpartition p_list_1_2  at(5) into (subpartition add_p_01,subpartition add_p_02);
--step13: 修改二级分区表,对非default二级分区split; expect:合理报错
alter table t_subpartition_0213 split subpartition p_list_1_1  values(4,5,6) into (subpartition add_p_01,subpartition add_p_02);
--step14: 修改二级分区表,二级分区split边界数目和分区数据不等; expect:成功
alter table t_subpartition_0213 split subpartition p_list_1_2  values(4,5,6) into (subpartition add_p_01,subpartition add_p_02);
--step15: 修改二级分区表,二级分区split边界数目和分区数据不等; expect:成功
alter table t_subpartition_0213 split subpartition add_p_02  values(7,8) into (subpartition add_p_03,subpartition add_p_04);
--step16: 修改二级分区表,二级分区split边界数目和分区数据相等; expect:成功
alter table t_subpartition_0213 split subpartition add_p_04  values(10) into (subpartition add_p_05,subpartition add_p_06);
--step17: 插入数据; expect:成功
insert into t_subpartition_0213 values(1,10,1,1);
insert into t_subpartition_0213 values(1,11,1,1);
--step18: 查询切割后的二级分区数据; expect:成功
select * from t_subpartition_0213 subpartition(add_p_01);
--step19: 修改二级分区表,多值split; expect:成功
alter table t_subpartition_0213 split subpartition add_p_06  values(13,11,12) into (subpartition add_p_07,subpartition add_p_08);

--test2: alter table  split(分割点与所在分区不符)
--step20: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0213;
create table if not exists t_subpartition_0213
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0213
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
--step21: 插入数据; expect:成功
insert into t_subpartition_0213 values(1,1,1,1),(4,4,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0213 values(11,1,1,1),(14,4,4,4),(15,5,5,5),(18,8,8,8),(19,9,9,9);
--step22: 修改二级分区表,对非default二级分区split; expect:合理报错
alter table t_subpartition_0213 split subpartition p_list_1_1  values(-88888) into (subpartition add_p_011 ,subpartition add_p_022);
--step23: 修改二级分区表,split切割值超出类型范围; expect:合理报错
alter table t_subpartition_0213 split subpartition p_list_1_2  values('15555555555555555555555555555555555555555555555555555555555') into (subpartition t_subpartition_0213,subpartition add_p_011);
--step24: 修改二级分区表,split切割值超出类型范围; expect:成功
alter table t_subpartition_0213 split subpartition p_list_1_2  values(2147483647) into (subpartition t_subpartition_0213,subpartition add_p_011);

--step25: 查询分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0213') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0213')) b where a.parentid = b.oid order by a.relname;
--step26: 插入数据; expect:成功
insert into t_subpartition_0213 values(-11,2147483647,1,1),(-14,2147483645,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0213 values(1,8,1,1),(4,7,4,4),(5,8,5,5),(8,9,8,8),(9,9,9,9);
--step27: 查询切割后二级分区数据; expect:成功
select * from t_subpartition_0213 subpartition(add_p_011);
--step28: 查询切割后二级分区数据; expect:成功
select * from t_subpartition_0213 subpartition(t_subpartition_0213);
--step29: 分区键创建索引; expect:成功
create index ind_01 on t_subpartition_0213(col_1,col_2) local;

--step30: 清理环境; expect:成功
drop table if exists t_subpartition_0213;
drop tablespace if exists ts_subpartition_0213;
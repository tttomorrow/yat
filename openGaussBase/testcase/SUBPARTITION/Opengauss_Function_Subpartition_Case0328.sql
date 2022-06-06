-- @testpoint: range_hash二级分区表：add约束/add分区,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0328;
drop tablespace if exists ts_subpartition_0328;
create tablespace ts_subpartition_0328 relative location 'subpartition_tablespace/subpartition_tablespace_0328';

--test1: alter table add --约束
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0328
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0328
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
	 subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
	subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
	subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 修改二级分区表，添加check约束; expect:成功
alter table t_subpartition_0328 add constraint constraint_check check (col_3 is not null);

--test2: alter table add --分区
--step4: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0328;
create   table if not exists t_subpartition_0328
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0328
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
	 subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
	subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
	subpartition t_subpartition_0328
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step5: 修改二级分区表，添加一级分区，分区值和已有相同; expect:合理报错
alter table t_subpartition_0328 add partition   p_range_10 values less than( 50 );
--step6: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0328;
create   table if not exists t_subpartition_0328
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0328
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
	 subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
	subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
	subpartition t_subpartition_0328
  )
) enable row movement;
--step7: 修改二级分区表，添加一级分区，分区名和分区值和已有相同; expect:合理报错
alter table t_subpartition_0328 add partition   p_range_4 values less than( 50 );

--step8: 清理环境; expect:成功
drop table if exists t_subpartition_0328;
drop tablespace if exists ts_subpartition_0328;
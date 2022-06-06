-- @testpoint: range_range二级分区表：primary key,部分测试点合理报错

--test1: 列约束--primary key index_parameters
--step1: 创建二级分区表，二级分区键包含列约束主键; expect:成功
drop table if exists t_subpartition_00264;
create   table if not exists t_subpartition_0264
(
    col_1 int  ,
    col_2 int  primary key,
	col_3 int ,
    col_4 int   
)
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
--step2: 创建二级分区表，一级分区键包含列约束主键; expect:成功
drop table if exists t_subpartition_00264;
create   table if not exists t_subpartition_0264
(
    col_1 int primary key ,
    col_2 int  ,
	col_3 int ,
    col_4 int   
)
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
insert into t_subpartition_0264 values(1,1,1,1),(5,5,5,5);
--step4: 插入重复数据; expect:合理报错
insert into t_subpartition_0264 values(1,1,1,1),(5,5,5,5);

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0264;
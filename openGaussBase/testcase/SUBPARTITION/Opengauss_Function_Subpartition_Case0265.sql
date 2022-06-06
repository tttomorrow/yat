-- @testpoint: range_range二级分区表列约束(主键)：约束推迟/using index tablespace,部分测试点合理报错

--test1: 列约束--primary key index_parameters 约束推迟
--step1: 创建二级分区表，一级分区键包含列约束主键; expect:成功
drop table if exists t_subpartition_00265;
create   table if not exists t_subpartition_0265
(
    col_1 int primary key  deferrable ,
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

--test2: 列约束--primary key index_parameters using index tablespace
--step2: 创建二级分区表，一级分区键包含列约束主键，using index不同的表空间; expect:成功
drop table if exists t_subpartition_00265;
drop tablespace if exists ts_subpartition_00265;
create tablespace ts_subpartition_00265 relative location 'subpartition_tablespace/subpartition_tablespace_00265';
create  table if not exists t_subpartition_00265
(
    col_1 int primary key using index tablespace ts_subpartition_00265,
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
--step3: 创建二级分区表，普通列包含列约束主键，using index不同的表空间; expect:成功
drop table if exists t_subpartition_00265;
create   table if not exists t_subpartition_0265
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int primary key   using index tablespace ts_subpartition_00265
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

--step4: 清理环境; expect:成功
drop table if exists t_subpartition_0265;
drop tablespace if exists ts_subpartition_0265;
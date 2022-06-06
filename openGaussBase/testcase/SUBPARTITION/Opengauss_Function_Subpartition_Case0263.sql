-- @testpoint: range_range二级分区表：default/unique

--test1: 列约束-- default default_expr
--step1: 创建二级分区表,二级分区键包含列约束default; expect:成功
drop table if exists t_subpartition_00263;
create   table if not exists t_subpartition_0263
(
    col_1 int  ,
    col_2 int  default 20 ,
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
--step2: 插入数据; expect:成功
insert into t_subpartition_0263(col_1,col_3,col_4) values(1,1,1),(5,5,5);
--step3: 查询数据; expect:成功
select * from t_subpartition_0263;
--step4: 查询二级分区数据; expect:成功
select * from t_subpartition_0263 subpartition(p_range_1_2);

--test2: 列约束--unique index_parameters
--step5: 创建二级分区表，二级分区键包含列约束unique index_parameters; expect:成功
drop table if exists t_subpartition_00263;
create   table if not exists t_subpartition_0263
(
    col_1 int  ,
    col_2 int  unique,
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

--test3: 列约束--unique index_parameters
--step6: 创建二级分区表，一级分区键包含列约束unique index_parameters; expect:成功
drop table if exists t_subpartition_00263;
create   table if not exists t_subpartition_0263
(
    col_1 int unique ,
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

--step7: 清理环境; expect:成功
drop table if exists t_subpartition_0263;
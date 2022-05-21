-- @testpoint: range_range二级分区表：null/not null,部分测试点合理报错

--test1: 列约束not null
--step1: 创建二级分区表，二级分区键包含列约束not null; expect:成功
drop table if exists t_subpartition_00262;
create   table if not exists t_subpartition_0261
(
    col_1 int  ,
    col_2 int  not null ,
	col_3 int not null ,
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
--step2: 非空约束列插入空数据; expect:合理报错
insert into t_subpartition_0261(col_1,col_2) values(1,1),(5,5);
--test2: 列约束null
--step3: 创建二级分区表，二级分区键包含列约束null; expect:成功
drop table if exists t_subpartition_00262;
create   table if not exists t_subpartition_0261
(
    col_1 int  ,
    col_2 int  null ,
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
--step4: 空约束列插入空数据; expect:合理报错
insert into t_subpartition_0261(col_1,col_3,col_4) values(1,1,1),(5,5,5);

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0262;
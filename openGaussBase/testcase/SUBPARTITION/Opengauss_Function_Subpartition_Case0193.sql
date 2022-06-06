-- @testpoint: range_list二级分区表：check约束/index_parameters(unique),部分测试点合理报错

--test1: check约束
--step1: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0193;
create   table if not exists t_subpartition_0193
(
    col_1 int  ,
    col_2 int  not null ,
	col_3 int not null ,
    col_4 int   ,
	check (col_1 > col_2 and col_4 is null)
)
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
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
--step2: 插入不符合check约束(col_1 > col_2)的数据; expect:合理报错
insert into t_subpartition_0193 values(1,1,1,1),(5,5,5,5);
--step3: 插入不符合check约束(col_1 > col_2)的数据; expect:合理报错
insert into t_subpartition_0193 values(2,1,1),(5,5,5);
--step4: 插入符合check约束"t_subpartition_0193_check"的数据; expect:成功
insert into t_subpartition_0193 values(2,1,1),(6,5,5);
--step5: 插入不符合check约束(col_4 is null)的数据; expect:合理报错
insert into t_subpartition_0193 values(2,1,1,1),(6,5,5,5);

--test2: index_parameters：unique
--step6: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0193;
create   table if not exists t_subpartition_0193
(
    col_1 int  ,
    col_2 int  not null ,
	col_3 int not null ,
    col_4 int   ,
	unique (col_1,col_2)
)
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_list_1_1 values ( '1','2','3','4','5'),
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
    subpartition p_list_4_1  values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step7: 插入符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0193 values(1,1,1,1),(5,5,5,5);
--step8: 插入不符合(col_1,col_2)唯一约束的数据; expect:合理报错
insert into t_subpartition_0193 values(1,1,1,1),(5,5,5,5);

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0193;
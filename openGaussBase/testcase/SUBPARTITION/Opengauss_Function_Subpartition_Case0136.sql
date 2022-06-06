-- @testpoint: list_hash二级分区表:check约束/index_parameters(unique),部分测试点合理报错

--test1: check约束
--step1: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0136;
create  table if not exists t_subpartition_0136
(
  col_1 int ,
  col_2 int not null ,
    col_3 int not null ,
  col_4 int ,
    check (col_1 > col_2 and col_4 is null)
)
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
 (
  subpartition p_hash_1_1 ,
  subpartition p_hash_1_2 ,
  subpartition p_hash_1_3
 ),
 partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
 (
  subpartition p_hash_2_1 ,
  subpartition p_hash_2_2 ,
  subpartition p_hash_2_3 ,
  subpartition p_hash_2_4 ,
  subpartition p_hash_2_5
 ),
 partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
 partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
 (
  subpartition p_hash_4_1
 ),
 partition p_list_5 values (default)
 (
  subpartition p_hash_5_1
 ),
 partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
 (
  subpartition p_hash_6_1 ,
  subpartition p_hash_6_2 ,
  subpartition p_hash_6_3
 )
) enable row movement ;
--step2: 插入不符合check约束(col_1 > col_2)的数据; expect:合理报错
insert into t_subpartition_0136 values(2,1,1),(5,5,5);
--step3: 插入符合check约束"t_subpartition_0136_check"的数据; expect:成功
insert into t_subpartition_0136 values(2,1,1),(6,5,5);
--step4: 插入不符合check约束(col_4 is null)的数据; expect:合理报错
insert into t_subpartition_0136 values(2,1,1,1),(6,5,5,5);

--test2: index_parameters：unique
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0136;
create  table if not exists t_subpartition_0136
(
  col_1 int ,
  col_2 int not null ,
    col_3 int not null ,
  col_4 int ,
    unique (col_1,col_2)
)
partition by list (col_1) subpartition by hash (col_2)
(
 partition p_list_1 values (-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
 (
  subpartition p_hash_1_1 ,
  subpartition p_hash_1_2 ,
  subpartition p_hash_1_3
 ),
 partition p_list_2 values (1,2,3,4,5,6,7,8,9,10 )
 (
  subpartition p_hash_2_1 ,
  subpartition p_hash_2_2 ,
  subpartition p_hash_2_3 ,
  subpartition p_hash_2_4 ,
  subpartition p_hash_2_5
 ),
 partition p_list_3 values (11,12,13,14,15,16,17,18,19,20),
 partition p_list_4 values (21,22,23,24,25,26,27,28,29,30 )
 (
  subpartition p_hash_4_1
 ),
 partition p_list_5 values (default)
 (
  subpartition p_hash_5_1
 ),
 partition p_list_6 values (31,32,33,34,35,36,37,38,39,40)
 (
  subpartition p_hash_6_1 ,
  subpartition p_hash_6_2 ,
  subpartition p_hash_6_3
 )
) enable row movement ;
--step6: 插入符合(col_1,col_2)唯一约束的数据; expect:成功
insert into t_subpartition_0136 values(1,1,1,1),(5,5,5,5);
--step7: 查询数据; expect:成功
select * from t_subpartition_0136;
--step8: 插入不符合(col_1,col_2)唯一约束的数据; expect:合理报错
insert into t_subpartition_0136 values(1,1,1,1),(5,5,5,5);

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0136;
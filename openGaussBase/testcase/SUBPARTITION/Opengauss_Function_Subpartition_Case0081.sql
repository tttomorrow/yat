-- @testpoint: hash_range二级分区表:null/not null,部分测试点合理报错

--test1: 列约束not null
--step1: 创建二级分区表，二级分区键包含列约束not null; expect:成功
drop table if exists t_subpartition_0081;
create   table if not exists t_subpartition_0081
(
    col_1 int  ,
    col_2 int  not null ,
	col_3 int not null ,
    col_4 int
)
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step2: 非空约束列插入空数据; expect:合理报错
insert into t_subpartition_0081(col_1,col_2) values(1,1),(5,5);

--test2: 列约束null
--step3: 创建二级分区表，二级分区键包含列约束null; expect:成功
drop table if exists t_subpartition_0081;
create   table if not exists t_subpartition_0081
(
    col_1 int  ,
    col_2 int  null ,
	col_3 int ,
    col_4 int
)
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step4: 空约束列插入空数据; expect:成功
insert into t_subpartition_0081(col_1,col_3,col_4) values(1,1,1),(5,5,5);
--step5: 查询全部数据; expect:成功，2条数据
select * from t_subpartition_0081;
--step6: 查询二级分区数据; expect:成功，2条数据
select * from t_subpartition_0081 subpartition(p_list_2_subpartdefault1);
--step7: 空约束列插入非空数据; expect:成功
insert into t_subpartition_0081(col_2,col_3,col_4) values(1,1,1),(5,5,5);
--step8: 查询全部数据; expect:成功，4条数据
select * from t_subpartition_0081;
--step9: 查询二级分区数据; expect:成功，2条数据
select * from t_subpartition_0081 subpartition(p_list_7_subpartdefault1);

--step10:清理环境; expect:成功
drop table if exists t_subpartition_0081;
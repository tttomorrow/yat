-- @testpoint: list_list二级分区表列约束:null/not null,部分测试点合理报错

--test1: 列约束not null
--step1: 创建二级分区表，二级分区键包含列约束not null; expect:成功
drop table if exists t_subpartition_0023;
create   table if not exists t_subpartition_0023
(
    col_1 int  ,
    col_2 int  not null ,
	col_3 int not null ,
    col_4 int
)
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values ( 0,-1,-2,-3,-4,-5,-6,-7,-8,-9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9)
  (
    subpartition p_list_2_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_2_2 values ( default ),
	subpartition p_list_2_3 values ( 10,11,12,13,14,15,16,17,18,19),
	subpartition p_list_2_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
	subpartition p_list_2_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19)
  (
    subpartition p_list_3_2 values ( default )
  ),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29)
  (
    subpartition p_list_5_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_5_2 values ( default ),
	subpartition p_list_5_3 values ( 10,11,12,13,14,15,16,17,18,19),
	subpartition p_list_5_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
	subpartition p_list_5_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39),
  partition p_list_7 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_7_1 values ( default )
  )
) enable row movement;
--step2: 非空约束列插入空数据; expect:合理报错
insert into t_subpartition_0023(col_1,col_2) values(1,1),(5,5);

--test2: 列约束null
--step3: 创建二级分区表，二级分区键包含列约束null; expect:成功
drop table if exists t_subpartition_0023;
create   table if not exists t_subpartition_0023
(
    col_1 int  ,
    col_2 int  null ,
	col_3 int ,
    col_4 int
)
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values ( 0,-1,-2,-3,-4,-5,-6,-7,-8,-9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9)
  (
    subpartition p_list_2_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_2_2 values ( default ),
	subpartition p_list_2_3 values ( 10,11,12,13,14,15,16,17,18,19),
	subpartition p_list_2_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
	subpartition p_list_2_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19)
  (
    subpartition p_list_3_2 values ( default )
  ),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29)
  (
    subpartition p_list_5_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_5_2 values ( default ),
	subpartition p_list_5_3 values ( 10,11,12,13,14,15,16,17,18,19),
	subpartition p_list_5_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
	subpartition p_list_5_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39),
  partition p_list_7 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_7_1 values ( default )
  )
) enable row movement;
--step4: 空约束列插入空数据; expect:成功
insert into t_subpartition_0023(col_1,col_3,col_4) values(1,1,1),(5,5,5);
--step5: 查询全部数据; expect:成功，2条数据
select * from t_subpartition_0023;
--step6: 查询二级分区数据; expect:成功，2条数据
select * from t_subpartition_0023 subpartition(p_list_2_2);
--step7: 空约束列插入非空数据; expect:成功
insert into t_subpartition_0023(col_2,col_3,col_4) values(1,1,1),(5,5,5);
--step8: 查询全部数据; expect:成功，4条数据
select * from t_subpartition_0023;
--step9: 查询二级分区数据; expect:成功，2条数据
select * from t_subpartition_0023 subpartition(p_list_4_subpartdefault1);

--step10: 删除表; expect:成功
drop table if exists t_subpartition_0023;
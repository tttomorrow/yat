-- @testpoint: list_list二级分区表修改：add字段/drop字段/add约束,部分测试点合理报错

--test1: alter table add/drop --字段
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0041;
drop tablespace if exists ts_subpartition_0041;
create tablespace ts_subpartition_0041 relative location 'subpartition_tablespace/subpartition_tablespace_0041';
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0041
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0041
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
--step3: 修改二级分区表，添加列; expect:成功
alter table t_subpartition_0041 add column col_5 int;
--step4: 插入数据; expect:成功
insert into t_subpartition_0041 values(1,8,1,1,1),(4,7,4,4,4),(5,8,5,5,5),(8,9,8,8,8),(9,9,9,9,9);
--step5: 查询二级分区数据; expect:成功，5条数据
select * from t_subpartition_0041 subpartition(p_list_2_1);
--step6: 修改二级分区表，清空指定二级分区数据; expect:成功
alter table t_subpartition_0041 truncate subpartition p_list_2_1;
--step7: 查询二级分区数据数据; expect:成功，0条数据
select * from t_subpartition_0041 subpartition(p_list_2_1);
--step8: 插入数据; expect:成功
insert into t_subpartition_0041 values(1,8,1,1,1),(4,7,4,4,4),(5,8,5,5,5),(8,9,8,8,8),(9,9,9,9,9);
--step9: 修改二级分区表，删除列; expect:成功
alter table t_subpartition_0041 drop column col_5 ;
--step10: 查询数据; expect:成功，4列
select * from t_subpartition_0041 subpartition(p_list_2_1);

--test2: alter table add --约束
--step11: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0041;
create table if not exists t_subpartition_0041
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0041
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
--step12: 修改二级分区表，添加check约束; expect:成功
alter table t_subpartition_0041 add constraint constraint_check check (col_3 is not null);
--step13: 插入违反check约束(col_3)的数据; expect:合理报错
insert into t_subpartition_0041 values(1,8);
--step14: 插入正确的数据; expect:成功
insert into t_subpartition_0041 values(4,7,4,4),(5,8,5,5),(8,9,8,8),(9,9,9,9);

--step15: 删除表; expect:成功
drop table if exists t_subpartition_0041;
drop tablespace if exists ts_subpartition_0041;
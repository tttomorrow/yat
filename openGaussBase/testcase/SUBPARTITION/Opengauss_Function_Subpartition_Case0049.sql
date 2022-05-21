-- @testpoint: list_list二级分区表：truncate,部分测试点合理报错

--test1: truncate  table
--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0049;
drop tablespace if exists ts_subpartition_0049;
create tablespace ts_subpartition_0049 relative location 'subpartition_tablespace/subpartition_tablespace_0049';
--step2: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0049;
create table if not exists t_subpartition_0049
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0049
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0049 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step4: 查询表数据; expect:成功
select * from t_subpartition_0049;
--step5: 清空表数据; expect:成功
truncate t_subpartition_0049;
--step6: 查询数据; expect:成功，0条数据
select * from t_subpartition_0049;
--step7: 查询二级分区数据; expect:成功，0条数据
select * from t_subpartition_0049 subpartition(p_list_1_1);

--test2: truncate  partition
--step8: 插入数据; expect:成功
insert into t_subpartition_0049 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0049 values(11,11,1,1),(15,15,5,5),(18,81,8,8),(29,9,9,9);
insert into t_subpartition_0049 values(21,11,1,1),(15,15,5,5),(18,81,8,8),(-29,31,9,9);
insert into t_subpartition_0049 values(-1,1,1,1),(-1,-15,5,5),(-8,7,8,8),(-9,29,9,9);
insert into t_subpartition_0049 values(-8,18,1);
insert into t_subpartition_0049 values(8,38,1);
--step9: 查询指定一级分区数据; expect:成功，5条数据
select * from t_subpartition_0049 partition(p_list_1);
--step10: 查询指定一级数据; expect:成功，5条数据
select * from t_subpartition_0049 partition(p_list_2);
--step11: 清空指定一级分区数据; expect:成功
alter table t_subpartition_0049 truncate partition p_list_1;
--step12: 清空指定一级分区数据; expect:成功
alter table t_subpartition_0049 truncate partition p_list_2;
--step13: 查询指定一级分区数据; expect:成功，0条数据
select * from t_subpartition_0049 partition(p_list_1);
--step14: 查询指定一级分区数据; expect:成功，0条数据
select * from t_subpartition_0049 partition(p_list_2);
--step15: 查询表数据; expect:成功，8条数据
select * from t_subpartition_0049;

--test3: truncate  subpartition
--step16: 清空指定两个二级分区数据; expect:合理报错
alter table t_subpartition_0049 truncate subpartition p_list_1,p_list_2;
--step17: 查询二级分区数据; expect:成功，1条数据
select * from t_subpartition_0049 subpartition(p_list_5_3);
--step18: 清空指定二级分区数据; expect:成功
alter table t_subpartition_0049 truncate subpartition p_list_5_3;
--step19: 查询数据; expect:成功，0条数据
select * from t_subpartition_0049 subpartition(p_list_5_3);

--step20: 删除表; expect:成功
drop table if exists t_subpartition_0049;
drop tablespace if exists ts_subpartition_0049;
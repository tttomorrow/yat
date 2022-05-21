-- @testpoint: list_list二级分区表：insert on duplicate key update,部分测试点合理报错

--test1: insert --insert  on duplicate key update -唯一索引
drop table if exists t_subpartition_0046;
drop tablespace if exists ts_subpartition_0046;
create tablespace ts_subpartition_0046 relative location 'subpartition_tablespace/subpartition_tablespace_0046';
--step1: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0046
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0046
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
--step2: 分区键创建唯一索引; expect:成功
create unique index on t_subpartition_0046(col_1,col_2);
--step3: 插入数据; expect:成功
insert into t_subpartition_0046 values(1,11,1,1);
--step4: 插入数据,指定on duplicate key update nothing; expect:成功
insert into t_subpartition_0046 values(1,11,1,1) on duplicate key update nothing;
--step5: 查询数据; expect:成功，一条数据
select * from t_subpartition_0046 subpartition (p_list_2_3);
--step6: 插入重复数据; expect:合理报错
insert into t_subpartition_0046 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step7: 插入不重复数据; expect:成功
insert into t_subpartition_0046 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step8: 查询数据; expect:成功,3条数据
select * from t_subpartition_0046 subpartition (p_list_2_2);
--step9: 插入重复数据更新一级分区键; expect:合理报错
insert into t_subpartition_0046 values(1,11,1,1) on duplicate key update col_1=10;
--step10: 插入重复数据更新二级分区键; expect:合理报错
insert into t_subpartition_0046 values(1,11,1,1) on duplicate key update col_2=10;
--step11: 插入重复数据更新普通列; expect:成功
insert into t_subpartition_0046 values(1,11,1,1) on duplicate key update col_3=10;
--step12: 查询数据; expect:成功，2条数据
select * from t_subpartition_0046 subpartition (p_list_2_3);

--test2: insert --insert  on duplicate key update -local索引
--step13: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0046;
create table if not exists t_subpartition_0046
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0046
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
--step14: 分区键创建local索引; expect:成功
create index on t_subpartition_0046(col_1) local;
--step15: 插入数据; expect:成功
insert into t_subpartition_0046 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step16: 查询数据; expect:成功，2条数据
select * from t_subpartition_0046 subpartition (p_list_2_3);
--step17: 插入重复数据更新一级分区键; expect:成功
insert into t_subpartition_0046 values(1,11,1,1) on duplicate key update col_1=10;
--step18: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0046 values(1,11,1,1) on duplicate key update col_2=10;
--step19: 插入重复数据更新一级分区键换二级分区; expect:成功
insert into t_subpartition_0046 values(1,11,1,1) on duplicate key update col_2=1;
--step20: 查询数据; expect:成功，2条数据
select * from t_subpartition_0046 subpartition (p_list_2_2) where col_2<55;

--step21: 清理环境; expect:成功
drop table if exists t_subpartition_0046;
drop tablespace if exists ts_subpartition_0046;
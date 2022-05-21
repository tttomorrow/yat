-- @testpoint: list_list二级分区表修改：split,测试点合理报错

--test1: alter table  split
--step1: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0040;
drop tablespace if exists ts_subpartition_0040;
create tablespace ts_subpartition_0040 relative location 'subpartition_tablespace/subpartition_tablespace_0040';
create table if not exists t_subpartition_0040
(
    col_1 int ,
    col_2 int ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0040
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
--step2: 插入数据; expect:成功
insert into t_subpartition_0040 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step3: 修改二级分区表，split一级分区; expect:合理报错
alter table t_subpartition_0040 split partition for (5) at (8) into ( partition add_p_01 , partition add_p_02 );
--step4: 修改二级分区表，split二级分区; expect:合理报错
alter table t_subpartition_0040 split subpartition for (5) at (8) into ( subpartition add_p_01 , subpartition add_p_02 );

--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0040;
create table if not exists t_subpartition_0040
(
    col_1 int ,
    col_2 int ,
	col_3 int ,
    col_4 int
)
tablespace ts_subpartition_0040
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
--step6: 插入数据; expect:成功
insert into t_subpartition_0040 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step7: 修改二级分区表，split非default二级分区; expect:合理报错
alter table t_subpartition_0040 split subpartition p_list_2_1 values(8) into ( subpartition add_p_01 , subpartition add_p_02 );
--step8: 插入数据; expect:成功
drop index if exists index_01;
create index index_01 on t_subpartition_0040(col_2);
--step9: split分区更新索引; expect:成功
alter table t_subpartition_0040 split subpartition p_list_4_subpartdefault1 values(100,200) into ( subpartition add_p_01 , subpartition add_p_02 ) update global index;
--step10: 查看执行计划; expect:成功
explain analyze  select * from t_subpartition_0040 where col_2 in  (select col_1 from t_subpartition_0040 subpartition(p_list_2_2) where col_1 >10);
explain analyze  select /*+ indexscan(t_subpartition_0040 index_01)*/  * from t_subpartition_0040 where col_2 in  (select col_1 from t_subpartition_0040 subpartition(p_list_2_2) where col_1 >10);

--step11: 删除表; expect:成功
drop table if exists t_subpartition_0040;
drop tablespace if exists ts_subpartition_0040;
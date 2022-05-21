-- @testpoint: list_hash二级分区表修改：split,测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0155;
drop tablespace if exists ts_subpartition_0155;
create tablespace ts_subpartition_0155 relative location 'subpartition_tablespace/subpartition_tablespace_0155';

--test1: alter table  split
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0155
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0155
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0155 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step4: 修改二级分区表,split一级分区; expect:合理报错
alter table t_subpartition_0155 split partition for (5) at (8) into ( partition add_p_01 , partition add_p_02 );
--step5: 修改二级分区表,split二级分区; expect:合理报错
alter table t_subpartition_0155 split subpartition for (5) at (8) into ( subpartition add_p_01 , subpartition add_p_02 );

--step6: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0155;
create table if not exists t_subpartition_0155
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0155
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
--step7: 插入数据; expect:成功
insert into t_subpartition_0155 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step8: 修改二级分区表,split非default二级分区; expect:合理报错
alter table t_subpartition_0155 split subpartition p_hash_4_1 at(8) into ( subpartition add_p_01 , subpartition add_p_02 );

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0155;
drop tablespace if exists ts_subpartition_0155;
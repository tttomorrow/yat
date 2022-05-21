-- @testpoint: range_hash二级分区表：split/add字段/drop字段,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0327;
drop tablespace if exists ts_subpartition_0327;
create tablespace ts_subpartition_0327 relative location 'subpartition_tablespace/subpartition_tablespace_0327';
--test1: alter table  split 一级分区和二级分区
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0327
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0327
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
	 subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
	subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
	subpartition t_subpartition_0327
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0327 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step4: 修改二级分区表，split一级分区; expect:合理报错
alter table t_subpartition_0327 split partition for (5) at (8) into ( partition add_p_01 , partition add_p_02 );
--step5: 修改二级分区表，split二级分区; expect:合理报错
alter table t_subpartition_0327 split subpartition for (5) at (8) into ( subpartition add_p_01 , subpartition add_p_02 );


--test2: alter table  split --hash二级分区不支持分割
--step6: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0327;
create   table if not exists t_subpartition_0327
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0327
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
	 subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
	subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
	subpartition t_subpartition_0327
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step7: 插入数据; expect:成功
insert into t_subpartition_0327 values(1,1,1,1),(5,5,5,5),(8,8,8,8),(9,9,9,9);
--step8: 修改二级分区表，分割hash分区; expect:合理报错
alter table t_subpartition_0327 split subpartition p_hash_3_3 at(8) into ( subpartition add_p_01 , subpartition add_p_02 );

--test3: alter table add/drop --字段
--step9: 创建表空间; expect:成功
drop table if exists t_subpartition_0327;
create   table if not exists t_subpartition_0327
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0327
partition by range (col_1) subpartition by hash (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_hash_1_1 ,
    subpartition p_hash_1_2 ,
	 subpartition p_hash_1_3
  ),
  partition p_range_2 values less than( 20 ),
  partition p_range_3 values less than( 30)
  (
    subpartition p_hash_3_1 ,
    subpartition p_hash_3_2 ,
	subpartition p_hash_3_3
  ),
    partition p_range_4 values less than( 50)
  (
    subpartition p_hash_4_1 ,
    subpartition p_hash_4_2 ,
	subpartition t_subpartition_0327
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step10: 修改二级分区表，添加列; expect:成功
alter table t_subpartition_0327 add column col_5 int;
--step11: 插入数据; expect:成功
insert into t_subpartition_0327 values(1,8,1,1,1),(4,7,4,4,4),(5,8,5,5,5),(8,9,8,8,8),(9,9,9,9,9); 
 --step12: 查询数据; expect:成功，5列数据
select * from t_subpartition_0327 subpartition(p_range_2_subpartdefault1);
--step13: 修改二级分区表，删除列; expect:成功
alter table t_subpartition_0327 drop column col_5 ;
--step14: 查询数据; expect:成功，4列数据
select * from t_subpartition_0327 subpartition(p_range_2_subpartdefault1);
 
--step15: 清理环境; expect:成功
drop table if exists t_subpartition_0327;
drop tablespace if exists ts_subpartition_0327;
-- @testpoint: range_hash二级分区表：drop约束/drop分区键和非分区键/drop分区,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0329;
drop tablespace if exists ts_subpartition_0329;
create tablespace ts_subpartition_0329 relative location 'subpartition_tablespace/subpartition_tablespace_0329';

--test1: alter table drop --约束
--step2: 创建二级分区表; expect:成功
create   table if not exists t_subpartition_0329
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
	check (col_4 is not null)
)tablespace ts_subpartition_0329
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
	subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:合理报错
insert into t_subpartition_0329 values(1,1,1,null);
--step4: 修改二级分区表，删除约束; expect:成功
alter table t_subpartition_0329 drop  constraint t_subpartition_0329_col_4_check;
--step5: 插入数据; expect:成功
insert into t_subpartition_0329 values(1,1,1,null);

--test2: alter table drop --字段（分区键和非分区键）
--step6: 创建表空间; expect:成功
drop table if exists t_subpartition_0329;
create   table if not exists t_subpartition_0329
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0329
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
	subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step7: 插入数据; expect:成功
insert into t_subpartition_0329 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step8: 修改二级分区表，删除非分区键; expect:成功
alter table t_subpartition_0329 drop column col_4;
--step9: 修改二级分区表，删除分区键; expect:合理报错
alter table t_subpartition_0329 drop column col_1;

--test3: alter table drop --分区
--step10: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0329;
create   table if not exists t_subpartition_0329
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0329
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
	subpartition t_subpartition_0329
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step11: 插入数据; expect:成功
insert into t_subpartition_0329 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step12: 修改二级分区表，删除一级分区; expect:成功
alter table t_subpartition_0329 drop partition p_range_1;
--step13: 修改二级分区表，删除二级分区; expect:合理报错
alter table t_subpartition_0329 drop subpartition p_list_2_1;
 
--step14: 清理环境; expect:成功
drop table if exists t_subpartition_0329;
drop tablespace if exists ts_subpartition_0329;
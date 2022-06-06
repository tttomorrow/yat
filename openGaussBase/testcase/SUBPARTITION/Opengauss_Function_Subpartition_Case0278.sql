-- @testpoint: range_range二级分区表：add分区/drop约束/drop分区键和非分区键/drop分区,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0278;
drop tablespace if exists ts_subpartition_0278;
create tablespace ts_subpartition_0278 relative location 'subpartition_tablespace/subpartition_tablespace_0278';

--test1: alter table add --分区
--step2: 创建表空间; expect:成功
create   table if not exists t_subpartition_0278
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0278
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step3: 修改二级分区表，添加一级分区; expect:成功
alter table t_subpartition_0278 add partition   p_range_4 values less than( 40 );

--test2: alter table drop --约束
--step4: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0278;
create   table if not exists t_subpartition_0278
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
	check (col_4 is not null)
)tablespace ts_subpartition_0278
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step5: 插入数据; expect:合理报错
insert into t_subpartition_0278 values(1,1,1,null);
--step6: 修改二级分区表，删除约束; expect:成功
alter table t_subpartition_0278 drop  constraint t_subpartition_0278_col_4_check;
--step7: 插入数据; expect:成功
insert into t_subpartition_0278 values(1,1,1,null);
 
--test3: alter table drop --字段（分区键和非分区键）
--step8: 创建表空间; expect:成功
drop table if exists t_subpartition_0278;
create   table if not exists t_subpartition_0278
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0278
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step9: 插入数据; expect:成功
insert into t_subpartition_0278 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step10: 修改二级分区表，删除非分区键; expect:成功
alter table t_subpartition_0278 drop column col_4;
--step11: 修改二级分区表，删除一级分区键; expect:合理报错
alter table t_subpartition_0278 drop column col_1;
--step12: 修改二级分区表，删除二级分区键; expect:合理报错
alter table t_subpartition_0278 drop column col_2;

--test4: alter table drop --分区
--step13: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0278;
create   table if not exists t_subpartition_0278
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0278
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step14: 插入数据; expect:成功
insert into t_subpartition_0278 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step15: 修改二级分区表，删除一级分区; expect:成功
alter table t_subpartition_0278 drop partition p_range_1;
--step16: 修改二级分区表，删除二级分区; expect:成功
alter table t_subpartition_0278 drop subpartition p_range_2_1;

--step17: 清理环境; expect:成功
drop table if exists t_subpartition_0278;
drop tablespace if exists ts_subpartition_0278;
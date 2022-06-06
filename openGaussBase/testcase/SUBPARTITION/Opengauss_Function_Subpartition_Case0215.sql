-- @testpoint: range_list二级分区表表修改：add分区/drop约束,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0215;
drop tablespace if exists ts_subpartition_0215;
create tablespace ts_subpartition_0215 relative location 'subpartition_tablespace/subpartition_tablespace_0215';

--test1: alter table add --分区
--step2: 创建表空间; expect:成功
create table if not exists t_subpartition_0215
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0215
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 修改二级分区表,添加非list一级分区; expect:合理报错
alter table t_subpartition_0215 add partition   p_range_10 values less than( 50 );

--step4: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0215;
create table if not exists t_subpartition_0215
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0215
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  )
) enable row movement;
--step5: 修改二级分区表,添加一级分区和原有分区名重复; expect:合理报错
 alter table t_subpartition_0215 add partition   p_range_4 values less than( 50 );

--test2: alter table drop --约束
--step6: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0215;
create table if not exists t_subpartition_0215
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
    check (col_4 is not null)
)tablespace ts_subpartition_0215
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step7: 插入数据; expect:合理报错
insert into t_subpartition_0215 values(1,1,1,null);
--step8: 修改二级分区表,删除约束; expect:成功
alter table t_subpartition_0215 drop  constraint t_subpartition_0215_col_4_check;
--step9: 插入数据; expect:成功
insert into t_subpartition_0215 values(1,1,1,null);

--step10: 清理环境; expect:成功
drop table if exists t_subpartition_0215;
drop tablespace if exists ts_subpartition_0215;
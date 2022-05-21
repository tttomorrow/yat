-- @testpoint: range_range二级分区表：分区键多个或相同/表达式,测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0273;
drop tablespace if exists ts_subpartition_0273;
create tablespace ts_subpartition_0273 relative location 'subpartition_tablespace/subpartition_tablespace_0273';

--test1: 分区键 --一级分区指定多个
--step2: 创建二级分区表,二级分区键指定多个; expect:合理报错
drop table if exists t_subpartition_0273;
create   table if not exists t_subpartition_0273
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0273
partition by range (col_1) subpartition by range ( col_2,col_3)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition t_subpartition_0273 values less than( 10 )
  )
) enable row movement;
--step3: 创建二级分区表,一级分区键与二级分区键相同; expect:合理报错
drop table if exists t_subpartition_0273;
create   table if not exists t_subpartition_0273
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0273
partition by range (col_1) subpartition by range ( col_1)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 10 ),
    subpartition p_range_2_2 values less than( 20 )
  ),
    partition p_range_3 values less than( 30 )
  (
    subpartition p_range_3_1 values less than( 20 ),
    subpartition p_range_3_2 values less than( 30 )
  )
) enable row movement;
--step4: 创建二级分区表,一级分区键为表达式; expect:合理报错
drop table if exists t_subpartition_0273;
create   table if not exists t_subpartition_0273
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0273
partition by range (col_1 + 1) subpartition by range (col_1)
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

--step5: 清理环境; expect:成功
drop table if exists t_subpartition_0273;
drop tablespace if exists ts_subpartition_0273;
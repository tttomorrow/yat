-- @testpoint: range_hash二级分区表：分区键多个/相同/表达式,测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0323;
drop tablespace if exists ts_subpartition_0323;
create tablespace ts_subpartition_0323 relative location 'subpartition_tablespace/subpartition_tablespace_0323';

--test1: 分区键 --一级分区指定多个
--step2: 创建二级分区表,一级分区键指定多个; expect:合理报错
drop table if exists t_subpartition_0323;
create   table if not exists t_subpartition_0323
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0323
partition by range (col_1,col_4) subpartition by hash (col_2)
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
	subpartition t_subpartition_0323
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--test2: 分区键 --二级分区指定多个
--step3: 创建二级分区表,一级分区键指定多个; expect:合理报错
drop table if exists t_subpartition_0323;
create   table if not exists t_subpartition_0323
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0323
partition by range (col_1,col_4) subpartition by hash (col_2,col_3)
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
	subpartition t_subpartition_0323
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--test3: 分区键 --一级分区键与二级分区键相同
--step4: 创建二级分区表,一级分区键与二级分区键相同; expect:合理报错
drop table if exists t_subpartition_0323;
create   table if not exists t_subpartition_0323
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0323
partition by range (col_1) subpartition by hash (col_1)
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
	subpartition t_subpartition_0323
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--test4: 分区键 --分区键为表达式--不支持
--step5: 创建二级分区表,分区键为表达式; expect:合理报错
drop table if exists t_subpartition_0323;
create   table if not exists t_subpartition_0323
(
    col_1 int ,
    col_2 int  ,
	col_3 int ,
    col_4 int 
)
tablespace ts_subpartition_0323
partition by range (upper(col_1)) subpartition by hash (col_2)
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
	subpartition t_subpartition_0323
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--step6: 清理环境; expect:成功
drop table if exists t_subpartition_0323;
drop tablespace if exists ts_subpartition_0323;
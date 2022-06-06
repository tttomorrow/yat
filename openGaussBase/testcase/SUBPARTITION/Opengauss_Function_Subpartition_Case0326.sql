-- @testpoint: range_hash二级分区表：local/global/unlogged,测试点合理报错

--step1: 创建二级分区表,指定local; expect:合理报错
drop table if exists t_subpartition_0326;
create local temp table t_subpartition_0326
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
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
	subpartition t_subpartition_0326
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step2: 创建二级分区表,指定global; expect:合理报错
drop table if exists t_subpartition_0326;
create global temp table t_subpartition_0326
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
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
	subpartition t_subpartition_0326
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 创建二级分区表,指定unlogged; expect:合理报错
drop table if exists t_subpartition_0326;
create unlogged table t_subpartition_0326
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
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
	subpartition t_subpartition_0326
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--step4: 清理环境; expect:成功
drop table if exists t_subpartition_0326;
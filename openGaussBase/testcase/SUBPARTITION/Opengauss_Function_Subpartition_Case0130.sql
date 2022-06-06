-- @testpoint: list_range二级分区表：索引,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0130;
drop tablespace if exists ts_subpartition_0130;
create tablespace ts_subpartition_0130 relative location 'subpartition_tablespace/subpartition_tablespace_0130';
--test1: 索引
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0130
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0130
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
    subpartition t_subpartition_0130
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 一级分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0130;
create unique index i_subpartition_0130 on t_subpartition_0130(col_1);
--step4: 二级分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0130;
create unique index i_subpartition_0130 on t_subpartition_0130(col_2);
--step5: 2个分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0130;
create unique index i_subpartition_0130 on t_subpartition_0130(col_1,col_2);
--step6: 同一列存在local索引,创建global索引; expect:合理报错
create unique index i_subpartition_0130 on t_subpartition_0130(col_1,col_2) global;
--step7: 分区键创建local唯一索引; expect:合理报错
drop index if exists i_subpartition_0130;
create unique index on t_subpartition_0130(col_1) local;
--step8: 分区键创建global索引; expect:成功
drop index if exists i_subpartition_0130_01;
create unique index i_subpartition_0130_01 on t_subpartition_0130(col_1) global;
--step9: 删除索引; expect:成功
drop index if exists i_subpartition_0130;
drop index if exists i_subpartition_0130_01;

--step10: 删除表和表空间; expect:成功
drop table if exists t_subpartition_0130;
drop tablespace if exists ts_subpartition_0130;
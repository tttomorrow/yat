-- @testpoint: list_hash二级分区表：索引,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0187;
drop tablespace if exists ts_subpartition_0187;
create tablespace ts_subpartition_0187 relative location 'subpartition_tablespace/subpartition_tablespace_0187';
--test1: 索引
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0187
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0187
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
create unique index i_subpartition_0187 on t_subpartition_0187(col_1);
--step3: 二级分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0187;
create unique index i_subpartition_0187 on t_subpartition_0187(col_2);
--step4: 2个分区键创建唯一索引; expect:成功
drop index if exists i_subpartition_0187;
create unique index i_subpartition_0187 on t_subpartition_0187(col_1,col_2);
--step5: 同一列存在local索引,创建global索引; expect:合理报错
create unique index i_subpartition_0187 on t_subpartition_0187(col_1,col_2) global;
--step6: 分区键创建local唯一索引; expect:合理报错
drop index if exists i_subpartition_0187;
create unique index on t_subpartition_0187(col_1) local;
--step7: 分区键创建global索引; expect:成功
drop index if exists i_subpartition_0187_01;
create unique index i_subpartition_0187_01 on t_subpartition_0187(col_1) global;
--step8: 删除索引; expect:成功
drop index if exists i_subpartition_0187;
drop index if exists i_subpartition_0187_01;

--step9: 删除表和表空间; expect:成功
drop table if exists t_subpartition_0187;
drop tablespace if exists ts_subpartition_0187;
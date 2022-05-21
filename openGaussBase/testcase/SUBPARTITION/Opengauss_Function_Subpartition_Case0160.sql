-- @testpoint: list_hash二级分区表修改：modify_clause/exchange/merge into/move,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0160;
drop tablespace if exists ts_subpartition_0160;
create tablespace ts_subpartition_0160 relative location 'subpartition_tablespace/subpartition_tablespace_0160';

--test1: alter table modify_clause
--step2: 创建表空间; expect:成功
create table if not exists t_subpartition_0160
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
    check (col_4 is not null)
)tablespace ts_subpartition_0160
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
--step3: 分区键创建唯一索引; expect:成功
 create unique index on t_subpartition_0160(col_1,col_2)  ;
--step4: 修改指定一级分区索引不可用; expect:合理报错
 alter table t_subpartition_0160 modify partition p_list_5 unusable local indexes;

--test2: alter table exchange
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0160;
create table if not exists t_subpartition_0160
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
    check (col_4 is not null)
)tablespace ts_subpartition_0160
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
--step6: 创建普通表; expect:成功
drop table if exists t_subpartition_0160_01;
create table if not exists t_subpartition_0160_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
    check (col_4 is not null)
)tablespace ts_subpartition_0160;
--step7: 普通表插入数据; expect:成功
insert into t_subpartition_0160_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step8: 把普通表的数据迁移到二级分区表; expect:合理报错
alter table t_subpartition_0160 exchange partition (p_list_5) with table t_subpartition_0160_01 without validation;
--step9: 查询数据; expect:成功,0条数据
select * from t_subpartition_0160;
--step10: 查询数据; expect:成功
select * from t_subpartition_0160_01;

--test3: alter table  merge into
--step11: 修改二级分区表,把多个一级分区合并为一个一级分区; expect:合理报错
alter table t_subpartition_0160 merge partitions p_hash_1,p_hash_2 into partition p_range_8;

--test4: alter table  move
--step12: 创建表空间; expect:成功
drop tablespace if exists ts_subpartition_0160_01;
create tablespace ts_subpartition_0160_01 relative location 'subpartition_tablespace/subpartition_tablespace_0160_01';
--step13: 修改二级分区表,移动一级分区到新的表空间; expect:合理报错
alter table t_subpartition_0160 move partition p_list_5 tablespace startend_tbs3;

--step14: 清理环境; expect:成功
drop table if exists t_subpartition_0160;
drop table if exists t_subpartition_0160_01;
drop tablespace if exists ts_subpartition_0160;
drop tablespace if exists ts_subpartition_0160_01;
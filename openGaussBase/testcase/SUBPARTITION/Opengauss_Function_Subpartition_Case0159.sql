-- @testpoint: list_hash二级分区表修改：rename约束/字段/分区/表,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0159;
drop tablespace if exists ts_subpartition_0159;
create tablespace ts_subpartition_0159 relative location 'subpartition_tablespace/subpartition_tablespace_0159';

--test1: alter table rename --约束
--step2: 创建表空间; expect:成功
create table if not exists t_subpartition_0159
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
    check (col_4 is not null)
)tablespace ts_subpartition_0159
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
--step3: 修改二级分区表,重命名约束; expect:成功
alter table t_subpartition_0159 rename  constraint t_subpartition_0159_col_4_check to drop_check;
--step4: 插入数据; expect:合理报错
insert into t_subpartition_0159 values(1,1,1,null);

--test2: alter table rename --字段
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0159;
create table if not exists t_subpartition_0159
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
    check (col_4 is not null)
)tablespace ts_subpartition_0159
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
--step6: 修改二级分区表,重命名非分区键; expect:成功
alter table t_subpartition_0159 rename column col_4 to col_4444;
--step7: 修改二级分区表,重命名分区键; expect:成功
alter table t_subpartition_0159 rename column col_2 to col_22222;
--step8: 原二级分区键创建唯一索引; expect:合理报错
create unique index on t_subpartition_0159(col_2);

--test3: alter table rename --分区
--step9: 修改二级分区表,重命名一级分区; expect:合理报错
alter table t_subpartition_0159 rename partition p_range_2 to p_range_2_2222222;
--step10: 查看分区数据; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0159') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0159')) b where a.parentid = b.oid order by a.relname;

--test4: alter table rename --表
--step11: 修改二级分区表,重命名二级分区表; expect:合理报错
alter table t_subpartition_0159 rename to hahahahahah;

--step12: 清理环境; expect:成功
drop table if exists t_subpartition_0159;
drop tablespace if exists ts_subpartition_0159;
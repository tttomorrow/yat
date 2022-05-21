-- @testpoint: list_hash二级分区表修改：add字段/drop字段/add约束,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0156;
drop tablespace if exists ts_subpartition_0156;
create tablespace ts_subpartition_0156 relative location 'subpartition_tablespace/subpartition_tablespace_0156';

--test1: alter table add/drop --字段
--step2: 创建表空间; expect:成功
create table if not exists t_subpartition_0156
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int
)tablespace ts_subpartition_0156
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
--step3: 修改二级分区表,添加列; expect:成功
alter table t_subpartition_0156 add column col_5 int;
--step4: 插入数据; expect:成功
insert into t_subpartition_0156 values(21,8,1,1,1),(4,7,4,4,4),(5,8,5,5,5),(8,9,8,8,8),(9,9,9,9,9);
--step5: 查询二级分区数据; expect:成功,有数据
select * from t_subpartition_0156 subpartition(p_hash_4_1);
--step6: 修改二级分区表,清空指定分区数据; expect:成功
alter table t_subpartition_0156 truncate subpartition p_hash_4_1;
--step7: 查询二级分区数据; expect:成功,无数据
select * from t_subpartition_0156 subpartition(p_hash_4_1);
--step8: 新增列创建索引; expect:成功
create index on t_subpartition_0156 (col_5);
--step9: 插入数据; expect:成功
insert into t_subpartition_0156 values(1,8,1,1,1),(4,7,4,4,4),(5,8,5,5,5),(8,9,8,8,8),(9,9,9,9,9);
--step10: 修改二级分区表,删除指定列; expect:成功
alter table t_subpartition_0156 drop column col_5 ;
--step11: 查询二级分区数据; expect:成功,4列数据
select * from t_subpartition_0156 subpartition(p_hash_2_1);

--test2: alter table add --约束
--step12: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0041;
create table if not exists t_subpartition_0156
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0156
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
--step13: 修改二级分区表,添加check约束; expect:成功
alter table t_subpartition_0156 add constraint constraint_check check (col_3 is not null);
--step14: col_3插入空数据; expect:合理报错
insert into t_subpartition_0156 values(1,8);
--step15: 插入正确数据; expect:成功
insert into t_subpartition_0156 values(4,7,4,4),(5,8,5,5),(8,9,8,8),(9,9,9,9);

--step16: 清理环境; expect:成功
drop table if exists t_subpartition_0156;
drop tablespace if exists ts_subpartition_0156;
-- @testpoint: list_hash二级分区表：insert on duplicate key update,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0161;
drop tablespace if exists ts_subpartition_0161;
create tablespace ts_subpartition_0161 relative location 'subpartition_tablespace/subpartition_tablespace_0161';
drop tablespace if exists ts_subpartition_0161_01;
create tablespace ts_subpartition_0161_01 relative location 'subpartition_tablespace/subpartition_tablespace_0161_01';

--test1: insert --insert  on duplicate key update -唯一索引
--step1: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0161
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0161
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
    subpartition p_hash_2_3 tablespace ts_subpartition_0161_01,
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
    subpartition p_hash_6_3 tablespace ts_subpartition_0161_01
  )
) enable row movement ;
--step2: 分区键创建唯一索引; expect:成功
create unique index on t_subpartition_0161(col_1,col_2);
--step3: 插入数据; expect:成功
insert into t_subpartition_0161 values(21,11,1,1);
--step4: 插入数据,指定on duplicate key update nothing; expect:成功
insert into t_subpartition_0161 values(21,11,1,1) on duplicate key update nothing;
--step5: 查询数据; expect:成功,1条数据
select * from t_subpartition_0161 subpartition (p_hash_4_1);
--step6: 插入重复数据; expect:合理报错
insert into t_subpartition_0161 values(21,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);--冲突
--step7: 插入不重复数据; expect:成功
insert into t_subpartition_0161 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(99,19,9,9);
--step8: 查询指定二级分区数据; expect:成功,1条数据
select * from t_subpartition_0161 subpartition (p_hash_5_1);
--step9: 插入重复数据更新一级分区键; expect:合理报错
insert into t_subpartition_0161 values(1,11,1,1) on duplicate key update col_1=10;
--step10: 插入重复数据更新二级分区键; expect:合理报错
insert into t_subpartition_0161 values(1,11,1,1) on duplicate key update col_2=10;
--step11: 插入重复数据更新普通列; expect:成功
insert into t_subpartition_0161 values(1,11,1,1) on duplicate key update col_3=10;
--step12: 查询指定二级分区数据; expect:成功,1条数据
select * from t_subpartition_0161 subpartition (p_hash_5_1);

--test2: insert --insert  on duplicate key update -local索引
--step13: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0161;
create table if not exists t_subpartition_0161
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0161
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
    subpartition p_hash_2_4 tablespace ts_subpartition_0161_01,
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
    subpartition p_hash_6_3 tablespace ts_subpartition_0161_01
  )
) enable row movement ;
--step14: 分区键创建local索引; expect:成功
create index on t_subpartition_0161(col_1) local;
--step15: 插入数据; expect:成功
insert into t_subpartition_0161 values(21,11,1,1),(24,41,4,4),(25,54,5,5),(28,87,8,8),(29,19,9,9);
--step16: 查询数据; expect:成功,5条数据
select * from t_subpartition_0161 subpartition (p_hash_4_1);
--step17: 插入重复数据更新一级分区键; expect:成功
insert into t_subpartition_0161 values(1,11,1,1) on duplicate key update col_1=10;
--step18: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0161 values(1,11,1,1) on duplicate key update col_2=10;
--step19: 插入重复数据更新一级分区键换二级分区; expect:成功
insert into t_subpartition_0161 values(1,11,1,1) on duplicate key update col_2=1;
--step20: 查询数据; expect:成功
select * from t_subpartition_0161 subpartition (p_hash_4_1) where col_2<55;

--step21: 清理环境; expect:成功
drop table if exists t_subpartition_0161;
drop tablespace if exists ts_subpartition_0161;
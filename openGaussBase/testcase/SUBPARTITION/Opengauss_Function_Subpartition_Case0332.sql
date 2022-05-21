-- @testpoint: range_hash二级分区表：insert  on duplicate key update/with_query insert字段相同/字段数目不符,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0332;
drop tablespace if exists ts_subpartition_0332;
create tablespace ts_subpartition_0332 relative location 'subpartition_tablespace/subpartition_tablespace_0332';

--test1: insert --insert  on duplicate key update
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0332
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0332
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
    subpartition t_subpartition_0332
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 创建索引数据; expect:成功
create unique index on t_subpartition_0332(col_1,col_2);
--step4: 插入数据,指定on duplicate key update nothing; expect:成功
insert into t_subpartition_0332 values(1,11,1,1) on duplicate key update nothing;
--step5: 查询数据; expect:成功,1条数据
select * from t_subpartition_0332 subpartition (p_range_2_subpartdefault1);
--step6: 插入不重复数据; expect:成功
insert into t_subpartition_0332 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step7: 插入重复数据; expect:合理报错
insert into t_subpartition_0332 values(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step8: 查询数据; expect:成功,5条数据
select * from t_subpartition_0332 subpartition (p_range_2_subpartdefault1);
--step9: 插入重复数据更新一级分区键; expect:合理报错
insert into t_subpartition_0332 values(1,11,1,1) on duplicate key update col_1=10;
--step10: 插入重复数据更新一级分区键; expect:合理报错
insert into t_subpartition_0332 values(1,11,1,1) on duplicate key update col_2=10;
--step11: 插入重复数据更新普通列; expect:成功
insert into t_subpartition_0332 values(1,11,1,1) on duplicate key update col_3=10;
--step12: 查询数据; expect:成功,数据更新
select * from t_subpartition_0332 subpartition (p_range_2_subpartdefault1);

--test2: insert --insert  on duplicate key update
--step13: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0332;
create table if not exists t_subpartition_0332
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0332
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
    subpartition t_subpartition_0332
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step14: 创建索引; expect:成功
create index on t_subpartition_0332(col_1) local;
drop index  if exists i_subpartition_0332;
create index i_subpartition_0332 on t_subpartition_0332(col_2) local(
partition index_p_range_1(subpartition index_p_hash_1_1,subpartition index_p_hash_1_2,subpartition index_p_hash_1_3),
partition index_p_range_2(subpartition index_p_hash_2_1),
partition index_p_range_3(subpartition index_p_hash_3_1,subpartition index_p_hash_3_2,subpartition index_p_hash_3_3),
partition index_p_range_4(subpartition index_p_hash_4_1,subpartition index_p_hash_4_2,subpartition index_p_hash_4_3),
partition index_p_range_5(subpartition index_p_hash_5_1)
);
--step15: 插入数据; expect:成功
insert into t_subpartition_0332 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step16: 查询数据; expect:成功
select * from t_subpartition_0332 subpartition (p_range_2_subpartdefault1);
--step17: 插入重复数据更新一级分区键; expect:成功
insert into t_subpartition_0332 values(1,11,1,1) on duplicate key update col_1=10;
--step18: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0332 values(1,11,1,1) on duplicate key update col_2=10;
--step19: 插入重复数据更新二级分区键; expect:成功
insert into t_subpartition_0332 values(1,11,1,1) on duplicate key update col_2=1;
--step20: 查询数据; expect:成功,数据更新
select * from t_subpartition_0332 subpartition (p_range_2_subpartdefault1);

--test3: insert --with_query  insert(字段数目不符)
--step21: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0332;
create table if not exists t_subpartition_0332
(
    col_1 int ,
    col_2 int ,
    col_3 int
)tablespace ts_subpartition_0332
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
    subpartition t_subpartition_0332
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step22: 创建普通表; expect:成功
drop table if exists t_subpartition_0332_01;
create table if not exists t_subpartition_0332_01
(
    col_1 int ,
    col_2 int ,
    col_3 int ,
    col_4 int 
)tablespace ts_subpartition_0332;
--step23: 普通表插入数据; expect:成功
insert into t_subpartition_0332_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
--step24: 查询临时表所有数据,插入到二级分区表; expect:合理报错
with with_t as (select 1,11,1,1) insert into t_subpartition_0332 (select * from with_t);
--step25: 查询普通表的所有数据,插入到二级分区表; expect:合理报错
insert into t_subpartition_0332 select * from t_subpartition_0332_01;
--step26: 二级分区表插入数据; expect:合理报错
insert into t_subpartition_0332 values(15,9,1,1);
--step27: 查询指定分区表数据; expect:合理报错
select * from t_subpartition_0332 partition(p_range_2) where col_4 > col_2/10;

--step28: 清理环境; expect:成功
drop table if exists t_subpartition_0332;
drop table if exists t_subpartition_0332_01;
drop tablespace if exists ts_subpartition_0332;
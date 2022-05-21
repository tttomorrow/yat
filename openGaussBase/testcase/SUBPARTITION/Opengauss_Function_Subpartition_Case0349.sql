-- @testpoint: range_hash二级分区表：强制转换/cluster,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0349;
drop tablespace if exists ts_subpartition_0349;
create tablespace ts_subpartition_0349 relative location 'subpartition_tablespace/subpartition_tablespace_0349';
--test1: 强制转换
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0349
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0349
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
    subpartition t_subpartition_0349
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0349 values(5.89,6.48,738.8,564.8);
--step4: 查询数据; expect:成功,小数转换为整数
select * from t_subpartition_0349;
--step5: 插入超长数据; expect:合理报错
insert into t_subpartition_0349 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);

--step6: 创建普通表; expect:成功
drop table if exists t_subpartition_0349_01;
create table if not exists t_subpartition_0349_01
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0349;
--step7: 插入超长数据; expect:合理报错
insert into t_subpartition_0349_01 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);
--step8: 插入数据; expect:成功
insert into t_subpartition_0349_01 values(5.89,6.48,738.8,564.8);
--step9: 查询数据; expect:成功,小数转换为整数
select * from t_subpartition_0349_01;

--test2:  cluster(不支持)
--step10: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0349;
create table if not exists t_subpartition_0349
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0349
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
    subpartition t_subpartition_0349
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step11: 插入数据; expect:成功
insert into t_subpartition_0349 values(5.89,6.48,738.8,564.8);
insert into t_subpartition_0349 values(10.89,6.48,738.8,564.8);
--step12: 创建索引; expect:成功
create index  index_01 on t_subpartition_0349(col_1,col_2);
--step13: cluster聚簇排序; expect:合理报错
cluster t_subpartition_0349;
--step14: cluster聚簇排序; expect:合理报错
cluster t_subpartition_0349 using index_01;
--step15: cluster聚簇排序; expect:合理报错
cluster verbose t_subpartition_0349 using index_01;

--step16: 清理环境; expect:成功
drop table if exists t_subpartition_0349_01;
drop table if exists t_subpartition_0349;
drop tablespace if exists ts_subpartition_0349;
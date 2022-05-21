-- @testpoint: range_range二级分区表：强制转换/cluster,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0305;
drop tablespace if exists ts_subpartition_0305;
create tablespace ts_subpartition_0305 relative location 'subpartition_tablespace/subpartition_tablespace_0305';
--test1: 强制转换
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0305
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0305
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0305 values(5.89,6.48,738.8,564.8);
--step4: 查询数据; expect:成功,小数转换为整数
select * from t_subpartition_0305;
--step5: 插入超长数据; expect:合理报错
insert into t_subpartition_0305 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);

--step6: 创建普通表; expect:成功
drop table if exists t_subpartition_0305_01;
create table if not exists t_subpartition_0305_01
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0305;
--step7: 插入超长数据; expect:合理报错
insert into t_subpartition_0305_01 values(58888888888888888888888888888888888885484848484888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888.89,6.48,738.8,564.8);
--step8: 查询数据; expect:成功,无数据
select * from t_subpartition_0305_01;

--test2:  cluster(不支持)
--step9: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0305;
create table if not exists t_subpartition_0305
(
    col_1 int ,
    col_2 int, 
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0305
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
) enable row movement;
--step10: 插入数据; expect:成功
insert into t_subpartition_0305 values(5.89,6.48,738.8,564.8);
--step11: 插入数据; expect:成功
insert into t_subpartition_0305 values(10.89,6.48,738.8,564.8);
--step12: 创建索引; expect:成功
create index  index_01 on t_subpartition_0305(col_1,col_2);
--step13: cluster聚簇排序; expect:合理报错
cluster t_subpartition_0305;
--step14: cluster聚簇排序; expect:合理报错
cluster t_subpartition_0305 using index_01;
--step15: cluster聚簇排序; expect:合理报错
cluster verbose t_subpartition_0305 using index_01;

--step16: 清理环境; expect:成功
drop table if exists t_subpartition_0305_01;
drop table if exists t_subpartition_0305;
drop tablespace if exists ts_subpartition_0305;

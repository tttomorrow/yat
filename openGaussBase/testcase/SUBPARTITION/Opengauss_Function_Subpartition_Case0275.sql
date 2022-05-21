-- @testpoint: range_range二级分区表：null值/local/global/unlogged,测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0275;
create table t_subpartition_0275
(
    col_1 int  ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values ( '1' ),
    subpartition p_range_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values ( '1' ),
    subpartition p_range_2_2 values ( default )
  )
) enable row movement;
--step2: 查询数据; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0275') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0275')) b where a.parentid = b.oid order by a.relname;
--step3: 插入数据; expect:成功
insert into t_subpartition_0275 values(1,null,'1',1);
--step4: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0275 subpartition(p_range_1_2);
--step5: 插入数据; expect:成功
insert into t_subpartition_0275 values(16,null,'1',1);
--step6: 查询指定二级分区数据; expect:成功
select * from t_subpartition_0275 subpartition(p_range_2_2);

--step7: 创建二级分区表,指定local; expect:合理报错
drop table if exists t_subpartition_0275;
create local temp table t_subpartition_0275
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values ( '1' ),
    subpartition p_range_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values ( '1' ),
    subpartition p_range_2_2 values ( default )
  )
) enable row movement;
--step8: 创建二级分区表,指定global; expect:合理报错
drop table if exists t_subpartition_0275;
create global temp table t_subpartition_0275
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values ( '1' ),
    subpartition p_range_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values ( '1' ),
    subpartition p_range_2_2 values ( default )
  )
) enable row movement;
--step9: 创建二级分区表,指定unlogged; expect:合理报错
drop table if exists t_subpartition_0275;
create unlogged table t_subpartition_0275
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values ( '1' ),
    subpartition p_range_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values ( '1' ),
    subpartition p_range_2_2 values ( default )
  )
) enable row movement;

--step10: 清理环境; expect:成功
drop table if exists t_subpartition_0275;
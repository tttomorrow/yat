-- @testpoint: range_range二级分区表：create like from 普通表/列存表,部分测试点合理报错

--test1: create like from 普通表
--step1: 创建普通表; expect:成功
drop table if exists t_subpartition_0257_01;
create table t_subpartition_0257_01
(
    col_1 int  primary key,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int  generated always as(2*col_2) stored  ,
	check (col_4 >= col_2)
);
--step2: 创建表指定like including partition，使用partition by子句; expect:合理报错
drop table if exists  t_subpartition_0257;
create table t_subpartition_0257 (like t_subpartition_0257_01 including partition )
with(fillfactor=80)
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step3: 创建表指定like including partition; expect:合理报错
create table t_subpartition_0257 (like t_subpartition_0257_01 including partition );
--step4: 创建表指定like，使用partition by子句; expect:成功
drop table if exists  t_subpartition_0257;
create table t_subpartition_0257 (like t_subpartition_0257_01  )
with(fillfactor=80)
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step5: 查询分区信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where partstrategy !='n' and parentid = (select oid from pg_class where relname = 't_subpartition_0257') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0257')) b where a.parentid = b.oid order by a.relname;

--test2: create like from 列存表
--step6: 创建列存表; expect:成功
drop table if exists  t_subpartition_0257_01;
create table t_subpartition_0257_01 (col_1 int, col_2 int,col_3 int )
with(orientation = column,compression=middle,max_batchrow=50000,
partial_cluster_rows=100000,deltarow_threshold=1000);
--step7: 创建表指定like including reloptions; expect:合理报错
drop table if exists  t_subpartition_0257;
create table t_subpartition_0257 (like t_subpartition_0257_01 including reloptions)
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 5 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 5 ),
    subpartition p_range_2_2 values less than( 10 )
  )
) enable row movement;
--step8: 插入数据; expect:合理报错
insert into t_subpartition_0257 values(1,1,2);

--step9: 清理环境; expect:成功
drop table if exists t_subpartition_0257;
drop table if exists t_subpartition_0257_01;
-- @testpoint: hash_range二级分区表：insert/explain/index/create as/create like(including all),部分测试点合理报错

--step1: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0075;
create table t_subpartition_0075
(
    col_1 int  primary key,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int  generated always as(2*col_2) stored  ,
	check (col_4 >= col_2)
)
with(fillfactor=80)
partition by list (col_1) subpartition by range (col_2)
(
 partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_range_1_1 values less than( -10 ),
    subpartition p_range_1_2 values less than( 0 ),
    subpartition p_range_1_3 values less than( 10 ),
    subpartition p_range_1_4 values less than( 20 ),
    subpartition p_range_1_5 values less than( 50 )
  ),
  partition p_list_2 values(1,2,3,4,5,6,7,8,9,10 ),
  partition p_list_3 values(11,12,13,14,15,16,17,18,19,20)
  (
    subpartition p_range_3_1 values less than( 15 ),
    subpartition p_range_3_2 values less than( maxvalue )
  ),
    partition p_list_4 values(21,22,23,24,25,26,27,28,29,30)
  (
    subpartition p_range_4_1 values less than( -10 ),
    subpartition p_range_4_2 values less than( 0 ),
    subpartition p_range_4_3 values less than( 10 ),
    subpartition p_range_4_4 values less than( 20 ),
    subpartition p_range_4_5 values less than( 50 )
  ),
   partition p_list_5 values(31,32,33,34,35,36,37,38,39,40)
  (
    subpartition p_range_5_1 values less than( maxvalue )
  ),
   partition p_list_6 values(41,42,43,44,45,46,47,48,49,50)
   (
    subpartition p_range_6_1 values less than( -10 ),
    subpartition p_range_6_2 values less than( 0 ),
    subpartition p_range_6_3 values less than( 10 ),
    subpartition p_range_6_4 values less than( 20 ),
    subpartition p_range_6_5 values less than( 50 )
   ),
   partition p_list_7 values(default)
) enable row movement;
--step1: 插入违反check约束的数据,; expect:合理报错
insert into t_subpartition_0075 values(-1,-1,'aa'),(-5,5,'bb');
--step1: 插入正确数据; expect:成功
insert into t_subpartition_0075 values(1,1,'aa'),(5,5,'bb'),(11,2,'cc'),(19,8,'dd');
--step1: 创建本地索引; expect:成功
drop index if exists i_subpartition_0075_01;
create index i_subpartition_0075_01 on t_subpartition_0075(col_1,col_3) local;
--step1: 创建唯一索引; expect:成功
drop index if exists i_subpartition_0075_02;
create unique index i_subpartition_0075_02 on t_subpartition_0075(col_2);
--step1: 系统表查询信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0075') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0075')) b where a.parentid = b.oid order by a.relname;
--step1: 显示统计数据; expect:成功
explain analyze select * from t_subpartition_0075 partition(p_list_2) where col_1 >5;
--step1: 显示统计数据; expect:成功
explain analyze select * from t_subpartition_0075 subpartition(p_range_4_5);
--step1: create as创建表(普通表); expect:成功
drop table if exists  t_subpartition_0075_01;
create table t_subpartition_0075_01 as select * from t_subpartition_0075;
drop table if exists  t_subpartition_0075_01;
create table t_subpartition_0075_01 as select col_1,col_2,col_3 from t_subpartition_0075;
--step1: create like(including all)  from 分区表; expect:合理报错
drop table if exists  t_subpartition_0075_01;
create table t_subpartition_0075_01 (like t_subpartition_0075 including all );

--step37: 清理环境; expect:成功
drop index if exists i_subpartition_0075_01;
drop index if exists i_subpartition_0075_02;
drop table if exists  t_subpartition_0075;
drop table if exists  t_subpartition_0075_01;
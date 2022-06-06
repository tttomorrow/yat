-- @testpoint: list_list二级分区表：insert/explain/index/create as/create like(including all),部分测试点合理报错

--step1: 创建二级分区表; expect:成功
drop table if exists  t_subpartition_0017;
create table t_subpartition_0017
(
    col_1 int  primary key,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int  generated always as(2*col_2) stored  ,
	check (col_4 >= col_2)
)
with(fillfactor=80)
partition by list (col_1) subpartition by list (col_2)
(
  partition p_list_1 values(-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 )
  (
    subpartition p_list_1_1 values ( 0,-1,-2,-3,-4,-5,-6,-7,-8,-9 ),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_list_2 values(0,1,2,3,4,5,6,7,8,9)
  (
    subpartition p_list_2_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_2_2 values ( default ),
	subpartition p_list_2_3 values ( 10,11,12,13,14,15,16,17,18,19),
	subpartition p_list_2_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
	subpartition p_list_2_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_3 values(10,11,12,13,14,15,16,17,18,19)
  (
    subpartition p_list_3_2 values ( default )
  ),
  partition p_list_4 values(default ),
  partition p_list_5 values(20,21,22,23,24,25,26,27,28,29)
  (
    subpartition p_list_5_1 values ( 0,1,2,3,4,5,6,7,8,9 ),
    subpartition p_list_5_2 values ( default ),
	subpartition p_list_5_3 values ( 10,11,12,13,14,15,16,17,18,19),
	subpartition p_list_5_4 values ( 20,21,22,23,24,25,26,27,28,29 ),
	subpartition p_list_5_5 values ( 30,31,32,33,34,35,36,37,38,39 )
  ),
  partition p_list_6 values(30,31,32,33,34,35,36,37,38,39),
  partition p_list_7 values(40,41,42,43,44,45,46,47,48,49)
  (
    subpartition p_list_7_1 values ( default )
  )
) enable row movement;
--step1: 插入违反check约束的数据,; expect:合理报错
insert into t_subpartition_0017 values(-1,-1,'aa'),(-5,5,'bb');
--step1: 插入正确数据; expect:成功
insert into t_subpartition_0017 values(1,1,'aa'),(5,5,'bb'),(11,2,'cc'),(19,8,'dd');
--step1: 创建本地索引; expect:成功
drop index if exists i_subpartition_0017_01;
create index i_subpartition_0017_01 on t_subpartition_0017(col_1,col_3) local;
--step1: 创建唯一索引; expect:成功
drop index if exists i_subpartition_0017_02;
create unique index i_subpartition_0017_02 on t_subpartition_0017(col_2);
--step1: 系统表查询信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0017') order by relname;
--step1: 显示统计数据; expect:成功
explain analyze select * from t_subpartition_0017 partition(p_list_2) where col_1 >5;
--step1: 显示统计数据; expect:成功
explain analyze select * from t_subpartition_0017 subpartition(p_list_5_5);
--step1: create as创建表(普通表); expect:成功
drop table if exists  t_subpartition_0017_01;
create table t_subpartition_0017_01 as select * from t_subpartition_0017;
drop table if exists  t_subpartition_0017_01;
create table t_subpartition_0017_01 as select col_1,col_2,col_3 from t_subpartition_0017;
--step1: create like(including all)  from 分区表; expect:合理报错
drop table if exists  t_subpartition_0017_01;
create table t_subpartition_0017_01 (like t_subpartition_0017 including all );

--step37: 清理环境; expect:成功
drop index if exists i_subpartition_0017_01;
drop index if exists i_subpartition_0017_02;
drop table if exists  t_subpartition_0017;
drop table if exists  t_subpartition_0017_01;

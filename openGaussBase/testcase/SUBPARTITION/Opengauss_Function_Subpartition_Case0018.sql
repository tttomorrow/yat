-- @testpoint: list_list二级分区表：create like from 普通表/列存表,部分测试点合理报错

--test1: create like from 普通表
--step1: 创建普通表; expect:成功
drop table if exists t_subpartition_0018_01;
create table t_subpartition_0018_01
(
    col_1 int  primary key,
    col_2 int  not null ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int  generated always as(2*col_2) stored  ,
	check (col_4 >= col_2)
);
--step1: 创建表指定like including partition，使用partition by子句; expect:合理报错
drop table if exists  t_subpartition_0018;
create table t_subpartition_0018 (like t_subpartition_0018_01 including partition )
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
--step1: 创建表指定like including partition; expect:合理报错
drop table if exists  t_subpartition_0018;
create table t_subpartition_0018 (like t_subpartition_0018_01 including partition );
--step1: 创建表指定like，使用partition by子句; expect:成功
drop table if exists  t_subpartition_0018;
create table t_subpartition_0018 (like t_subpartition_0018_01  )
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
--step1: 系统表查询信息; expect:成功
select relname, parttype, partstrategy, boundaries from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0018') order by relname;


--test1: create like from 列存表
--step1: 创建列存表; expect:成功
drop table if exists  t_subpartition_0018_01;
create table t_subpartition_0018_01 (col_1 int, col_2 int,col_3 int )
with(orientation = column,compression=middle,max_batchrow=50000,
partial_cluster_rows=100000,deltarow_threshold=1000);
--step1: 创建表指定like including reloptions; expect:合理报错
drop table if exists  t_subpartition_0018;
create table t_subpartition_0018 (like t_subpartition_0018_01 including reloptions)
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

--step37: 删除表; expect:成功
drop table if exists t_subpartition_0018;
drop table if exists t_subpartition_0018_01;

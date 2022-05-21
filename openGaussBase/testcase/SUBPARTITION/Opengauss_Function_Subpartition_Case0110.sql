-- @testpoint: list_range二级分区表：select join

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0110;
drop tablespace if exists ts_subpartition_0110;
create tablespace ts_subpartition_0110 relative location 'subpartition_tablespace/subpartition_tablespace_0110';
--test1: select join
--step2: 创建二级分区表1; expect:成功
drop table if exists t_subpartition_0110_01;
create table t_subpartition_0110_01
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 int not null ,
    col_4 int
)
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
--step3: 插入数据; expect:成功
insert into t_subpartition_0110_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0110_01 values(1,8,1,1),(4,7,4,4),(5,8,5,5),(8,9,8,8),(9,9,9,9);
--step4: 创建二级分区表2; expect:成功
drop table if exists t_subpartition_0110;
create table if not exists t_subpartition_0110
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int
)tablespace ts_subpartition_0110
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
--step5: 插入数据; expect:成功
insert into t_subpartition_0110 values(-15,1,1,1),(-4,1,4,4),(15,5,5,5),(18,8,8,8),(199,9,9,9);
insert into t_subpartition_0110 values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0110 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0110 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);

--step6: inner join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0110.col_1,t_subpartition_0110.col_2,t_subpartition_0110.col_3,t_subpartition_0110.col_4 from t_subpartition_0110 inner join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) aa
inner join  t_subpartition_0110_01 bb
on aa.col_2 = bb.col_4;
--step7: left join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0110.col_1,t_subpartition_0110.col_2,t_subpartition_0110.col_3,t_subpartition_0110.col_4 from t_subpartition_0110 LEFT join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) aa
LEFT join  t_subpartition_0110_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;
--step8: right join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0110.col_1,t_subpartition_0110.col_2,t_subpartition_0110.col_3,t_subpartition_0110.col_4 from t_subpartition_0110 RIGHT join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) aa
RIGHT join  t_subpartition_0110_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;
--step9: full  join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0110.col_1,t_subpartition_0110.col_2,t_subpartition_0110.col_3,t_subpartition_0110.col_4 from t_subpartition_0110 FULL join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) aa
FULL join  t_subpartition_0110_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;
--step10: anti-join查询数据; expect:成功
select * from t_subpartition_0110 where not exists
(select t_subpartition_0110.col_1 from t_subpartition_0110 FULL join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) order by 1 limit 2 ;
--step11: explain anti-join查询数据的执行计划; expect:成功,确认使用hash join
explain select * from t_subpartition_0110 where not exists
(select t_subpartition_0110.col_1 from t_subpartition_0110 FULL join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) order by 1 limit 2 ;
--step12: semi-join查询数据; expect:成功
select * from t_subpartition_0110 where  exists
(select t_subpartition_0110.col_1 from t_subpartition_0110 FULL join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) order by 1 limit 2 ;
--step13: cross join查询数据; expect:成功
select * from t_subpartition_0110 where  exists
(select t_subpartition_0110.col_1 from t_subpartition_0110 CROSS join t_subpartition_0110_01
where t_subpartition_0110.col_2 >10) order by 1 limit 2 ;
--step14: explain cross join查询数据的执行计划; expect:成功,确认使用nest loop join
explain select * from t_subpartition_0110 where  exists
(select t_subpartition_0110.col_1 from t_subpartition_0110 CROSS join t_subpartition_0110_01
where t_subpartition_0110.col_2 >10) order by 1 limit 2 ;

--test2: netloop join
--step15: 设置相关参数; expect:成功
SET enable_nestloop TO true;
SET enable_hashjoin TO false;
SET enable_mergejoin TO  false;
--step16: netloop join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0110.col_1,t_subpartition_0110.col_2,t_subpartition_0110.col_3,t_subpartition_0110.col_4 from t_subpartition_0110 FULL join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) aa
FULL join  t_subpartition_0110_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;
--step17: explain analyze  netloop join查询数据的执行计划; expect:成功,确认使用nest loop join
explain analyze select bb.col_3 from (
select t_subpartition_0110.col_1,t_subpartition_0110.col_2,t_subpartition_0110.col_3,t_subpartition_0110.col_4 from t_subpartition_0110 FULL join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) aa
FULL join  t_subpartition_0110_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;

--test3: hash join
--step18: 设置相关参数; expect:成功
SET enable_nestloop TO false;
SET enable_hashjoin TO true;
SET enable_mergejoin TO  false;
--step19: explain analyze  hash join查询数据的执行计划; expect:成功,确认使用hash join
explain analyze select bb.col_3 from (
select t_subpartition_0110.col_1,t_subpartition_0110.col_2,t_subpartition_0110.col_3,t_subpartition_0110.col_4 from t_subpartition_0110 FULL join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) aa
FULL join  t_subpartition_0110_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;

--test4: merge join
--step20: 设置相关参数; expect:成功
SET enable_nestloop TO false;
SET enable_hashjoin TO false;
SET enable_mergejoin TO  true;
--step21: explain analyze  merge join查询数据的执行计划; expect:成功,确认使用merge join
explain analyze select bb.col_3 from (
select t_subpartition_0110.col_1,t_subpartition_0110.col_2,t_subpartition_0110.col_3,t_subpartition_0110.col_4 from t_subpartition_0110 FULL join t_subpartition_0110_01
on t_subpartition_0110.col_1 = t_subpartition_0110_01.col_1
where t_subpartition_0110.col_2 >10) aa
FULL join  t_subpartition_0110_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;

--step22: 清理环境; expect:成功
drop table if exists t_subpartition_0110;
drop table if exists t_subpartition_0110_01;
drop tablespace if exists ts_subpartition_0110;
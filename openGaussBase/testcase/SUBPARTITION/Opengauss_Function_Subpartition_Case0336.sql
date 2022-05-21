-- @testpoint: range_hash二级分区表：select join,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0336;
drop table if exists t_subpartition_0336_01;
drop tablespace if exists ts_subpartition_0336;
create tablespace ts_subpartition_0336 relative location 'subpartition_tablespace/subpartition_tablespace_0336';

--test1: select join
--step2: 创建二级分区表1; expect:成功
create table t_subpartition_0336_01
(
    col_1 int  not null ,
    col_2 int  not null ,
    col_3 int not null ,
    col_4 int
)
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
    subpartition t_subpartition_0336
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0336_01 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0336_01 values(1,8,1,1),(4,7,4,4),(5,8,5,5),(8,9,8,8),(9,9,9,9);
--step4: 创建二级分区表2; expect:成功
drop table if exists t_subpartition_0336;
create table if not exists t_subpartition_0336
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) not null ,
    col_4 int 
)tablespace ts_subpartition_0336
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
    subpartition t_subpartition_0336
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step5: 插入数据; expect:成功
insert into t_subpartition_0336 values(-15,1,1,1),(-4,1,4,4),(15,5,5,5),(18,8,8,8),(199,9,9,9);
insert into t_subpartition_0336 values(1,1,1,1),(4,1,4,4),(5,5,5,5),(8,8,8,8),(9,9,9,9);
insert into t_subpartition_0336 values(1,11,1,1),(4,41,4,4),(5,54,5,5),(8,87,8,8),(9,19,9,9);
insert into t_subpartition_0336 values(11,1,1,1),(14,1,4,4),(15,5,5,5),(18,8,8,8),(19,1,9,9);

--step6: inner join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0336.col_1,t_subpartition_0336.col_2,t_subpartition_0336.col_3,t_subpartition_0336.col_4 from t_subpartition_0336 inner join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) aa
inner join  t_subpartition_0336_01 bb
on aa.col_2 = bb.col_4;
--step7: left join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0336.col_1,t_subpartition_0336.col_2,t_subpartition_0336.col_3,t_subpartition_0336.col_4 from t_subpartition_0336 left join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) aa
left join  t_subpartition_0336_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;
--step8: right join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0336.col_1,t_subpartition_0336.col_2,t_subpartition_0336.col_3,t_subpartition_0336.col_4 from t_subpartition_0336 right join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) aa
right join  t_subpartition_0336_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;
--step9: full  join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0336.col_1,t_subpartition_0336.col_2,t_subpartition_0336.col_3,t_subpartition_0336.col_4 from t_subpartition_0336 full join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) aa
full join  t_subpartition_0336_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;
--step10: anti-join查询数据; expect:成功
select * from t_subpartition_0336 where not exists
(select t_subpartition_0336.col_1 from t_subpartition_0336 full join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) order by 1 limit 2 ;
--step11: explain anti-join查询数据的执行计划; expect:成功,确认使用hash join
explain select * from t_subpartition_0336 where not exists
(select t_subpartition_0336.col_1 from t_subpartition_0336 full join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) order by 1 limit 2 ;
--step12: semi-join查询数据; expect:成功
select * from t_subpartition_0336 where  exists
(select t_subpartition_0336.col_1 from t_subpartition_0336 full join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) order by 1 limit 2 ;
--step13: cross join查询数据; expect:成功
select * from t_subpartition_0336 where  exists
(select t_subpartition_0336.col_1 from t_subpartition_0336 cross join t_subpartition_0336_01
where t_subpartition_0336.col_2 >10) order by 1 limit 2 ;
--step14: explain cross join查询数据的执行计划; expect:成功,确认使用nest loop join
explain select * from t_subpartition_0336 where  exists
(select t_subpartition_0336.col_1 from t_subpartition_0336 cross join t_subpartition_0336_01
where t_subpartition_0336.col_2 >10) order by 1 limit 2 ;

--test2: netloop join
--step15: 设置相关参数; expect:成功
set enable_nestloop to true;
set enable_hashjoin to false;
set enable_mergejoin to  false;
--step16: netloop join查询数据; expect:成功
select bb.col_3 from (
select t_subpartition_0336.col_1,t_subpartition_0336.col_2,t_subpartition_0336.col_3,t_subpartition_0336.col_4 from t_subpartition_0336 full join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) aa
full join  t_subpartition_0336_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;
--step17: explain analyze  netloop join查询数据的执行计划; expect:成功,确认使用nest loop join
explain analyze select bb.col_3 from (
select t_subpartition_0336.col_1,t_subpartition_0336.col_2,t_subpartition_0336.col_3,t_subpartition_0336.col_4 from t_subpartition_0336 full join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) aa
full join  t_subpartition_0336_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;

--test3: hash join
--step18: 设置相关参数; expect:成功
set enable_nestloop to false;
set enable_hashjoin to true;
set enable_mergejoin to  false;
--step19: explain analyze  hash join查询数据的执行计划; expect:成功,确认使用hash join
explain analyze select bb.col_3 from (
select t_subpartition_0336.col_1,t_subpartition_0336.col_2,t_subpartition_0336.col_3,t_subpartition_0336.col_4 from t_subpartition_0336 full join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) aa
full join  t_subpartition_0336_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;

--test4: merge join
--step20: 设置相关参数; expect:成功
set enable_nestloop to false;
set enable_hashjoin to false;
set enable_mergejoin to  true;
--step21: explain analyze  merge join查询数据的执行计划; expect:成功,确认使用merge join
explain analyze select bb.col_3 from (
select t_subpartition_0336.col_1,t_subpartition_0336.col_2,t_subpartition_0336.col_3,t_subpartition_0336.col_4 from t_subpartition_0336 full join t_subpartition_0336_01
on t_subpartition_0336.col_1 = t_subpartition_0336_01.col_1
where t_subpartition_0336.col_2 >10) aa
full join  t_subpartition_0336_01 bb
on aa.col_1 = bb.col_2 order by 1 limit 2 offset 3;

--step22: 清理环境; expect:成功
drop table if exists t_subpartition_0336;
drop table if exists t_subpartition_0336_01;
drop tablespace if exists ts_subpartition_0336;
-- @testpoint: list_list二级分区表：analyze/vacuum,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0070;
drop tablespace if exists ts_subpartition_0070;
create tablespace ts_subpartition_0070 relative location 'subpartition_tablespace/subpartition_tablespace_0070';
--test1: analyze收集分区表的统计信息
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0070
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
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
--step3: 插入数据; expect:成功
insert into  t_subpartition_0070 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step4: 收集指定分区的统计信息; expect:成功,只支持语法,不收集统计信息
analyze t_subpartition_0070 partition(p_list_6);
select pg_sleep(2);
--step5: 查询pg_statistic数据; expect:成功,0条数据
select starelkind,stainherit from pg_statistic where starelid=(select oid from pg_class where relname='t_subpartition_0070');
--step6: 查询pg_stats数据; expect:成功,0条数据
select tablename,attname from pg_stats  where tablename='t_subpartition_0070';

--test2:  analyze--收集多列统计信息(包含分区列)
--step7: 收集2个分区列统计信息; expect:成功
analyze t_subpartition_0070 (col_1,col_2);
select pg_sleep(2);
--step8: 查询pg_statistic数据; expect:成功,2条数据
select starelkind,stainherit from pg_statistic where starelid=(select oid from pg_class where relname='t_subpartition_0070');
--step9: 查询pg_stats数据; expect:成功,2条数据
select tablename,attname from pg_stats  where tablename='t_subpartition_0070';
--step10: 查询pg_stat_all_tables数据; expect:成功,显示analyze的次数1
select schemaname,relname,analyze_count from pg_stat_all_tables where relname='t_subpartition_0070';

--test3:  analyze--收集多列统计信息(不包含分区列)
--step11: 收集2个普通列统计信息; expect:成功
analyze t_subpartition_0070 (col_3,col_4);
select pg_sleep(2);
--step12: 查询pg_statistic数据; expect:成功,4条数据
select starelkind,stainherit from pg_statistic where starelid=(select oid from pg_class where relname='t_subpartition_0070');
--step13: 查询pg_stats数据; expect:成功,4条数据
select tablename,attname from pg_stats  where tablename='t_subpartition_0070';
--step14: 查询pg_stat_all_tables数据; expect:成功,显示analyze的次数2
select schemaname,relname,analyze_count from pg_stat_all_tables where relname='t_subpartition_0070';

--test4:  analyze--检测表数据文件
--step15: 检测表数据文件; expect:成功
analyze  verify fast;
analyze  verify complete;

--test5:  analyze--检测表和索引的数据文件
--step7: 创建索引; expect:成功
drop index if exists i_subpartition_0070;
create index i_subpartition_0070 on t_subpartition_0070(col_2);
--step16: 检测表和索引的数据文件; expect:成功
analyze verify fast t_subpartition_0070 ;
analyse verify complete i_subpartition_0070 cascade;

--test6:  analyze--检测表分区的数据文件
--step17: 检测表分区的数据文件; expect:成功
analyze  verify fast t_subpartition_0070 partition (p_list_1);
analyze  verify complete t_subpartition_0070 partition (p_list_1) cascade;

--test7:  vacuum--仅回收空间,不更新统计信息
--step18: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0070 cascade;
create table t_subpartition_0070
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0070
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
--step19: 插入数据; expect:成功
insert into  t_subpartition_0070 values (generate_series(0, 79),generate_series(0, 79),generate_series(0, 79));
--step20: vacuum回收空间; expect:成功
vacuum  full freeze  verbose  t_subpartition_0070 partition(p_list_2);
select pg_sleep(2);
--step21: 查询pg_stat_all_tables数据; expect:成功,vacuum_count次数未更新
select schemaname,relname,vacuum_count from pg_stat_all_tables where relname='t_subpartition_0070';
--step22: vacuum不同组合; expect:成功
vacuum full  freeze t_subpartition_0070;
vacuum full  verbose t_subpartition_0070;
vacuum full  compact t_subpartition_0070;
vacuum freeze t_subpartition_0070;
vacuum freeze t_subpartition_0070 partition(p_list_5);
vacuum verbose t_subpartition_0070;
vacuum verbose t_subpartition_0070 partition(p_list_5);
vacuum full  freeze t_subpartition_0070 partition(p_list_5);
vacuum full  verbose t_subpartition_0070 partition(p_list_5);
--step23: vacuum组合compact,partition; expect:合理报错
vacuum full  compact t_subpartition_0070 partition(p_list_5);

--test8:  vacuum--回收空间并更新统计信息,对关键字顺序无要求
--step24: vacuum回收空间; expect:成功
vacuum  full freeze  verbose analyze t_subpartition_0070 partition(p_list_2);
vacuum full  analyze  t_subpartition_0070;
vacuum freeze analyze  t_subpartition_0070(col_1);
vacuum verbose analyze t_subpartition_0070 partition(p_list_5);
vacuum verbose analyze t_subpartition_0070(col_5) partition(p_list_5);

--test9:  vacuum--回收空间并更新统计信息,且对关键字顺序有要求。
--step25: vacuum顺序改变; expect:合理报错
vacuum  freeze full verbose analyze verbose t_subpartition_0070;
--step23: vacuum分析具体的字段名称,不搭配analyze选项使用; expect:合理报错
vacuum full freeze verbose t_subpartition_0070(col_2);
vacuum full freeze verbose t_subpartition_0070(col_2) partition(p_list_5);

--step26: vacuum搭配不同的关键字回收空间; expect:成功
vacuum full freeze verbose analyze verbose t_subpartition_0070;
vacuum full freeze verbose analyze verbose t_subpartition_0070(col_2);
vacuum full freeze verbose analyze verbose t_subpartition_0070(col_2) partition(p_list_5);
vacuum full freeze verbose analyze verbose t_subpartition_0070 partition(p_list_5);
vacuum freeze verbose analyze verbose t_subpartition_0070;
vacuum freeze verbose analyze verbose t_subpartition_0070(col_2);
vacuum freeze verbose analyze verbose t_subpartition_0070(col_2) partition(p_list_5);
vacuum freeze verbose analyze verbose t_subpartition_0070 partition(p_list_5);
vacuum full freeze  analyze verbose t_subpartition_0070;
vacuum full freeze  analyze verbose t_subpartition_0070(col_2);
vacuum full freeze  analyze verbose t_subpartition_0070(col_2) partition(p_list_5);
vacuum full freeze  analyze verbose t_subpartition_0070 partition(p_list_5);
vacuum full freeze verbose t_subpartition_0070;
vacuum full freeze verbose t_subpartition_0070 partition(p_list_5);
vacuum analyze verbose t_subpartition_0070;
vacuum analyze verbose t_subpartition_0070(col_2);
vacuum analyze verbose t_subpartition_0070(col_2) partition(p_list_5);
vacuum analyze verbose t_subpartition_0070 partition(p_list_5);

--step27: 查询表数据大小：包括表数据+索引; expect:成功
create index on t_subpartition_0070(col_1,col_3);
create index on t_subpartition_0070(col_2);
select ctid,* from t_subpartition_0070 order by col_1;
select pg_size_pretty(pg_total_relation_size('t_subpartition_0070'));
select pg_size_pretty(pg_indexes_size('t_subpartition_0070'));
select pg_size_pretty(pg_relation_size('t_subpartition_0070'));
select pg_size_pretty(pg_relation_size('t_subpartition_0070_col_1_col_3_tableoid_idx'));
select pg_size_pretty(pg_relation_size('t_subpartition_0070_col_2_tableoid_idx'));

--step28: 删除表和表空间; expect:成功
drop table if exists t_subpartition_0070;
drop tablespace if exists ts_subpartition_0070;
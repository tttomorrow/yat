-- @testpoint: range_range二级分区表：相关系统表pg_stat_user_tables/pg_statistic/pg_stat_all_tables/pg_get_tabledef

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0287_01;
drop table if exists t_subpartition_0287;
drop tablespace if exists ts_subpartition_0287;
create tablespace ts_subpartition_0287 relative location 'subpartition_tablespace/subpartition_tablespace_0287';

--test1: 相关系统表 --pg_stat_user_tables
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0287
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0287
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than(-80 )
  (
    subpartition p_range_1_1 values less than(  -20),
    subpartition p_range_1_2 values less than( 50 ),
    subpartition p_range_1_3 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  ),
  partition p_range_3 values less than( 100 ),
  partition p_range_4 values less than( 200 )
  (
    subpartition p_range_4_1 values less than( 30 ),
    subpartition p_range_4_2 values less than( 100),
    subpartition p_range_4_3 values less than( 150 ),
    subpartition p_range_4_4 values less than( maxvalue )
  )
);
--step3: 清空数据; expect:成功
truncate t_subpartition_0287;
--step4: 插入数据; expect:成功
insert into t_subpartition_0287 values(-90,-10,3,8),(-90,10,3,8),(-100,80,3,8);
insert into t_subpartition_0287 values(90,-10,3,8),(90,10,3,8),(100,80,3,8);
select pg_sleep(2);
--step5: 查询系统表pg_stat_user_tables数据; expect:成功
select n_tup_ins from pg_stat_user_tables where relname = 't_subpartition_0287';

--step6: 创建普通表; expect:成功
drop table if exists t_subpartition_0287_01;
create table t_subpartition_0287_01
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0287;
--step7: 插入数据; expect:成功
insert into t_subpartition_0287_01 values(-90,-10,3,8),(-90,10,3,8),(-100,80,3,8);
insert into t_subpartition_0287_01 values(90,-10,3,8),(90,10,3,8),(100,80,3,8);
select pg_sleep(2);
--step8: 查询系统表pg_stat_user_tables数据; expect:成功,普通表更新
select n_tup_ins from pg_stat_user_tables where relname = 't_subpartition_0287_01';

--test2: 相关系统表 --pg_statistic
--step9: analyze收集表的统计信息; expect:成功
analyze t_subpartition_0287;
select pg_sleep(2);
--step10: 查询数据; expect:成功
select starelkind,stainherit from pg_statistic  where starelid =(select oid from pg_class where relname = 't_subpartition_0287');

--test3: 相关系统表 --pg_stat_all_tables
--step11: vacuum回收空间; expect:成功
vacuum t_subpartition_0287;
select pg_sleep(2);
--step12: 查询数据; expect:成功
select vacuum_count from pg_stat_all_tables where  relid =(select oid from pg_class where relname = 't_subpartition_0287');

--test4: 相关系统表 --pg_get_tabledef
--step13: 查询数据; expect:成功
select pg_get_tabledef(oid) from pg_class where relname='t_subpartition_0287';

--step14: 清理环境; expect:成功
drop table if exists t_subpartition_0287_01;
drop table if exists t_subpartition_0287;
drop tablespace if exists ts_subpartition_0287;
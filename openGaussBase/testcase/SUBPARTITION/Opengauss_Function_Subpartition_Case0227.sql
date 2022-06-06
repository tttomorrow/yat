-- @testpoint: range_list二级分区表：相关系统表pg_class/pg_stat_user_tables/pg_statistic/pg_stat_all_tables/pg_get_tabledef

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0227;
drop tablespace if exists ts_subpartition_0227;
create tablespace ts_subpartition_0227 relative location 'subpartition_tablespace/subpartition_tablespace_0227';

--test1: 相关系统表 --pg_class
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0227
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0227
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step3: 查询系统表pg_partition数据; expect:成功
select relname,parttype,relrowmovement from pg_class where relname='t_subpartition_0227';
--step4: 查看分区信息; expect:成功
select relname,parttype,partstrategy,indisusable,interval from pg_partition where parentid = (select oid from pg_class where relname = 't_subpartition_0227') order by relname;
select a.relname,a.parttype,a.partstrategy,a.indisusable from pg_partition a,(select oid from pg_partition
where parentid = (select oid from pg_class where relname = 't_subpartition_0227')) b where a.parentid = b.oid order by a.relname;

--test2: 相关系统表 --pg_stat_user_tables
--step5: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0227;
create table t_subpartition_0227
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0227
partition by range (col_1) subpartition by list (col_2)
(
  partition p_range_1 values less than( -10 )
  (
    subpartition p_list_1_1 values ( '-1','-2','-3','-4','-5'),
    subpartition p_list_1_2 values ( default )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_list_2_1 values ( '6','7','8','9','10'),
    subpartition p_list_2_2 values ( default )
  ),
   partition p_range_3 values less than( 30 )
   (
    subpartition p_list_3_1 values ( default )
  ),
   partition p_range_4 values less than( 40 )
   (
    subpartition p_list_4_1 values ( default )
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step6: 查询系统表pg_stat_user_tables数据; expect:成功
select n_tup_ins,n_tup_upd from pg_stat_user_tables where relname = 't_subpartition_0227';
--step7: 清空表数据; expect:成功
truncate t_subpartition_0227;
--step8: 插入数据; expect:成功
insert into t_subpartition_0227 values(-90,-10,3,8),(-90,10,3,8),(-100,80,3,8);
insert into t_subpartition_0227 values(90,-10,3,8),(90,10,3,8),(100,80,3,8);
--step9: 更新指定条件的数据; expect:成功
update t_subpartition_0227 set  col_1=100 where col_1=90;
select pg_sleep(6);
select pg_sleep(6);
--step10: 查询系统表pg_stat_user_tables数据; expect:成功,插入行数6,更新行数2
select n_tup_ins,n_tup_upd from pg_stat_user_tables where relname = 't_subpartition_0227';

--step11: 创建普通表; expect:成功
drop table if exists t_subpartition_0227_01;
create table t_subpartition_0227_01
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0227;
select n_tup_ins from pg_stat_user_tables where relname = 't_subpartition_0227_01';
--step12: 插入数据; expect:成功
insert into t_subpartition_0227_01 values(-90,-10,3,8),(-90,10,3,8),(-100,80,3,8);
insert into t_subpartition_0227_01 values(90,-10,3,8),(90,10,3,8),(100,80,3,8);
select pg_sleep(6);
select pg_sleep(6);
--step13: 查询系统表pg_stat_user_tables数据; expect:成功,插入行数6
select n_tup_ins from pg_stat_user_tables where relname = 't_subpartition_0227_01';

--test3: 相关系统表 --pg_statistic
--step14: analyze收集表的统计信息; expect:成功
analyze t_subpartition_0227;
select pg_sleep(6);
select pg_sleep(6);
--step15: 查询数据; expect:成功,4条数据
select starelkind,stainherit from pg_statistic  where starelid =(select oid from pg_class where relname = 't_subpartition_0227');

--test4: 相关系统表 --pg_stat_all_tables
--step16: vacuum回收空间; expect:成功
vacuum t_subpartition_0227;
select pg_sleep(6);
select pg_sleep(6);
--step17: 查询数据; expect:成功,被清理的次数1
select vacuum_count from pg_stat_all_tables where  relid =(select oid from pg_class where relname = 't_subpartition_0227');

--test5: 相关系统表 --pg_get_tabledef
--step18: 查询数据; expect:成功
select pg_get_tabledef(oid) from pg_class where relname='t_subpartition_0227';

--step19: 清理环境; expect:成功
drop table if exists t_subpartition_0227;
drop table if exists t_subpartition_0227_01;
drop tablespace if exists ts_subpartition_0227;
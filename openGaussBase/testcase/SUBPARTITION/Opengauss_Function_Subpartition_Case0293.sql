-- @testpoint: range_range二级分区表：视图/物化视图,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0293;
drop tablespace if exists ts_subpartition_0293;
create tablespace ts_subpartition_0293 relative location 'subpartition_tablespace/subpartition_tablespace_0293';
--test1: 视图
--step2: 创建二级分区表; expect:成功
create table if not exists t_subpartition_0293
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0293
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 20 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
) enable row movement;
--step3: 插入数据; expect:成功
insert into t_subpartition_0293 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));

--step4: 创建视图：rownum; expect:成功
drop view if exists v_subpartition_0293;
create view v_subpartition_0293 as select * from t_subpartition_0293;
--step5: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0293 where col_1 =4;
--step6: 查询视图数据; expect:成功,95095条
select  count(*) from v_subpartition_0293;
--step7: 查询表数据; expect:成功,95095条
select  count(*) from t_subpartition_0293;
--step8: 更新表中指定条件的数据; expect:成功
update t_subpartition_0293 set col_1 =4 where col_1=1;
--step9: 查询指定条件的视图数据; expect:成功,0条
select * from v_subpartition_0293 where col_1=1;

--test2: 物化视图
--step10: 创建物化视图; expect:成功
drop materialized view if exists vm_subpartition_0293;
create materialized view vm_subpartition_0293 as select * from t_subpartition_0293;
--step11: 查询物化视图数据; expect:成功
select  count(*) from vm_subpartition_0293;
--step12: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0293 where col_1 =4;
--step13: 查询物化视图数据; expect:成功,数据条数没变
select  count(*) from vm_subpartition_0293;
--step14: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0293;
--step15: 查询物化视图数据; expect:成功,数据条数减少
select  count(*) from vm_subpartition_0293;

--step16: count查询指定条件的物化视图数据; expect:成功
select count(*) from vm_subpartition_0293 where col_1=1;
--step17: count查询指定条件的物化视图数据; expect:成功
select count(*) from vm_subpartition_0293 where col_1=4;
--step18: 更新表中指定条件的数据; expect:成功
update t_subpartition_0293 set col_1 =4 where col_1=1;
--step19: 查询数据; expect:成功,5005条数据
select count(*) from vm_subpartition_0293 where col_1=11;
--step20: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0293;
--step21: 查询数据; expect:成功,5005条数据
select count(*) from vm_subpartition_0293 where col_1=11;

--step22: 清理环境; expect:成功
drop view if exists v_subpartition_0293;
drop materialized view if exists vm_subpartition_0293;
drop table if exists t_subpartition_0293 cascade;
drop table if exists t_subpartition_0293_01 cascade;
drop table if exists t_subpartition_0293_02 cascade;
drop tablespace if exists ts_subpartition_0293;
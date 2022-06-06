-- @testpoint: range_list二级分区表：rownum/视图/物化视图

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0234 cascade;
drop tablespace if exists ts_subpartition_0234;
create tablespace ts_subpartition_0234 relative location 'subpartition_tablespace/subpartition_tablespace_0234';
--test1: 分区表 + rownum
--step2: 创建二级分区表并插入数据; expect:成功
create table if not exists t_subpartition_0234
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)tablespace ts_subpartition_0234
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
insert into t_subpartition_0234 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
--step3: 查询数据：rownum; expect:成功
select rownum,* from t_subpartition_0234 where col_3 >98 and rownum <10;
--step4: 查询数据：rownum/order by/desc/limit; expect:成功
select rownum,* from t_subpartition_0234 where col_3 >98 order by rownum desc limit 2,18;
--step5: 查询数据：select rownum as 别名; expect:成功
select rownum rrrr,col_2 from t_subpartition_0234 limit 5;

--test2: 视图
--step6: 创建视图：rownum; expect:成功
drop view if exists v_subpartition_0234;
create view v_subpartition_0234 as select * from t_subpartition_0234;
--step7: 查询视图数据; expect:成功
select * from v_subpartition_0234 limit 10;
--step8: 查询视图数据; expect:成功,100100条
select  count(*) from v_subpartition_0234;
--step9: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0234 where col_1 =4;
--step10: 查询视图数据; expect:成功,数据减少,95095条
select  count(*) from v_subpartition_0234;
--step11: 查询表数据; expect:成功,数据减少,95095条
select  count(*) from t_subpartition_0234;
--step12: 更新表中指定条件的数据; expect:成功
update t_subpartition_0234 set col_1 =4 where col_1=1;
--step13: 查询指定条件的视图数据; expect:成功,0条
select * from v_subpartition_0234 where col_1=1;

--test3: 物化视图
--step14: 创建物化视图; expect:成功
drop materialized view if exists vm_subpartition_0234;
create materialized view vm_subpartition_0234 as select * from t_subpartition_0234;
--step15: 查询物化视图数据; expect:成功
select  count(*) from vm_subpartition_0234;
--step16: 删除表中指定条件的数据; expect:成功
delete t_subpartition_0234 where col_1 =4;
--step17: 查询物化视图数据; expect:成功,数据条数没变
select  count(*) from vm_subpartition_0234;
--step18: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0234;
--step19: 查询物化视图数据; expect:成功,数据条数减少
select  count(*) from vm_subpartition_0234;

--step20: count查询指定条件的物化视图数据; expect:成功
select  count(*) from vm_subpartition_0234;
--step21: count查询指定条件的物化视图数据; expect:成功
select count(*) from vm_subpartition_0234 where col_1=11;
--step22: count查询指定条件的物化视图数据; expect:成功
select count(*) from vm_subpartition_0234 where col_1=4;
--step23: 更新表中指定条件的数据; expect:成功
update t_subpartition_0234 set col_1 =18 where col_1=11;
--step24: 查询数据; expect:成功,数据条数没变
select count(*) from vm_subpartition_0234 where col_1=11;
--step25: 刷新物化视图数据; expect:成功
refresh materialized view vm_subpartition_0234;
--step26: 查询数据; expect:成功,0条数据
select count(*) from vm_subpartition_0234 where col_1=11;

--step27: 清理环境; expect:成功
drop view if exists v_subpartition_0234;
drop materialized view if exists vm_subpartition_0234;
drop table if exists t_subpartition_0234 cascade;
drop table if exists t_subpartition_0234_01 cascade;
drop table if exists t_subpartition_0234_02 cascade;
drop tablespace if exists ts_subpartition_0234;
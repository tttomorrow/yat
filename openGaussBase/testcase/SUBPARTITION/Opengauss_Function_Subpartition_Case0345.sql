-- @testpoint: range_hash二级分区表：segment/并行查询smp/package/生成列,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0345;
drop tablespace if exists ts_subpartition_0345;
create tablespace ts_subpartition_0345 relative location 'subpartition_tablespace/subpartition_tablespace_0345';

--test1: segment表
--step2: 创建二级分区表,指定segment=on; expect:成功
create table t_subpartition_0345
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)with (segment=on)
tablespace ts_subpartition_0345
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
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;

--test2: 并行查询smp
--step3: 创建二级分区表; expect:成功
drop table if exists t_subpartition_0345;
create table t_subpartition_0345
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0345
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
    subpartition t_subpartition_0345
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step4: 插入大量数据; expect:成功
insert into  t_subpartition_0345 values (generate_series(0, 19),generate_series(0, 1000),generate_series(0, 99));
insert into  t_subpartition_0345 values (generate_series(-19, 19),generate_series(-10, 100),generate_series(0, 99));
--step5: 查看参数query_dop的值; expect:成功
show query_dop ;
--step6: 修改参数query_dop的值为3; expect:成功
set query_dop=3;
--step7: 查看执行计划; expect:成功
explain select * from t_subpartition_0345  a,t_subpartition_0345 b  where a.col_1=b.col_2 and  a.col_1 >10;

--test3: package
--step8: 清空表数据; expect:成功
truncate t_subpartition_0345;
--step9: 创建package1; expect:成功
drop package if exists pkg1;
drop package if exists pkg2;
create or replace package pkg1 as
  function func(var1 int, var2 int) return int;
end pkg1;
/
create or replace package body pkg1 as
  function func(var1 int, var2 int) return int as
  begin
    raise info 'pkg1.func is called';
    insert into t_subpartition_0345 values(var1,var2);
    update t_subpartition_0345 set col_2=8 where col_2=4;
    return 0;
  end;
end pkg1;
/
--step10: 创建package2; expect:成功
create or replace package pkg2 as
  function func1(var1 int, var2 int) return int;
end pkg2;
/
create or replace package body pkg2 as
  function func1(var1 int, var2 int) return int as
  begin
    raise info 'pkg2.func1 is called';
    insert into t_subpartition_0345 values(var1,var2);
    delete t_subpartition_0345 where col_2=8;
    return 0;
  end;
end pkg2;
/
--step11: 调用package1; expect:成功
call pkg1.func(4,4);
--step12: 调用package2; expect:成功
call pkg2.func1(5,5);
--step13: 查询数据; expect:成功
select * from t_subpartition_0345 ;
--step14: 查询数据; expect:成功,2条数据
select pkgname,pkgspecsrc,pkgbodydeclsrc from gs_package;

--step15: 删除package; expect:成功
drop package if exists pkg1;
drop package if exists pkg2;

--test4: 生成列
--step16: 创建二级分区表,一级分区列指定生成列; expect:合理报错
drop table if exists t_subpartition_0345;
create table t_subpartition_0345
(
    col_1 int generated always as(2*col_4) stored ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0345
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
    subpartition t_subpartition_0345
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step17: 创建二级分区表,二级分区列指定生成列; expect:合理报错
drop table if exists t_subpartition_0345;
create table t_subpartition_0345
(
    col_1 int ,
    col_2 int generated always as(2*col_4) stored ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0345
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
    subpartition t_subpartition_0345
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step18: 创建二级分区表,普通列指定生成列; expect:成功
drop table if exists t_subpartition_0345;
create table t_subpartition_0345
(
    col_1 int ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int generated always as(2*col_1) stored
)
tablespace ts_subpartition_0345
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
    subpartition p_hash_4_3
  ),
  partition p_range_5 values less than( maxvalue )
) enable row movement;
--step19: 插入数据; expect:成功
insert into t_subpartition_0345 values(1,1,1),(4,4,4),(5,5,5),(8,8,8),(9,9,9);
insert into t_subpartition_0345(col_1,col_2,col_3)  values(31,1,1),(34,4,4),(45,5,5),(68,8,8),(70,9,9);
--step20: 查询指定分区数据; expect:成功
select * from t_subpartition_0345 partition(p_range_4);
--step21: 查询指定分区数据; expect:成功
select * from t_subpartition_0345 subpartition(p_hash_4_1);
--step22: 查询指定分区数据; expect:成功
select * from t_subpartition_0345 partition(p_range_5);
--step23: 查询指定分区数据; expect:成功
select * from t_subpartition_0345 subpartition(p_range_5_subpartdefault1);

--step24: 清理环境; expect:成功
drop table if exists t_subpartition_0345;
drop tablespace if exists ts_subpartition_0345;
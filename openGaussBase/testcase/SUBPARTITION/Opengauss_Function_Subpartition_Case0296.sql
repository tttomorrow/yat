-- @testpoint: range_range二级分区表：并行查询smp/package/segment表/生成列,部分测试点合理报错

--step1: 创建表空间; expect:成功
drop table if exists t_subpartition_0296;
drop tablespace if exists ts_subpartition_0296;
create tablespace ts_subpartition_0296 relative location 'subpartition_tablespace/subpartition_tablespace_0296';

--test1: 并行查询smp
--step2: 创建二级分区表; expect:成功
create table t_subpartition_0296
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0296
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
);
--step3: 插入大量数据; expect:成功
insert into  t_subpartition_0296 values (generate_series(0, 10),generate_series(0, 8000),generate_series(0, 99));
--step4: 查看参数query_dop的值; expect:成功
show query_dop ;
--step5: 修改参数query_dop的值为2; expect:成功
set query_dop=2;
--step6: 查看执行计划; expect:成功
explain select col_1,upper(col_3) from t_subpartition_0296 subpartition(p_range_1_2)   order by col_1 limit 10 ;

--test2: package
--step7: 清空表数据; expect:成功
truncate t_subpartition_0296;
--step8: 创建package1; expect:成功
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
    insert into t_subpartition_0296 values(var1,var2);
    update t_subpartition_0296 set col_2=8 where col_2=4;
    return 0;
  end;
end pkg1;
/
--step9: 创建package2; expect:成功
create or replace package pkg2 as
  function func1(var1 int, var2 int) return int;
end pkg2;
/
create or replace package body pkg2 as
  function func1(var1 int, var2 int) return int as
  begin
    raise info 'pkg2.func1 is called';
    insert into t_subpartition_0296 values(var1,var2);
    delete t_subpartition_0296 where col_2=8;
    return 0;
  end;
end pkg2;
/
--step10: 调用package1; expect:成功
call pkg1.func(4,4);
--step11: 调用package2; expect:成功
call pkg2.func1(5,5);
--step12: 查询数据; expect:成功
select * from t_subpartition_0296 ;
--step13: 查询数据; expect:成功,2条数据
select pkgname,pkgspecsrc,pkgbodydeclsrc from gs_package;

--step14: 删除package; expect:成功
drop package if exists pkg1;
drop package if exists pkg2;

--test3: segment表
--step15: 创建二级分区表,指定segment=on; expect:成功
drop table if exists t_subpartition_0296 cascade;
create table t_subpartition_0296
(
    col_1 int ,
    col_2 int,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)with (segment=on)
tablespace ts_subpartition_0296
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
);

--test4: 生成列
--step16: 创建二级分区表,二级分区列指定生成列; expect:合理报错
drop table if exists t_subpartition_0296;
create table t_subpartition_0296
(
    col_1 int,
    col_2 int generated always as(2*col_4) stored ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0296
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
);
--step17: 创建二级分区表,一级分区键指定生成列; expect:合理报错
drop table if exists t_subpartition_0296;
create table t_subpartition_0296
(
    col_1 int generated always as(2*col_2) stored ,
    col_2 int ,
    col_3 varchar2 ( 30 ) ,
    col_4 int
)
tablespace ts_subpartition_0296
partition by range (col_1) subpartition by range (col_2)
(
  partition p_range_1 values less than( 10 )
  (
    subpartition p_range_1_1 values less than( 50 ),
    subpartition p_range_1_2 values less than( maxvalue )
  ),
  partition p_range_2 values less than( 80 )
  (
    subpartition p_range_2_1 values less than( 50 ),
    subpartition p_range_2_2 values less than( maxvalue )
  )
);

--step18: 清理环境; expect:成功
drop table if exists t_subpartition_0296;
drop tablespace if exists ts_subpartition_0296;